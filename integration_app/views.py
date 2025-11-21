from django.shortcuts import render

# Create your views here.

def index(request):
    """Home page view that renders index.html"""
    return render(request, 'integration_app/index.html')