from django.urls import path
from .views import main_view, start_website_process, events_view, call_to_fetch_results, download_Data_into_csv

urlpatterns = [
    path('', main_view, name='main_view'),
    path('events/', events_view, name='events_view'),
    path('call_to_fetch_results', call_to_fetch_results, name='call_to_fetch_results'),
    path('download_Data_into_csv', download_Data_into_csv, name='download_Data_into_csv'),
    path('start-website-process/', start_website_process, name='start_website_process'),

]
