from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.urls import get_resolver, reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
import logging
import json
import os
from datetime import datetime
from .models import ContactMessage

logger = logging.getLogger(__name__)

# #region agent log
DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
# #endregion

# Create your views here.

def get_redirect_url_with_anchor(request, anchor='#contact-form-section'):
    """
    Referer URL'den sayfa yolunu çıkarır ve anchor ile birlikte redirect URL'i döndürür.
    Eğer referer yoksa veya geçersizse, contact sayfasına yönlendirir.
    """
    referer = request.META.get('HTTP_REFERER', '')
    
    if not referer:
        # Referer yoksa contact sayfasına yönlendir
        return reverse('integration_app:contact')
    
    # Referer URL'ini parse et
    parsed = urlparse(referer)
    path = parsed.path
    
    # Path'ten anchor'ı temizle (varsa)
    if '#' in path:
        path = path.split('#')[0]
    
    # Path'i temizle (başında ve sonunda / varsa)
    path = path.strip('/')
    
    # Path'i URL name'e map et
    url_mapping = {
        '': 'integration_app:index',
        'hakkimizda': 'integration_app:about',
        'hizmetler': 'integration_app:services',
        'kontakt': 'integration_app:contact',
        'contact': 'integration_app:contact',
        'hukuki-bilgilendirme': 'integration_app:legal_info',
        'vize-yollari': 'integration_app:visa_routes',
        'surec-nasil-isler': 'integration_app:process',
        'isverenler-icin': 'integration_app:employers',
        'faq': 'integration_app:faq',
        'referenzen': 'integration_app:references',
        'blog': 'integration_app:blog',
        'almanyada-yasamin-rehberi': 'integration_app:life_guide',
    }
    
    # Path'i kontrol et ve URL name'i bul
    url_name = None
    if path in url_mapping:
        url_name = url_mapping[path]
    elif path == '' or path == 'index':
        url_name = 'integration_app:index'
    else:
        # Bilinmeyen path için contact sayfasına yönlendir
        url_name = 'integration_app:contact'
    
    # URL'i oluştur ve anchor ekle
    try:
        url = reverse(url_name)
        # Contact sayfasından geliyorsa anchor ekleme
        if url_name == 'integration_app:contact':
            return url
        return f"{url}{anchor}"
    except:
        # Hata durumunda contact sayfasına yönlendir
        return reverse('integration_app:contact')

def index(request):
    """Home page view that renders index.html"""
    # Ana sayfadaki form POST request'i ise contact view'ını çağır
    if request.method == 'POST':
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

def life_guide(request):
    """Almanya'da Yaşamın Rehberi page view"""
    return render(request, 'integration_app/life_guide.html')

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
            # Hata varsa referer sayfasına geri dön
            redirect_url = get_redirect_url_with_anchor(request)
            return HttpResponseRedirect(redirect_url)
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
                # Formu temizlemek için redirect - referer sayfasına geri dön
                redirect_url = get_redirect_url_with_anchor(request)
                return HttpResponseRedirect(redirect_url)
            except Exception as e:
                messages.error(request, 'Bir hata oluştu. Lütfen tekrar deneyin.')
    
    return render(request, 'integration_app/contact.html')


def send_contact_notification_email(contact_message):
    """
    Contact formu gönderildiğinde:
    1. Kullanıcıya teşekkür e-postası gönderir
    2. Admin'e bildirim e-postası gönderir
    Spam önleme için uygun e-posta başlıkları eklenir
    """
    # #region agent log
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'id': f'log_{int(datetime.now().timestamp() * 1000)}_entry',
                'timestamp': int(datetime.now().timestamp() * 1000),
                'location': 'integration_app/views.py:221',
                'message': 'send_contact_notification_email function entry',
                'data': {'contact_id': contact_message.id if hasattr(contact_message, 'id') else None},
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'A'
            }, ensure_ascii=False) + '\n')
    except: pass
    # #endregion
    
    # #region agent log
    try:
        smtp_config = {
            'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', 'NOT_SET'),
            'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 'NOT_SET'),
            'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', 'NOT_SET'),
            'EMAIL_USE_SSL': getattr(settings, 'EMAIL_USE_SSL', 'NOT_SET'),
            'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', 'NOT_SET')[:10] + '...' if getattr(settings, 'EMAIL_HOST_USER', '') else 'EMPTY',
            'EMAIL_HOST_PASSWORD': '***' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'EMPTY',
            'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', 'NOT_SET'),
            'EMAIL_TIMEOUT': getattr(settings, 'EMAIL_TIMEOUT', 'NOT_SET'),
        }
        logger.info(f'[DEBUG] SMTP Config: {smtp_config}')
        try:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'id': f'log_{int(datetime.now().timestamp() * 1000)}_smtp_config',
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'location': 'integration_app/views.py:235',
                    'message': 'SMTP configuration values',
                    'data': smtp_config,
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A,B,C'
                }, ensure_ascii=False) + '\n')
        except: pass
    except Exception as e:
        logger.error(f'[DEBUG] Error reading SMTP config: {e}', exc_info=True)
        try:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'id': f'log_{int(datetime.now().timestamp() * 1000)}_config_error',
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'location': 'integration_app/views.py:235',
                    'message': 'Error reading SMTP config',
                    'data': {'error': str(e)},
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'B'
                }, ensure_ascii=False) + '\n')
        except: pass
    # #endregion
    
    # E-posta içeriği için context
    context = {
        'contact_name': contact_message.name or '',
        'contact_email': contact_message.email or '',
        'contact_phone': contact_message.phone or '',
        'contact_message': contact_message.message or '',
        'contact_date': contact_message.created_at or timezone.now(),
    }
    
    # E-posta başlıkları - Spam önleme ve deliverability için önemli
    headers = {
        'X-Mailer': 'Django Contact Form',
        'X-Priority': '1',
        'Importance': 'high',
    }
    
    # 1. KULLANICIYA TEŞEKKÜR E-POSTASI GÖNDER
    # SEND_USER_CONFIRMATION_EMAIL ayarı False ise kullanıcıya e-posta gönderme
    if context['contact_email'] and getattr(settings, 'SEND_USER_CONFIRMATION_EMAIL', True):
        try:
            # Kullanıcıya teşekkür e-postası
            user_subject = 'Vielen Dank für Ihre Nachricht'
            user_text_content = render_to_string('integration_app/emails/contact_confirmation.txt', context)
            user_html_content = render_to_string('integration_app/emails/contact_confirmation.html', context)
            
            user_email = EmailMultiAlternatives(
                subject=user_subject,
                body=user_text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[context['contact_email']],
                headers=headers,
            )
            user_email.attach_alternative(user_html_content, "text/html")
            user_result = user_email.send()
            logger.info(f'Kullanıcıya teşekkür e-postası gönderildi. TO: {context["contact_email"]}, Sonuç: {user_result}')
        except Exception as e:
            error_message = str(e)
            # ElasticEmail test hesabı limiti kontrolü
            if '421' in error_message and 'testing purposes' in error_message.lower():
                logger.warning(
                    f'ElasticEmail test hesabı limiti: Kullanıcıya e-posta gönderilemedi. '
                    f'TO: {context["contact_email"]}. '
                    f'Not: Test hesabı sadece kayıt e-postasına gönderebilir. '
                    f'Production için ElasticEmail planı gerekli.'
                )
            else:
                logger.error(f'Kullanıcıya e-posta gönderim hatası: {error_message}', exc_info=True)
            # Kullanıcıya e-posta gönderilemese bile admin'e göndermeye devam et
    
    # 2. ADMIN'E BİLDİRİM E-POSTASI GÖNDER
    admin_emails = [admin[1] for admin in settings.ADMINS if admin[1]]
    
    # #region agent log
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'id': f'log_{int(datetime.now().timestamp() * 1000)}_admin_emails',
                'timestamp': int(datetime.now().timestamp() * 1000),
                'location': 'integration_app/views.py:278',
                'message': 'Admin emails check',
                'data': {'admin_emails': admin_emails, 'count': len(admin_emails)},
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'A'
            }, ensure_ascii=False) + '\n')
    except: pass
    # #endregion
    
    if not admin_emails:
        logger.warning('Admin e-posta adresi bulunamadı. Admin e-postası gönderilemedi.')
        return
    
    # #region agent log
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'id': f'log_{int(datetime.now().timestamp() * 1000)}_before_send',
                'timestamp': int(datetime.now().timestamp() * 1000),
                'location': 'integration_app/views.py:284',
                'message': 'Before admin email send attempt',
                'data': {
                    'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT_SET'),
                    'to_emails': admin_emails,
                    'smtp_host': getattr(settings, 'EMAIL_HOST', 'NOT_SET'),
                    'smtp_port': getattr(settings, 'EMAIL_PORT', 'NOT_SET')
                },
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'A,C,D'
            }, ensure_ascii=False) + '\n')
    except: pass
    # #endregion
    
    try:
        # Admin'e bildirim e-postası
        admin_subject = f'Neue Kontaktnachricht - {context["contact_name"] or "Unbekannt"}'
        admin_text_content = render_to_string('integration_app/emails/contact_notification.txt', context)
        admin_html_content = render_to_string('integration_app/emails/contact_notification.html', context)
        
        # Reply-To: İletişim formundan gelen e-posta adresi (varsa)
        # Bu sayede admin direkt kullanıcıya cevap verebilir
        reply_to = [context['contact_email']] if context['contact_email'] else None
        
        admin_email = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=admin_emails,
            reply_to=reply_to,
            headers=headers,
        )
        admin_email.attach_alternative(admin_html_content, "text/html")
        
        # #region agent log
        try:
            from django.core.mail import get_connection
            import socket
            conn = get_connection()
            conn_params = {
                'host': conn.host if hasattr(conn, 'host') else 'N/A',
                'port': conn.port if hasattr(conn, 'port') else 'N/A',
                'use_tls': conn.use_tls if hasattr(conn, 'use_tls') else 'N/A',
                'use_ssl': conn.use_ssl if hasattr(conn, 'use_ssl') else 'N/A',
            }
            # Test network connectivity
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(5)
                test_result = test_socket.connect_ex((conn.host, conn.port))
                test_socket.close()
                conn_params['socket_test'] = 'SUCCESS' if test_result == 0 else f'FAILED: {test_result}'
            except Exception as sock_err:
                conn_params['socket_test'] = f'ERROR: {str(sock_err)}'
            logger.info(f'[DEBUG] Connection params: {conn_params}')
            try:
                with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({
                        'id': f'log_{int(datetime.now().timestamp() * 1000)}_connection_params',
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'location': 'integration_app/views.py:303',
                        'message': 'SMTP connection parameters from backend',
                        'data': conn_params,
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'A,C,D'
                    }, ensure_ascii=False) + '\n')
            except: pass
        except Exception as conn_err:
            logger.error(f'[DEBUG] Error getting connection params: {conn_err}', exc_info=True)
            try:
                with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({
                        'id': f'log_{int(datetime.now().timestamp() * 1000)}_conn_error',
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'location': 'integration_app/views.py:303',
                        'message': 'Error getting connection params',
                        'data': {'error': str(conn_err)},
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'B'
                    }, ensure_ascii=False) + '\n')
            except: pass
        # #endregion
        
        admin_result = admin_email.send()
        
        # #region agent log
        try:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'id': f'log_{int(datetime.now().timestamp() * 1000)}_send_success',
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'location': 'integration_app/views.py:303',
                    'message': 'Admin email send successful',
                    'data': {'result': admin_result},
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A'
                }, ensure_ascii=False) + '\n')
        except: pass
        # #endregion
        
        logger.info(f'Admin e-postası gönderildi. TO: {admin_emails}, Sonuç: {admin_result}')
    except Exception as e:
        # #region agent log
        try:
            import traceback
            error_details = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_args': list(e.args) if hasattr(e, 'args') else [],
                'traceback': traceback.format_exc(),
            }
            logger.error(f'[DEBUG] Admin email send error details: {error_details}')
            try:
                with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({
                        'id': f'log_{int(datetime.now().timestamp() * 1000)}_send_error',
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'location': 'integration_app/views.py:305',
                        'message': 'Admin email send error details',
                        'data': error_details,
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'A,C,D,E'
                    }, ensure_ascii=False) + '\n')
            except: pass
        except: pass
        # #endregion
        
        logger.error(f'Admin e-posta gönderim hatası: {str(e)}', exc_info=True)
        raise


def is_staff_user(user):
    """Check if user is staff/admin"""
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user, login_url='/admin/login/')
def urls_list(request):
    """List all URLs in the project - Admin only"""
    from django.urls.resolvers import URLPattern, URLResolver
    
    resolver = get_resolver()
    urls = []
    seen_urls = set()  # To avoid duplicates
    
    def extract_urls(url_patterns, prefix='', namespace=''):
        """Recursively extract all URL patterns"""
        for pattern in url_patterns:
            if isinstance(pattern, URLResolver):
                # This is an include() pattern
                pattern_str = str(pattern.pattern) if hasattr(pattern, 'pattern') and pattern.pattern else ''
                new_prefix = prefix + pattern_str
                
                # Handle namespace
                new_namespace = namespace
                if hasattr(pattern, 'namespace') and pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                elif hasattr(pattern, 'app_name') and pattern.app_name:
                    new_namespace = f"{namespace}:{pattern.app_name}" if namespace else pattern.app_name
                
                # Recursively process nested patterns
                if hasattr(pattern, 'url_patterns'):
                    extract_urls(pattern.url_patterns, new_prefix, new_namespace)
            elif isinstance(pattern, URLPattern):
                # This is a regular path pattern
                pattern_str = str(pattern.pattern) if hasattr(pattern, 'pattern') and pattern.pattern else ''
                url_path = prefix + pattern_str
                url_name = pattern.name if hasattr(pattern, 'name') and pattern.name else ''
                
                # Build full name with namespace
                if namespace and url_name:
                    full_name = f"{namespace}:{url_name}"
                else:
                    full_name = url_name if url_name else ''
                
                # Build full URL - clean up the path
                if url_path:
                    # Remove regex markers and clean up
                    url_path = url_path.replace('^', '').replace('$', '')
                    # Remove leading/trailing slashes and add properly
                    url_path = url_path.strip('/')
                    full_url = f"/{url_path}" if url_path else "/"
                else:
                    full_url = "/"
                
                # Avoid duplicates
                url_key = (full_url, full_name)
                if url_key not in seen_urls:
                    seen_urls.add(url_key)
                    urls.append({
                        'url': full_url,
                        'name': full_name,
                        'pattern': pattern_str,
                    })
    
    extract_urls(resolver.url_patterns)
    
    # Filter out admin URLs, media URLs, and urls_list page itself
    urls = [
        url_item for url_item in urls 
        if not url_item['url'].startswith('/admin') 
        and not url_item['name'].startswith('admin:')
        and 'admin' not in url_item['name'].lower()
        and not url_item['url'].startswith('/media')
        and url_item['url'] != '/urls/'
        and url_item['name'] != 'integration_app:urls_list'
    ]
    
    # Sort URLs by path
    urls.sort(key=lambda x: x['url'])
    
    context = {
        'urls': urls,
    }
    
    return render(request, 'integration_app/urls_list.html', context)