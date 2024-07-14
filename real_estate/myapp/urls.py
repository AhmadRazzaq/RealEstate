from django.urls import path
from .views import main_view, start_website_process

urlpatterns = [
    path('', main_view, name='main_view'),
    path('start-website-process/', start_website_process, name='start_website_process'),

]
