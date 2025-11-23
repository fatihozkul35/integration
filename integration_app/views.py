from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging
from .models import ContactMessage

logger = logging.getLogger(__name__)

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
                contact_message = ContactMessage.objects.create(
                    name=name,
                    email=email if email else None,
                    phone=phone if phone else None,
                    message=message,
                    consent=True if consent else False
                )
                
                # E-posta gönder
                try:
                    send_contact_notification_email(contact_message)
                except Exception as email_error:
                    # E-posta gönderim hatası olsa bile form kaydı başarılı oldu
                    # Hata detaylarını logla
                    logger.error(f'E-posta gönderim hatası: {str(email_error)}', exc_info=True)
                    # Kullanıcıya hata göstermiyoruz ama logluyoruz
                
                messages.success(request, _('Ihre Nachricht wurde erfolgreich gesendet!'))
                # Formu temizlemek için redirect
                return redirect('integration_app:contact')
            except Exception as e:
                messages.error(request, _('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.'))
    
    return render(request, 'integration_app/contact.html')


def send_contact_notification_email(contact_message):
    """
    Contact formu gönderildiğinde admin'e bildirim e-postası gönderir
    """
    # Admin e-posta adreslerini al
    admin_emails = [admin[1] for admin in settings.ADMINS if admin[1]]
    
    if not admin_emails:
        logger.warning('Admin e-posta adresi bulunamadı. E-posta gönderilemedi.')
        return
    
    # E-posta ayarlarını logla (debug için)
    logger.info(f'E-posta gönderiliyor - FROM: {settings.DEFAULT_FROM_EMAIL}, TO: {admin_emails}')
    
    # E-posta içeriği için context
    context = {
        'contact_name': contact_message.name or '',
        'contact_email': contact_message.email or '',
        'contact_phone': contact_message.phone or '',
        'contact_message': contact_message.message or '',
        'contact_date': contact_message.created_at or timezone.now(),
    }
    
    # E-posta konusu
    subject = f'Neue Kontaktnachricht von {context["contact_name"] or "Unbekannt"}'
    
    # Text ve HTML içerikleri oluştur
    text_content = render_to_string('integration_app/emails/contact_notification.txt', context)
    html_content = render_to_string('integration_app/emails/contact_notification.html', context)
    
    # E-posta oluştur ve gönder
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=admin_emails,
        )
        email.attach_alternative(html_content, "text/html")
        result = email.send()
        logger.info(f'E-posta gönderildi. Sonuç: {result}')
    except Exception as e:
        logger.error(f'E-posta gönderim hatası: {str(e)}', exc_info=True)
        raise