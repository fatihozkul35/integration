#!/usr/bin/env python
"""
E-posta gönderimini test etmek için basit bir script.
Kullanım: python test_email.py
"""
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integration_project.settings')
django.setup()

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def test_simple_email():
    """Basit bir test e-postası gönderir"""
    print("=" * 50)
    print("E-posta Gönderim Testi")
    print("=" * 50)
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 50)
    
    # Test e-postası gönder
    recipient = input("\nTest e-postasını göndermek istediğiniz e-posta adresini girin: ").strip()
    
    if not recipient:
        print("❌ E-posta adresi girilmedi!")
        return
    
    try:
        result = send_mail(
            subject='Test E-postası - ElasticEmail',
            message='Bu bir test e-postasıdır. E-posta yapılandırmanız çalışıyor! 🎉',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        if result:
            print(f"\n✅ E-posta başarıyla gönderildi! ({recipient})")
        else:
            print(f"\n❌ E-posta gönderilemedi.")
            
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")
        print("\nKontrol edin:")
        print("1. .env dosyasında EMAIL_HOST_USER ve EMAIL_HOST_PASSWORD doğru mu?")
        print("2. ElasticEmail hesabınız aktif mi?")
        print("3. API anahtarınız doğru mu?")

def test_html_email():
    """HTML içerikli test e-postası gönderir"""
    from django.core.mail import EmailMultiAlternatives
    
    recipient = input("\nHTML test e-postasını göndermek istediğiniz e-posta adresini girin: ").strip()
    
    if not recipient:
        print("❌ E-posta adresi girilmedi!")
        return
    
    try:
        msg = EmailMultiAlternatives(
            subject='HTML Test E-postası - ElasticEmail',
            body='Bu bir HTML test e-postasıdır. HTML görünümü için HTML formatını destekleyen bir e-posta istemcisi kullanın.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        
        html_content = """
        <html>
            <body>
                <h2 style="color: #4CAF50;">✅ E-posta Yapılandırması Başarılı!</h2>
                <p>Bu bir <strong>HTML test e-postasıdır</strong>.</p>
                <p>ElasticEmail yapılandırmanız çalışıyor! 🎉</p>
                <hr>
                <p style="color: #666; font-size: 12px;">Bu e-posta Django ve ElasticEmail kullanılarak gönderilmiştir.</p>
            </body>
        </html>
        """
        
        msg.attach_alternative(html_content, "text/html")
        result = msg.send()
        
        if result:
            print(f"\n✅ HTML e-posta başarıyla gönderildi! ({recipient})")
        else:
            print(f"\n❌ HTML e-posta gönderilemedi.")
            
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")

if __name__ == '__main__':
    print("\nE-posta Test Seçenekleri:")
    print("1. Basit metin e-postası gönder")
    print("2. HTML e-postası gönder")
    print("3. Her ikisini de gönder")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    
    if choice == '1':
        test_simple_email()
    elif choice == '2':
        test_html_email()
    elif choice == '3':
        test_simple_email()
        test_html_email()
    else:
        print("❌ Geçersiz seçim!")

