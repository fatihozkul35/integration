#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
E-posta gönderim hatasını test etmek ve detaylı hata mesajı almak için script.
Kullanım: python test_email_error.py
"""
import os
import sys
import django

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integration_project.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
import traceback

def test_admin_email():
    """Admin'e test e-postası gönderir ve hatayı gösterir"""
    print("=" * 60)
    print("E-POSTA GONDERIM HATA TESTI")
    print("=" * 60)
    
    # Ayarları göster
    print("\nE-posta Ayarlari:")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    admin_emails = [admin[1] for admin in settings.ADMINS if admin[1]]
    print(f"  ADMIN_EMAIL: {', '.join(admin_emails) if admin_emails else 'AYARLANMAMIS'}")
    
    if not admin_emails:
        print("\n[HATA] ADMIN_EMAIL ayarlanmamis!")
        return
    
    # Test context
    context = {
        'contact_name': 'Test Kullanici',
        'contact_email': 'test@example.com',
        'contact_phone': '+90 555 123 4567',
        'contact_message': 'Bu bir test mesajidir.',
        'contact_date': timezone.now(),
    }
    
    print("\n" + "=" * 60)
    print("E-posta gonderiliyor...")
    print("=" * 60)
    
    try:
        # Admin'e bildirim e-postası
        admin_subject = f'Test E-postasi - {context["contact_name"]}'
        admin_text_content = render_to_string('integration_app/emails/contact_notification.txt', context)
        admin_html_content = render_to_string('integration_app/emails/contact_notification.html', context)
        
        headers = {
            'X-Mailer': 'Django Contact Form',
            'X-Priority': '1',
            'Importance': 'high',
        }
        
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
        
        print(f"\nGonderen: {settings.DEFAULT_FROM_EMAIL}")
        print(f"Alici: {', '.join(admin_emails)}")
        print(f"Konu: {admin_subject}")
        
        admin_result = admin_email.send()
        
        print("\n" + "=" * 60)
        print("[BASARILI] E-posta basariyla gonderildi!")
        print(f"Sonuc: {admin_result}")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("[HATA] E-posta gonderim hatasi!")
        print("=" * 60)
        
        error_type = type(e).__name__
        error_message = str(e)
        
        print(f"\nHata Tipi: {error_type}")
        print(f"Hata Mesaji: {error_message}")
        
        # Yaygın hatalar için çözüm önerileri
        print("\n" + "-" * 60)
        print("COZUM ONERILERI:")
        print("-" * 60)
        
        if 'authentication' in error_message.lower() or '535' in error_message or 'SMTPAuthenticationError' in error_type:
            print("\n[SMTP Kimlik Dogrulama Hatasi]")
            print("  - EMAIL_HOST_USER ve EMAIL_HOST_PASSWORD dogru mu kontrol edin")
            print("  - ElasticEmail hesabinizda SMTP sifresini kontrol edin")
            print("  - API anahtari kullaniyorsaniz dogru anahtari kullandiginizdan emin olun")
            print("  - ElasticEmail hesabiniz aktif mi kontrol edin")
        
        elif 'connection' in error_message.lower() or 'timeout' in error_message.lower() or 'refused' in error_message.lower():
            print("\n[Baglanti Hatasi]")
            print("  - Port numarasini kontrol edin (2525, 587 veya 465)")
            print("  - Firewall ayarlarini kontrol edin")
            print("  - TLS/SSL ayarlarini kontrol edin")
            print("  - Internet baglantinizi kontrol edin")
        
        elif 'ssl' in error_message.lower() or 'certificate' in error_message.lower():
            print("\n[SSL Sertifika Hatasi]")
            print("  - EMAIL_USE_TLS ve EMAIL_USE_SSL ayarlarini kontrol edin")
            print("  - Port 465 icin EMAIL_USE_SSL=True olmali")
            print("  - Port 587 icin EMAIL_USE_TLS=True olmali")
        
        elif '421' in error_message and 'testing' in error_message.lower():
            print("\n[ElasticEmail Test Hesabi Limiti]")
            print("  - ElasticEmail test hesabi sadece kayit e-postasina gonderebilir")
            print("  - Production icin ElasticEmail plani gerekli")
        
        elif '550' in error_message or '553' in error_message or 'invalid' in error_message.lower():
            print("\n[Gecersiz E-posta Adresi]")
            print("  - DEFAULT_FROM_EMAIL adresi ElasticEmail'de dogrulanmis mi?")
            print("  - ADMIN_EMAIL adresi gecerli mi?")
            print("  - E-posta adreslerinde yazim hatasi var mi?")
        
        else:
            print("\n[Genel Hata]")
            print("  - Django log dosyalarini kontrol edin")
            print("  - ElasticEmail dashboard'unu kontrol edin")
            print("  - .env dosyasindaki tum ayarlari kontrol edin")
        
        print("\n" + "-" * 60)
        print("DETAYLI HATA BILGISI:")
        print("-" * 60)
        print(traceback.format_exc())

if __name__ == '__main__':
    try:
        test_admin_email()
    except Exception as e:
        print(f"\n[KRITIK HATA] Script hatasi: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

