# ElasticEmail Yapılandırma Kılavuzu

Bu proje ElasticEmail SMTP servisi kullanarak e-posta gönderimi için yapılandırılmıştır.

## Kurulum Adımları

### 1. Gerekli Paketi Yükleyin

```bash
pip install -r requirements.txt
```

**Not:** Bu proje `python-decouple` kütüphanesini kullanarak ortam değişkenlerini yönetir.

### 2. ElasticEmail Hesabı Ayarları

1. [ElasticEmail](https://elasticemail.com) hesabınıza giriş yapın
2. **Settings** > **SMTP Settings** bölümüne gidin
3. SMTP bilgilerinizi ve API anahtarınızı alın

### 3. Ortam Değişkenlerini Ayarlayın

Proje kök dizininde `.env` dosyası oluşturun ve aşağıdaki değişkenleri ekleyin:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ElasticEmail SMTP Configuration
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-elasticemail-account@example.com
EMAIL_HOST_PASSWORD=your-elasticemail-api-key-or-password
DEFAULT_FROM_EMAIL=your-elasticemail-account@example.com
SERVER_EMAIL=your-elasticemail-account@example.com

# Admin Settings
# Contact formu bildirimleri bu adrese gönderilir
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com
```

### 4. Port Seçenekleri

ElasticEmail için farklı port seçenekleri:

**Port 2525 (Önerilen - Standart SMTP)**
```env
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

**Port 587 (TLS)**
```env
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

**Port 465 (SSL)**
```env
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

## Kullanım

### Django'da E-posta Gönderme

```python
from django.core.mail import send_mail

send_mail(
    'Konu',
    'E-posta içeriği',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

### HTML E-posta Gönderme

```python
from django.core.mail import EmailMultiAlternatives

msg = EmailMultiAlternatives(
    subject='Konu',
    body='Düz metin içerik',
    from_email='from@example.com',
    to=['to@example.com'],
)
msg.attach_alternative('<html>HTML içerik</html>', "text/html")
msg.send()
```

## Test Etme

E-posta yapılandırmasını test etmek için:

```bash
python manage.py sendtestemail admin@example.com
```

## Güvenlik Notları

- `.env` dosyasını asla Git'e commit etmeyin
- `.env` dosyasını `.gitignore` dosyasına ekleyin
- Production ortamında `DEBUG=False` kullanın
- API anahtarlarınızı güvende tutun

## Sorun Giderme

### E-posta gönderilemiyor

1. ElasticEmail hesabınızın aktif olduğundan emin olun
2. API anahtarınızın doğru olduğunu kontrol edin
3. Port ve TLS/SSL ayarlarının doğru olduğunu kontrol edin
4. Firewall ayarlarınızı kontrol edin

### Bağlantı hatası

- Port 2525, 587 veya 465'ün açık olduğundan emin olun
- TLS/SSL ayarlarını kontrol edin
- ElasticEmail SMTP sunucusunun erişilebilir olduğundan emin olun

