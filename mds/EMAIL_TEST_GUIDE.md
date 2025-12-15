# E-posta Gönderim Test Kılavuzu

Bu kılavuz, ElasticEmail yapılandırmanızı test etmek için farklı yöntemler sunar.

## Hızlı Test Yöntemleri

### 1. Django Built-in Test Komutu (En Kolay)

Django'nun kendi test komutunu kullanarak hızlıca test edebilirsiniz:

```bash
# Tek bir e-posta adresine test gönder
python manage.py sendtestemail test@example.com

# Birden fazla e-posta adresine gönder
python manage.py sendtestemail test1@example.com test2@example.com

# Makefile ile (daha kolay)
make sendtestemail EMAIL=test@example.com
```

### 2. İnteraktif Test Scripti

Projede hazır bir test scripti var:

```bash
python test_email.py
```

veya makefile ile:

```bash
make testemail
```

Bu script size şu seçenekleri sunar:
- Basit metin e-postası gönderme
- HTML e-postası gönderme
- Her ikisini birden gönderme

### 3. Django Shell ile Test

Django shell'i kullanarak manuel test yapabilirsiniz:

```bash
python manage.py shell
```

Shell'de şu komutları çalıştırın:

```python
from django.core.mail import send_mail
from django.conf import settings

# Basit test e-postası
send_mail(
    subject='Test E-postası',
    message='Bu bir test e-postasıdır.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['test@example.com'],
    fail_silently=False,
)

# HTML e-posta testi
from django.core.mail import EmailMultiAlternatives

msg = EmailMultiAlternatives(
    subject='HTML Test',
    body='Düz metin içerik',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['test@example.com'],
)
msg.attach_alternative('<html><body><h1>HTML Test</h1></body></html>', "text/html")
msg.send()
```

### 4. Console Backend ile Test (Geliştirme İçin)

Gerçek e-posta göndermeden, e-postaları konsola yazdırmak için:

`settings.py` dosyasında geçici olarak şunu değiştirin:

```python
# Test için - e-postalar konsola yazdırılır
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Sonra normal şekilde e-posta göndermeyi deneyin. E-postalar konsola yazdırılacaktır.

**Not:** Test bitince tekrar SMTP backend'e dönmeyi unutmayın!

### 5. File Backend ile Test

E-postaları dosyaya kaydetmek için:

```python
# settings.py'de geçici olarak
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  # E-postalar bu klasöre kaydedilir
```

## Yapılandırma Kontrolü

E-posta ayarlarınızı kontrol etmek için:

```python
python manage.py shell
```

```python
from django.conf import settings

print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
```

## Yaygın Hatalar ve Çözümleri

### 1. "SMTPAuthenticationError"

**Sorun:** Kullanıcı adı veya şifre yanlış.

**Çözüm:**
- `.env` dosyasında `EMAIL_HOST_USER` ve `EMAIL_HOST_PASSWORD` doğru mu kontrol edin
- ElasticEmail hesabınızda SMTP şifresini kontrol edin
- API anahtarı kullanıyorsanız doğru anahtarı kullandığınızdan emin olun

### 2. "Connection refused" veya "Timeout"

**Sorun:** SMTP sunucusuna bağlanılamıyor.

**Çözüm:**
- Port numarasını kontrol edin (2525, 587 veya 465)
- Firewall ayarlarını kontrol edin
- TLS/SSL ayarlarını kontrol edin
- İnternet bağlantınızı kontrol edin

### 3. "SSL: CERTIFICATE_VERIFY_FAILED"

**Sorun:** SSL sertifika doğrulama hatası.

**Çözüm:**
- `EMAIL_USE_TLS` ve `EMAIL_USE_SSL` ayarlarını kontrol edin
- Port 465 için `EMAIL_USE_SSL=True` olmalı
- Port 587 için `EMAIL_USE_TLS=True` olmalı

### 4. E-posta gönderiliyor ama gelmiyor

**Sorun:** E-posta spam klasörüne düşüyor veya gönderilmiyor.

**Çözüm:**
- Spam klasörünü kontrol edin
- ElasticEmail hesabınızda gönderim limitlerini kontrol edin
- Gönderen e-posta adresinin doğru olduğundan emin olun
- ElasticEmail dashboard'unda gönderim loglarını kontrol edin

## Production Test Önerileri

1. **Önce test ortamında deneyin** - Gerçek kullanıcılara göndermeden önce
2. **Küçük bir test grubuyla başlayın** - Birkaç e-posta adresiyle test edin
3. **ElasticEmail dashboard'unu izleyin** - Gönderim istatistiklerini takip edin
4. **Spam skorunu kontrol edin** - E-postalarınızın spam olarak işaretlenmediğinden emin olun

## İpuçları

- Geliştirme sırasında `console` backend kullanarak e-postaları konsola yazdırabilirsiniz
- Production'da mutlaka gerçek SMTP backend kullanın
- `.env` dosyasını asla Git'e commit etmeyin
- E-posta gönderim hatalarını loglamak için Django'nun logging sistemini kullanın

