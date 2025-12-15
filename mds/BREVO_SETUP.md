# Brevo E-posta Yapılandırma Kılavuzu

Bu proje Brevo (eski adıyla Sendinblue) SMTP servisi kullanarak e-posta gönderimi için yapılandırılmıştır.

## Brevo Hakkında

Brevo, güvenilir ve kullanıcı dostu bir e-posta gönderim servisidir. Ücretsiz plan ile günde 300 e-posta gönderebilirsiniz.

**Avantajları:**
- ✅ Ücretsiz plan: 300 e-posta/gün
- ✅ Kolay kurulum
- ✅ İyi deliverability (spam'a düşme riski düşük)
- ✅ Analytics ve raporlama
- ✅ API erişimi

## Kurulum Adımları

### 1. Brevo Hesabı Oluşturma

1. [Brevo](https://www.brevo.com) web sitesine gidin
2. Ücretsiz hesap oluşturun
3. E-posta adresinizi doğrulayın

### 2. SMTP Ayarlarını Alma

1. Brevo hesabınıza giriş yapın
2. **SMTP & API** > **SMTP** bölümüne gidin
3. **SMTP Server**: `smtp-relay.brevo.com`
4. **Port**: `587` (TLS) veya `465` (SSL)
5. **SMTP Login**: E-posta adresiniz (örnek: `your-email@example.com`)
6. **SMTP Key**: SMTP şifrenizi oluşturun veya mevcut şifrenizi kullanın

**Önemli:** SMTP Key'i kopyalayın, bu şifre olarak kullanılacak.

### 3. Ortam Değişkenlerini Ayarlayın

Proje kök dizininde `.env` dosyası oluşturun veya mevcut dosyayı güncelleyin:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Brevo SMTP Configuration
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-smtp-key-from-brevo
DEFAULT_FROM_EMAIL=your-email@example.com
SERVER_EMAIL=your-email@example.com

# Admin Settings
# Contact formu bildirimleri bu adrese gönderilir
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com

# Email sending settings
SEND_USER_CONFIRMATION_EMAIL=True
```

### 4. Port Seçenekleri

Brevo için farklı port seçenekleri:

**Port 587 (TLS) - Önerilen**
```env
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

**Port 465 (SSL) - Alternatif**
```env
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

## Gönderen E-posta Adresini Doğrulama

1. Brevo hesabınıza giriş yapın
2. **Senders** > **Add a sender** bölümüne gidin
3. Gönderen e-posta adresinizi ekleyin
4. E-posta adresinize gelen doğrulama linkine tıklayın
5. `.env` dosyasında `DEFAULT_FROM_EMAIL` adresinin doğrulanmış adresle aynı olduğundan emin olun

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
    subject='HTML Test',
    body='Düz metin içerik',
    from_email='from@example.com',
    to=['to@example.com'],
)
msg.attach_alternative('<html><body><h1>HTML Test</h1></body></html>', "text/html")
msg.send()
```

## Test Etme

### 1. Django Built-in Test Komutu

```bash
python manage.py sendtestemail test@example.com
```

### 2. Django Shell ile Test

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Test E-postası',
    message='Bu bir test e-postasıdır.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['test@example.com'],
    fail_silently=False,
)
```

## Yaygın Sorunlar ve Çözümleri

### 1. "SMTPAuthenticationError"

**Sorun:** SMTP kullanıcı adı veya şifre yanlış.

**Çözüm:**
- `.env` dosyasında `EMAIL_HOST_USER` ve `EMAIL_HOST_PASSWORD` doğru mu kontrol edin
- Brevo'da SMTP Key'inizi kontrol edin
- SMTP Login'in e-posta adresiniz olduğundan emin olun

### 2. "Connection refused" veya "Timeout"

**Sorun:** SMTP sunucusuna bağlanılamıyor.

**Çözüm:**
- Port numarasını kontrol edin (587 veya 465)
- Firewall ayarlarını kontrol edin
- TLS/SSL ayarlarını kontrol edin
- İnternet bağlantınızı kontrol edin

### 3. E-posta gönderiliyor ama gelmiyor

**Sorun:** E-posta spam klasörüne düşüyor veya gönderilmiyor.

**Çözüm:**
- Gönderen e-posta adresinin Brevo'da doğrulandığından emin olun
- SPF/DKIM/DMARC kayıtlarını kontrol edin (domain kullanıyorsanız)
- Brevo dashboard'unda gönderim istatistiklerini kontrol edin

### 4. "Sender address not verified"

**Sorun:** Gönderen e-posta adresi Brevo'da doğrulanmamış.

**Çözüm:**
1. Brevo hesabınıza giriş yapın
2. **Senders** bölümüne gidin
3. Gönderen e-posta adresinizi doğrulayın
4. E-posta adresinize gelen doğrulama linkine tıklayın

## Brevo Limitleri

### Ücretsiz Plan
- **Günlük limit**: 300 e-posta/gün
- **Aylık limit**: 9,000 e-posta/ay
- **Gönderim hızı**: Saniyede 1 e-posta

### Ücretli Planlar
Daha yüksek limitler için Brevo'nun ücretli planlarını inceleyin:
- [Brevo Pricing](https://www.brevo.com/pricing/)

## SPF/DKIM/DMARC Ayarları (Domain Kullanıyorsanız)

Eğer kendi domain'inizi kullanıyorsanız, spam önleme için DNS kayıtları eklemeniz gerekir:

### SPF Kaydı

```
Type: TXT
Name: @
Value: v=spf1 include:spf.brevo.com ~all
```

### DKIM Kaydı

1. Brevo hesabınıza giriş yapın
2. **Senders** > **Domains** bölümüne gidin
3. Domain'inizi ekleyin
4. Brevo size DKIM kayıtlarını verecek
5. Bu kayıtları DNS'e ekleyin

### DMARC Kaydı

```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com; sp=quarantine; aspf=r;
```

## Brevo Dashboard'da Kontrol

1. **Statistics** bölümünde gönderim istatistiklerinizi görün
2. **Logs** bölümünde gönderilen e-postaları görün
3. **Bounces** bölümünde bounce nedenlerini görün

## Örnek .env Dosyası

```env
# Brevo SMTP Configuration
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# ÖNEMLİ: Bu adres Brevo'da doğrulanmış olmalı!
EMAIL_HOST_USER=your-verified-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-smtp-key-from-brevo
DEFAULT_FROM_EMAIL=your-verified-email@yourdomain.com

# Bildirim e-postalarının gönderileceği adres
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_NAME=Admin

# Email sending settings
SEND_USER_CONFIRMATION_EMAIL=True
```

## Faydalı Linkler

- [Brevo Ana Sayfa](https://www.brevo.com)
- [Brevo SMTP Dokümantasyonu](https://developers.brevo.com/docs/send-emails-with-smtp)
- [Brevo API Dokümantasyonu](https://developers.brevo.com/)
- [Brevo Pricing](https://www.brevo.com/pricing/)

## ElasticEmail'den Geçiş

Eğer ElasticEmail'den Brevo'ya geçiyorsanız:

1. ✅ `settings.py` dosyası zaten güncellendi
2. ✅ Brevo hesabı oluşturun
3. ✅ `.env` dosyasını Brevo ayarlarına göre güncelleyin
4. ✅ Gönderen e-posta adresini Brevo'da doğrulayın
5. ✅ Test e-postası gönderin

## Notlar

- Brevo ücretsiz plan ile günde 300 e-posta gönderebilirsiniz
- Gönderen e-posta adresi mutlaka Brevo'da doğrulanmış olmalı
- Domain kullanıyorsanız SPF/DKIM/DMARC kayıtlarını ekleyin
- Brevo dashboard'unda gönderim istatistiklerinizi takip edin

