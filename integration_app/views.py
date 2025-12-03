from django.shortcuts import render, redirect
from django.contrib import messages
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
    # Ana sayfadaki form POST request'i ise contact view'ını çağır
    if request.method == 'POST':
        # Contact view'ını çağır ama referer'ı index olarak ayarla
        request.META['HTTP_REFERER'] = request.build_absolute_uri('/')
        return contact(request)
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

def visa_routes(request):
    """Visa routes / Qualified Migration Law page view"""
    return render(request, 'integration_app/visa_routes.html')

def employers(request):
    """For employers page view"""
    return render(request, 'integration_app/employers.html')

def legal_info(request):
    """Legal information page view"""
    return render(request, 'integration_app/legal_info.html')

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
        age = request.POST.get('age', '').strip()
        marital_status = request.POST.get('marital_status', '').strip()
        children_count = request.POST.get('children_count', '0').strip()
        driving_license = request.POST.get('driving_license', '').strip()
        profession = request.POST.get('profession', '').strip()
        graduation = request.POST.get('graduation', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        consent = request.POST.get('consent')
        
        # Validation
        errors = []
        
        if not consent:
            errors.append('Gizlilik politikasına onay vermelisiniz.')
        
        # Zorunlu alanlar
        if not age:
            errors.append('Yaş bilgisi zorunludur.')
        if not marital_status:
            errors.append('Medeni durum seçimi zorunludur.')
        if not driving_license:
            errors.append('Sürücü belgesi sınıfı zorunludur.')
        if not profession:
            errors.append('Meslek bilgisi zorunludur.')
        if not graduation:
            errors.append('Mezuniyet bilgisi zorunludur.')
        if not email:
            errors.append('E-Posta adresi zorunludur.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            # Hata varsa referer'a göre yönlendir
            referer = request.META.get('HTTP_REFERER', '')
            # Ana sayfadan geliyorsa ana sayfaya dön
            if referer and (referer.endswith('/') or '/index' in referer or 'index' in referer.lower()):
                return redirect('integration_app:index#contact-form-section')
            else:
                return render(request, 'integration_app/contact.html')
        else:
            # Veritabanına kaydet
            try:
                # Yaş ve çocuk sayısı için integer dönüşümü
                age_int = None
                if age:
                    try:
                        age_int = int(age)
                    except ValueError:
                        age_int = None
                
                children_count_int = 0
                if children_count:
                    try:
                        children_count_int = int(children_count)
                    except ValueError:
                        children_count_int = 0
                
                contact_message = ContactMessage.objects.create(
                    name=name if name else None,
                    age=age_int,
                    marital_status=marital_status if marital_status else '',
                    children_count=children_count_int,
                    driving_license=driving_license if driving_license else '',
                    profession=profession if profession else '',
                    graduation=graduation if graduation else '',
                    email=email if email else None,
                    phone=phone if phone else None,
                    message=message if message else '',
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
                
                messages.success(request, 'Mesajınız başarıyla gönderildi!')
                # Formu temizlemek için redirect - referer'a göre yönlendir
                referer = request.META.get('HTTP_REFERER', '')
                # Ana sayfadan geliyorsa ana sayfaya dön (form bölümüne anchor ile)
                # Referer kontrolü: ana sayfa URL'i genellikle '/' ile biter veya 'index' içerir
                if referer and (referer.endswith('/') or '/index' in referer or 'index' in referer.lower() or not '/kontakt' in referer.lower() and not '/contact' in referer.lower()):
                    return redirect('integration_app:index#contact-form-section')
                else:
                    return redirect('integration_app:contact')
            except Exception as e:
                messages.error(request, 'Bir hata oluştu. Lütfen tekrar deneyin.')
    
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
    subject = f'Yeni İletişim Mesajı - {context["contact_name"] or "İsimsiz"}'
    
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