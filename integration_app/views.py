from django.shortcuts import render

# Create your views here.

def index(request):
    """Home page view that renders index.html"""
    return render(request, 'integration_app/index.html')

def services(request):
    """Services page view"""
    return render(request, 'integration_app/services.html')

def about(request):
    """About us page view"""
    return render(request, 'integration_app/about.html')

def process(request):
    """Process / How it works page view"""
    return render(request, 'integration_app/process.html')

def pricing(request):
    """Pricing page view"""
    return render(request, 'integration_app/pricing.html')

def faq(request):
    """FAQ page view"""
    return render(request, 'integration_app/faq.html')

def references(request):
    """References / Testimonials page view"""
    return render(request, 'integration_app/references.html')

def blog(request):
    """Blog page view"""
    return render(request, 'integration_app/blog.html')

def contact(request):
    """Contact page view"""
    return render(request, 'integration_app/contact.html')