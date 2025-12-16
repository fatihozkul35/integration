#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
E-posta yapılandırmasını kontrol etmek ve hataları teşhis etmek için script.
Kullanım: python diagnose_email.py
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

from django.conf import settings
from django.core.mail import get_connection
import socket

def check_email_config():
    """E-posta yapılandırmasını kontrol eder"""
    print("=" * 60)
    print("E-POSTA YAPILANDIRMA KONTROLÜ")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # 1. EMAIL_HOST kontrolü
    print("\n1. SMTP Sunucu Ayarlari:")
    email_host = getattr(settings, 'EMAIL_HOST', None)
    if not email_host or email_host == '':
        issues.append("[HATA] EMAIL_HOST ayarlanmamis!")
        print(f"   EMAIL_HOST: [HATA] AYARLANMAMIS")
    else:
        print(f"   EMAIL_HOST: [OK] {email_host}")
    
    # 2. EMAIL_PORT kontrolü
    email_port = getattr(settings, 'EMAIL_PORT', None)
    if not email_port:
        issues.append("[HATA] EMAIL_PORT ayarlanmamis!")
        print(f"   EMAIL_PORT: [HATA] AYARLANMAMIS")
    else:
        print(f"   EMAIL_PORT: [OK] {email_port}")
    
    # 3. EMAIL_HOST_USER kontrolü
    print("\n2. Kimlik Dogrulama Ayarlari:")
    email_user = getattr(settings, 'EMAIL_HOST_USER', None)
    if not email_user or email_user == '':
        issues.append("[HATA] EMAIL_HOST_USER ayarlanmamis!")
        print(f"   EMAIL_HOST_USER: [HATA] AYARLANMAMIS")
    else:
        # Güvenlik için sadece ilk 10 karakteri göster
        masked_user = email_user[:10] + '...' if len(email_user) > 10 else email_user
        print(f"   EMAIL_HOST_USER: [OK] {masked_user}")
    
    # 4. EMAIL_HOST_PASSWORD kontrolü
    email_password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
    if not email_password or email_password == '':
        issues.append("[HATA] EMAIL_HOST_PASSWORD ayarlanmamis!")
        print(f"   EMAIL_HOST_PASSWORD: [HATA] AYARLANMAMIS")
    else:
        print(f"   EMAIL_HOST_PASSWORD: [OK] *** (ayarlanmis)")
    
    # 5. DEFAULT_FROM_EMAIL kontrolü
    print("\n3. Gonderen E-posta Ayarlari:")
    default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    if not default_from or default_from == '':
        issues.append("[HATA] DEFAULT_FROM_EMAIL ayarlanmamis!")
        print(f"   DEFAULT_FROM_EMAIL: [HATA] AYARLANMAMIS")
    else:
        print(f"   DEFAULT_FROM_EMAIL: [OK] {default_from}")
        if email_user and default_from != email_user:
            warnings.append("[UYARI] DEFAULT_FROM_EMAIL, EMAIL_HOST_USER ile ayni degil. Bu bazi SMTP servislerinde sorun yaratabilir.")
    
    # 6. ADMIN_EMAIL kontrolü
    print("\n4. Admin E-posta Ayarlari:")
    admin_emails = [admin[1] for admin in getattr(settings, 'ADMINS', []) if admin[1]]
    if not admin_emails:
        issues.append("[HATA] ADMIN_EMAIL ayarlanmamis! Admin'e bildirim gonderilemez.")
        print(f"   ADMIN_EMAIL: [HATA] AYARLANMAMIS")
    else:
        print(f"   ADMIN_EMAIL: [OK] {', '.join(admin_emails)}")
    
    # 7. TLS/SSL ayarları
    print("\n5. Guvenlik Ayarlari:")
    use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
    use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
    print(f"   EMAIL_USE_TLS: [{'OK' if use_tls else 'HATA'}] {use_tls}")
    print(f"   EMAIL_USE_SSL: [{'OK' if use_ssl else 'HATA'}] {use_ssl}")
    
    if email_port:
        if email_port == 465 and not use_ssl:
            issues.append("[HATA] Port 465 kullaniyorsaniz EMAIL_USE_SSL=True olmali!")
        elif email_port == 587 and not use_tls:
            issues.append("[HATA] Port 587 kullaniyorsaniz EMAIL_USE_TLS=True olmali!")
        elif email_port == 2525 and not use_tls:
            warnings.append("[UYARI] Port 2525 genellikle TLS gerektirir. EMAIL_USE_TLS=True oldugundan emin olun.")
    
    # 8. EMAIL_BACKEND kontrolü
    print("\n6. E-posta Backend:")
    email_backend = getattr(settings, 'EMAIL_BACKEND', None)
    print(f"   EMAIL_BACKEND: {email_backend}")
    
    # 9. SMTP bağlantı testi
    print("\n7. SMTP Baglanti Testi:")
    if email_host and email_port:
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)
            result = test_socket.connect_ex((email_host, email_port))
            test_socket.close()
            
            if result == 0:
                print(f"   Baglanti: [OK] {email_host}:{email_port} erisilebilir")
            else:
                issues.append(f"[HATA] {email_host}:{email_port} portuna baglanilamiyor! (Hata kodu: {result})")
                print(f"   Baglanti: [HATA] {email_host}:{email_port} erisilemiyor (Hata: {result})")
        except socket.gaierror as e:
            issues.append(f"[HATA] DNS hatasi: {email_host} cozumlenemiyor!")
            print(f"   Baglanti: [HATA] DNS hatasi - {email_host} bulunamadi")
        except Exception as e:
            warnings.append(f"[UYARI] Baglanti testi basarisiz: {str(e)}")
            print(f"   Baglanti: [UYARI] Test edilemedi - {str(e)}")
    else:
        warnings.append("[UYARI] EMAIL_HOST veya EMAIL_PORT ayarlanmamis, baglanti testi yapilamadi")
    
    # 10. Django connection testi
    print("\n8. Django E-posta Backend Testi:")
    try:
        conn = get_connection()
        print(f"   Backend: [OK] {type(conn).__name__}")
        if hasattr(conn, 'host'):
            print(f"   Host: {conn.host}")
        if hasattr(conn, 'port'):
            print(f"   Port: {conn.port}")
    except Exception as e:
        issues.append(f"[HATA] Django e-posta backend'i olusturulamadi: {str(e)}")
        print(f"   Backend: [HATA] Hata - {str(e)}")
    
    # Özet
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    
    if issues:
        print("\n[KRITIK SORUNLAR]")
        for issue in issues:
            print(f"   {issue}")
    
    if warnings:
        print("\n[UYARILAR]")
        for warning in warnings:
            print(f"   {warning}")
    
    if not issues and not warnings:
        print("\n[OK] Tum kontroller basarili! E-posta yapılandırması doğru görünüyor.")
        print("\n[IPUCU] Test e-postası göndermek için: python test_email.py")
    else:
        print("\n[IPUCU] Çözüm önerileri:")
        print("   1. .env dosyasını kontrol edin")
        print("   2. EMAIL_HOST_USER ve EMAIL_HOST_PASSWORD doğru mu?")
        print("   3. ElasticEmail/Brevo hesabınızda SMTP ayarlarını kontrol edin")
        print("   4. DEFAULT_FROM_EMAIL adresi doğrulanmış mı?")
    
    return len(issues) == 0

if __name__ == '__main__':
    try:
        success = check_email_config()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[HATA] Script hatasi: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

