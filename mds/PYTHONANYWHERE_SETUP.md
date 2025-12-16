# PythonAnywhere E-posta Yapılandırma Kılavuzu

PythonAnywhere'de e-posta gönderimi için özel yapılandırma gereklidir çünkü PythonAnywhere SMTP port kısıtlamaları vardır.

## Önemli: Port Kısıtlamaları

PythonAnywhere **sadece port 587 ve 465'e izin verir**. Port 2525 çalışmaz!

- ✅ Port 587 (TLS) - **Önerilen**
- ✅ Port 465 (SSL) - Alternatif
- ❌ Port 2525 - **ÇALIŞMAZ**

## Otomatik Port Ayarlama

Proje PythonAnywhere'de otomatik olarak port 587'ye geçer. Ancak `.env` dosyasında manuel olarak da ayarlayabilirsiniz.

## PythonAnywhere'de .env Dosyası Ayarları

PythonAnywhere'de `.env` dosyanızı şu şekilde yapılandırın:

### ElasticEmail için:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=msinternational.pythonanywhere.com

# ElasticEmail SMTP Configuration - PythonAnywhere için port 587 kullanın
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-elasticemail-account@example.com
EMAIL_HOST_PASSWORD=your-elasticemail-api-key-or-password
DEFAULT_FROM_EMAIL=your-elasticemail-account@example.com
SERVER_EMAIL=your-elasticemail-account@example.com

# Admin Settings
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com

# Email sending settings
SEND_USER_CONFIRMATION_EMAIL=False
```

### Alternatif: Port 465 (SSL) kullanmak isterseniz:

```env
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

## PythonAnywhere'de .env Dosyasını Oluşturma

1. PythonAnywhere konsoluna giriş yapın
2. Proje dizininize gidin:
   ```bash
   cd /home/yourusername/path/to/your/project
   ```
3. `.env` dosyasını oluşturun:
   ```bash
   nano .env
   ```
4. Yukarıdaki ayarları ekleyin ve kaydedin (Ctrl+X, Y, Enter)

## PythonAnywhere'de Environment Variables Kullanma

Alternatif olarak, PythonAnywhere Web tab'ında **Environment variables** bölümünden de ayarlayabilirsiniz:

1. PythonAnywhere dashboard'a giriş yapın
2. **Web** tab'ına gidin
3. **Environment variables** bölümünü bulun
4. Her bir değişkeni ekleyin:
   - `EMAIL_HOST=smtp.elasticemail.com`
   - `EMAIL_PORT=587`
   - `EMAIL_USE_TLS=True`
   - `EMAIL_USE_SSL=False`
   - `EMAIL_HOST_USER=your-email@example.com`
   - `EMAIL_HOST_PASSWORD=your-password`
   - `DEFAULT_FROM_EMAIL=your-email@example.com`
   - `ADMIN_EMAIL=admin@example.com`
   - vb.

## Test Etme

PythonAnywhere konsolunda test edin:

```bash
cd /home/yourusername/path/to/your/project
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

# Test e-postası gönder
send_mail(
    subject='Test E-postası',
    message='Bu bir test e-postasıdır.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['test@example.com'],
    fail_silently=False,
)
```

## Yaygın Sorunlar

### 1. "Connection refused" veya "Timeout"

**Sorun:** Port 2525 kullanıyorsunuz.

**Çözüm:** `.env` dosyasında `EMAIL_PORT=587` olarak ayarlayın.

### 2. "SMTPAuthenticationError"

**Sorun:** Kimlik bilgileri yanlış veya `.env` dosyası yüklenmemiş.

**Çözüm:**
- `.env` dosyasının doğru konumda olduğundan emin olun
- PythonAnywhere Web tab'ında **Reload** butonuna tıklayın
- Environment variables'ı kontrol edin

### 3. E-posta gönderilmiyor ama hata yok

**Sorun:** `.env` dosyası yüklenmemiş olabilir.

**Çözüm:**
- PythonAnywhere Web tab'ında **Reload** butonuna tıklayın
- Konsolda `python manage.py shell` ile ayarları kontrol edin:
  ```python
  from django.conf import settings
  print(settings.EMAIL_PORT)  # 587 olmalı
  ```

## PythonAnywhere'de Reload

Her `.env` dosyası değişikliğinden sonra:

1. PythonAnywhere dashboard'a gidin
2. **Web** tab'ına gidin
3. **Reload** butonuna tıklayın

## Otomatik Tespit

Proje otomatik olarak PythonAnywhere'de çalıştığını tespit eder ve port 587'ye geçer. Ancak manuel olarak da ayarlayabilirsiniz:

```env
ON_PYTHONANYWHERE=True
```

## ElasticEmail Port Seçenekleri (PythonAnywhere için)

### Port 587 (TLS) - Önerilen ✅
```env
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

### Port 465 (SSL) - Alternatif
```env
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

## Kontrol Listesi

- [ ] `.env` dosyası PythonAnywhere'de oluşturuldu
- [ ] `EMAIL_PORT=587` veya `EMAIL_PORT=465` ayarlandı
- [ ] Port 2525 kullanılmıyor
- [ ] `EMAIL_HOST_USER` ve `EMAIL_HOST_PASSWORD` doğru
- [ ] `DEFAULT_FROM_EMAIL` ElasticEmail'de doğrulanmış
- [ ] PythonAnywhere Web tab'ında **Reload** yapıldı
- [ ] Test e-postası gönderildi ve başarılı oldu

