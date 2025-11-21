from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import ContactMessage

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
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        consent = request.POST.get('consent')
        
        # Validation
        errors = []
        
        if not consent:
            errors.append(_('Sie müssen der Datenschutzerklärung zustimmen.'))
        
        # En az bir iletişim bilgisi gerekli
        if not email and not phone:
            errors.append(_('Bitte geben Sie mindestens eine Kontaktmöglichkeit an (E-Mail oder Telefon).'))
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Veritabanına kaydet
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email if email else None,
                    phone=phone if phone else None,
                    message=message,
                    consent=True if consent else False
                )
                messages.success(request, _('Ihre Nachricht wurde erfolgreich gesendet!'))
                # Formu temizlemek için redirect
                return redirect('integration_app:contact')
            except Exception as e:
                messages.error(request, _('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.'))
    
    return render(request, 'integration_app/contact.html')