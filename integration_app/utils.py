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
            # We can't use messages.get_messages() here because it consumes messages
            # and they won't be available in the template after redirect.
            # Instead, we'll check if response is a redirect (which indicates success)
            # and if it's redirecting to contact page or back to referer (success case)
            # Note: This is a simple heuristic - if view redirects, it's likely successful
            # Error messages also redirect, but they're handled by the view itself
            # The view only redirects on success or validation errors (which we catch above)
            if isinstance(response, HttpResponseRedirect):
                # Check if redirect URL indicates success (not an error page)
                redirect_url = response.url
                # If redirecting to contact page or back to referer, it's likely successful
                # We'll increment counter for any redirect (conservative approach)
                # The view will handle showing appropriate messages
                # Increment IP counter
                cache.set(ip_cache_key, ip_count + 1, period)
                
                # Increment email counter if email is provided
                if email:
                    cache.set(email_cache_key, email_count + 1, period)
            
            return response
        
        return wrapped_view
    return decorator

