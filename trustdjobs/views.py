from django.shortcuts import render, HttpResponse
from django.core import management

def index(request):
    
    management.call_command('scrappy')
    return HttpResponse("Done Scraping Jobs!")

