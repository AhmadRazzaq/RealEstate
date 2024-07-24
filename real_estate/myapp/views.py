import json
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI
from django.db import IntegrityError, connection
import csv
from django.http import HttpResponse


def main_view(request):
    return render(request, 'main.html')


def events_view(request):
    return render(request, 'events_page.html')


def fetch_data_according_to_query(organizer_name, database_name, city_name):
    if database_name == 'tixr_data':
        query = f'SELECT * FROM defaultdb.{database_name} WHERE Address LIKE %s AND Venue LIKE %s'
    else:
        query = f'SELECT * FROM defaultdb.{database_name} WHERE Location LIKE %s AND Venue LIKE %s'

    with connection.cursor() as cursor:
        cursor.execute(query, ('%' + city_name + '%', '%' + organizer_name + '%'))
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data_returned = [dict(zip(columns, row)) for row in results]

    return data_returned

@require_POST
@csrf_exempt
def download_Data_into_csv(request):
    data = cache.get("last_data")
    if not data:
        return JsonResponse({"Message": "No data found"}, status=404)
    # for iteration in data[:1]:
    #     print("--->", iteration)
        # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    if data:
        # Write headers (keys of the first dictionary)
        headers = data[0].keys()
        writer.writerow(headers)
        for item in data:
            writer.writerow(item.values())

    return response


@require_POST
def call_to_fetch_results(request):
    organizer_name = request.POST.get('organizer_name')
    city_name = request.POST.get('city_name')
    source_name = request.POST.get('source_name')

    print(f"Organizer Name: {organizer_name}")
    print(f"City Name: {city_name}")
    print(f"Source Name: {source_name}")
    computed_data = fetch_data_according_to_query(organizer_name, source_name, city_name)
    if source_name == 'eventbrite_data':
        for iteration in computed_data:
            iteration['ImageUrl'] = "https://codewithninja.com/Image/noImage.png"
            iteration['TicketPackages'] = json.loads(iteration['TicketPackages'])
    if source_name == 'dice_data1':
        for iteration in computed_data:
            if iteration['ImageUrl'] == None or iteration['ImageUrl'] == '':
                iteration['ImageUrl'] = "https://codewithninja.com/Image/noImage.png"
            if iteration['Price'] == None or iteration['Price'] == '':
                iteration['Price'] = "N/A"
            # print("---->", iteration)
    if source_name == 'tixr_data':
        for iteration in computed_data:
            iteration['Prices'] = json.loads(iteration['Prices'])
            # print("---->", iteration)
    cache.set("last_data", computed_data)
    listingPageHtml = render_to_string(
        r'jinja_form.html', {'computed_Data': computed_data, 'source': source_name})
    response_data = {'listingPageHtml': listingPageHtml}
    return JsonResponse(response_data)


@csrf_exempt
def start_website_process(request):
    if request.method == 'POST':
        website_name = request.POST.get('website_name')
        print("Website Name:", website_name)
        if website_name == 'JBG Smith':
            scrapyd = ScrapydAPI('http://44.193.195.179:6800')
            scrapyd.schedule('jbgsmith', 'JBGS_Scraper')
            return JsonResponse(
                {'message': 'The Program is running, please download the file after 2 to 3 minutes thank you.',
                 'scraper': 'JBGS_Scraper'})
    return JsonResponse({'message': 'Invalid request'}, status=400)
