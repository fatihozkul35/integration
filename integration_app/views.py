from django.shortcuts import render, redirect
from django.contrib import messages
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
from .models import ContactMessage, SliderImage, AppConfig
from .utils import rate_limit_contact

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
    
    # Aktif slider görsellerini sıralı şekilde getir
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order', 'created_at')
    
    context = {
        'slider_images': slider_images,
    }
    
    return render(request, 'integration_app/index.html', context)

def services(request):
    """Services page view"""
    return render(request, 'integration_app/services.html')

def about(request):
    """About us page view"""
    app_config = AppConfig.load() if AppConfig.objects.exists() else None
    context = {
        'app_config': app_config,
    }
    return render(request, 'integration_app/about.html', context)

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

@rate_limit_contact(max_requests=5, period=86400)
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
                
                # Başarı mesajını göster ve redirect yap
                messages.success(request, 'Mesajınız başarıyla gönderildi!')
                redirect_url = get_redirect_url_with_anchor(request)
                return HttpResponseRedirect(redirect_url)
            except Exception as e:
                print(e)
                messages.error(request, 'Bir hata oluştu. Lütfen tekrar deneyin.')
                redirect_url = get_redirect_url_with_anchor(request)
                return HttpResponseRedirect(redirect_url)
    
    return render(request, 'integration_app/contact.html')


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