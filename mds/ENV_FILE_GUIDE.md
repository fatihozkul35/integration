# .env Dosyası Yapılandırma Kılavuzu

Bu kılavuz, projeniz için `.env` dosyasını nasıl yapılandıracağınızı açıklar.

## .env Dosyası Nedir?

`.env` dosyası, hassas bilgileri (şifreler, API anahtarları vb.) ve ortam değişkenlerini saklamak için kullanılır. Bu dosya **asla** Git'e commit edilmemelidir!

## Dosya Konumu

`.env` dosyası proje kök dizininde olmalıdır:
```
integration/
├── .env              ← Buraya
├── manage.py
├── integration_app/
└── integration_project/
```

## Minimum Gerekli Ayarlar

### 1. Django Temel Ayarları

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. E-posta Yapılandırması (ElasticEmail)

```env
# SMTP Sunucu
EMAIL_HOST=smtp.elasticemail.com

# Port Ayarları
# Local için:
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# PythonAnywhere için:
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_USE_SSL=False

# Kimlik Bilgileri
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-api-key-or-password

# Gönderen Adres
DEFAULT_FROM_EMAIL=your-email@example.com
SERVER_EMAIL=your-email@example.com
```

### 3. Admin Ayarları

```env
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com
```

## Local Geliştirme İçin Tam Örnek

```env
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-1234567890
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ElasticEmail SMTP Configuration
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=maske.dali27122019@gmail.com
EMAIL_HOST_PASSWORD=your-elasticemail-api-key
DEFAULT_FROM_EMAIL=maske.dali27122019@gmail.com
SERVER_EMAIL=maske.dali27122019@gmail.com

# Admin Settings
ADMIN_NAME=Admin
ADMIN_EMAIL=maske.dali27122019@gmail.com

# Email Settings
SEND_USER_CONFIRMATION_EMAIL=False
```

## PythonAnywhere İçin Tam Örnek

```env
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-1234567890
DEBUG=False
ALLOWED_HOSTS=msinternational.pythonanywhere.com

# ElasticEmail SMTP Configuration - PythonAnywhere için port 587 kullanın!
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=maske.dali27122019@gmail.com
EMAIL_HOST_PASSWORD=your-elasticemail-api-key
DEFAULT_FROM_EMAIL=maske.dali27122019@gmail.com
SERVER_EMAIL=maske.dali27122019@gmail.com

# Admin Settings
ADMIN_NAME=Admin
ADMIN_EMAIL=maske.dali27122019@gmail.com

# Email Settings
SEND_USER_CONFIRMATION_EMAIL=False
```

## Önemli Notlar

### 1. Port Ayarları

- **Local**: Port `2525` kullanabilirsiniz
- **PythonAnywhere**: Port `587` (TLS) veya `465` (SSL) kullanmalısınız
- **Port 2525 PythonAnywhere'de ÇALIŞMAZ!**

### 2. ElasticEmail API Anahtarı

`EMAIL_HOST_PASSWORD` için ElasticEmail'den aldığınız API anahtarını kullanın:
1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **SMTP Settings** bölümüne gidin
3. API anahtarınızı kopyalayın

### 3. Gönderen E-posta Adresi Doğrulama

`DEFAULT_FROM_EMAIL` adresinin ElasticEmail'de doğrulanmış olması gerekir:
1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **Verified Senders** veya **Domains** bölümüne gidin
3. E-posta adresinizi doğrulayın

### 4. Güvenlik

- `.env` dosyasını **asla** Git'e commit etmeyin
- `.gitignore` dosyasında `.env` olduğundan emin olun
- Production'da `DEBUG=False` kullanın
- `SECRET_KEY`'i güçlü ve benzersiz yapın

## .env Dosyası Oluşturma

### Windows'ta:

1. Proje kök dizininde `.env` dosyası oluşturun
2. Notepad veya başka bir metin editörü ile açın
3. Yukarıdaki örnekleri kopyalayıp kendi bilgilerinizle doldurun

### Linux/Mac'ta:

```bash
cd /path/to/integration
nano .env
# veya
vim .env
```

### PythonAnywhere'de:

1. PythonAnywhere konsoluna giriş yapın
2. Proje dizininize gidin:
   ```bash
   cd /home/msinternational/integration
   ```
3. `.env` dosyasını oluşturun:
   ```bash
   nano .env
   ```
4. Ayarları ekleyin ve kaydedin (Ctrl+X, Y, Enter)

## Kontrol Listesi

- [ ] `.env` dosyası proje kök dizininde
- [ ] `SECRET_KEY` ayarlanmış
- [ ] `EMAIL_HOST` doğru (smtp.elasticemail.com)
- [ ] `EMAIL_PORT` doğru (Local: 2525, PythonAnywhere: 587)
- [ ] `EMAIL_USE_TLS` doğru (True)
- [ ] `EMAIL_HOST_USER` ElasticEmail hesabınız
- [ ] `EMAIL_HOST_PASSWORD` API anahtarınız
- [ ] `DEFAULT_FROM_EMAIL` ElasticEmail'de doğrulanmış
- [ ] `ADMIN_EMAIL` ayarlanmış
- [ ] `.env` dosyası `.gitignore`'da

## Sorun Giderme

### E-posta gönderilmiyor

1. `.env` dosyasının doğru konumda olduğundan emin olun
2. PythonAnywhere'de **Reload** yapın
3. Port ayarını kontrol edin (PythonAnywhere için 587)
4. ElasticEmail API anahtarınızı kontrol edin
5. `DEFAULT_FROM_EMAIL` adresinin doğrulanmış olduğundan emin olun

### "Settings not found" hatası

- `.env` dosyasının proje kök dizininde olduğundan emin olun
- Dosya adının tam olarak `.env` olduğundan emin olun (`.env.txt` değil!)

### PythonAnywhere'de çalışmıyor

- Port 587 kullandığınızdan emin olun
- PythonAnywhere Web tab'ında **Reload** yapın
- Environment variables'ı kontrol edin

## Örnek .env Dosyası

Tam bir örnek için `.env.example` dosyasına bakın. Bu dosyayı kopyalayıp `.env` olarak kaydedebilirsiniz:

```bash
# Windows'ta:
copy .env.example .env

# Linux/Mac'ta:
cp .env.example .env
```

Sonra `.env` dosyasını açıp kendi bilgilerinizle doldurun.



