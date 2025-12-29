from functools import wraps
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def rate_limit_contact(max_requests=5, period=86400):
    """
    Rate limiting decorator for contact form submissions.
    
    Args:
        max_requests: Maximum number of requests allowed (default: 5)
        period: Time period in seconds (default: 86400 = 24 hours)
    
    Checks both IP address and email address to prevent abuse.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Only apply rate limiting to POST requests
            if request.method != 'POST':
                return view_func(request, *args, **kwargs)
            
            # Get IP address
            ip_address = get_client_ip(request)
            
            # Get email from POST data
            email = request.POST.get('email', '').strip().lower()
            
            # Check IP-based rate limit
            ip_cache_key = f'rate_limit:contact:ip:{ip_address}'
            ip_count = cache.get(ip_cache_key, 0)
            
            if ip_count >= max_requests:
                messages.error(
                    request,
                    'Günlük gönderim limitinize ulaştınız. Lütfen yarın tekrar deneyin.'
                )
                # Redirect back to the referer page or contact page
                redirect_url = request.META.get('HTTP_REFERER', reverse('integration_app:contact'))
                return HttpResponseRedirect(redirect_url)
            
            # Check email-based rate limit (only if email is provided)
            if email:
                email_cache_key = f'rate_limit:contact:email:{email}'
                email_count = cache.get(email_cache_key, 0)
                
                if email_count >= max_requests:
                    messages.error(
                        request,
                        'Bu e-posta adresi ile günlük gönderim limitinize ulaştınız. Lütfen yarın tekrar deneyin.'
                    )
                    # Redirect back to the referer page or contact page
                    redirect_url = request.META.get('HTTP_REFERER', reverse('integration_app:contact'))
                    return HttpResponseRedirect(redirect_url)
            
            # Call the original view function
            response = view_func(request, *args, **kwargs)
            
            # Increment counters only if the form submission was successful
            # We check if there's a success message indicating successful submission
            # The view adds 'Mesajınız başarıyla gönderildi!' message on success
            storage = messages.get_messages(request)
            has_success = any(
                msg.level_tag == 'success' and 'başarıyla gönderildi' in msg.message.lower()
                for msg in storage
            )
            
            # Only increment if we have a success message (ContactMessage was created)
            if has_success:
                # Increment IP counter
                cache.set(ip_cache_key, ip_count + 1, period)
                
                # Increment email counter if email is provided
                if email:
                    cache.set(email_cache_key, email_count + 1, period)
            
            return response
        
        return wrapped_view
    return decorator

