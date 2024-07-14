from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI


def main_view(request):
    return render(request, 'main.html')


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
