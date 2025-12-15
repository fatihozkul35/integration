# E-posta Bounce Sorunları ve Çözümleri

ElasticEmail'de "bounced" (geri dönen) e-postalar genellikle şu nedenlerle olur:

## Yaygın Bounce Nedenleri

### 1. Gönderen E-posta Adresi Doğrulanmamış ⚠️ (EN YAYGIN)

**Sorun:** `DEFAULT_FROM_EMAIL` adresi ElasticEmail hesabınızda doğrulanmamış.

**Çözüm:**
1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **Domains** veya **Settings** > **Verified Senders** bölümüne gidin
3. Gönderen e-posta adresinizi doğrulayın
4. E-posta adresinize gelen doğrulama linkine tıklayın

**Kontrol:**
- `.env` dosyasında `DEFAULT_FROM_EMAIL` adresinin ElasticEmail hesabınızdaki doğrulanmış adreslerden biri olduğundan emin olun

### 2. Geçersiz Alıcı E-posta Adresi

**Sorun:** `ADMIN_EMAIL` adresi geçersiz veya mevcut değil.

**Çözüm:**
- `.env` dosyasında `ADMIN_EMAIL` adresinin doğru olduğundan emin olun
- Test için kendi e-posta adresinizi kullanın
- E-posta adresinin yazım hatası olmadığından emin olun

### 3. SPF/DKIM Ayarları Eksik

**Sorun:** Domain'iniz için SPF ve DKIM kayıtları eksik.

**Çözüm:**
1. ElasticEmail dashboard'unda **Settings** > **Domains** bölümüne gidin
2. Domain'inizi ekleyin ve doğrulayın
3. DNS kayıtlarınızı (SPF, DKIM) ekleyin
4. DNS değişikliklerinin yayılması için 24-48 saat bekleyin

### 4. Spam Olarak İşaretlenmiş

**Sorun:** E-postalar spam olarak algılanıyor.

**Çözüm:**
- E-posta içeriğinizi kontrol edin (spam kelimelerden kaçının)
- HTML template'inizi kontrol edin
- ElasticEmail'de spam skorunuzu kontrol edin

### 5. Hesap Limitleri

**Sorun:** ElasticEmail hesabınızın gönderim limiti dolmuş olabilir.

**Çözüm:**
- ElasticEmail dashboard'unda kalan gönderim limitinizi kontrol edin
- Ücretsiz plan limitlerini kontrol edin

## Hızlı Kontrol Listesi

1. ✅ `.env` dosyasında `DEFAULT_FROM_EMAIL` doğru mu?
2. ✅ `.env` dosyasında `ADMIN_EMAIL` doğru mu?
3. ✅ `DEFAULT_FROM_EMAIL` ElasticEmail'de doğrulanmış mı?
4. ✅ ElasticEmail hesabınız aktif mi?
5. ✅ API anahtarı/şifre doğru mu?
6. ✅ Port ve TLS ayarları doğru mu?

## Debug İçin Kontrol Komutları

### 1. E-posta Ayarlarını Kontrol Et

```bash
python manage.py shell
```

```python
from django.conf import settings

print("=== E-posta Ayarları ===")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
print(f"ADMINS: {settings.ADMINS}")
```

### 2. Test E-postası Gönder

```bash
python manage.py sendtestemail your-email@example.com
```

### 3. Log Dosyalarını Kontrol Et

E-posta gönderim hatalarını görmek için Django loglarını kontrol edin:

```python
# views.py'de logger kullanılıyor
# Hatalar Django log sistemine yazılıyor
```

## ElasticEmail Dashboard'da Kontrol

1. **Campaigns** > **Sent** bölümünde gönderilen e-postaları görün
2. **Campaigns** > **Bounced** bölümünde bounce nedenlerini görün
3. Her bounce için detaylı hata mesajını kontrol edin

## Örnek .env Dosyası

```env
# ElasticEmail SMTP Configuration
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# ÖNEMLİ: Bu adres ElasticEmail'de doğrulanmış olmalı!
EMAIL_HOST_USER=your-verified-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-api-key
DEFAULT_FROM_EMAIL=your-verified-email@yourdomain.com

# Bildirim e-postalarının gönderileceği adres
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_NAME=Admin
```

## En Yaygın Çözüm

**%90 durumda sorun:** `DEFAULT_FROM_EMAIL` adresi ElasticEmail'de doğrulanmamış.

**Hızlı çözüm:**
1. ElasticEmail hesabınıza giriş yapın
2. Gönderen e-posta adresinizi doğrulayın
3. `.env` dosyasında `DEFAULT_FROM_EMAIL` adresinin doğrulanmış adresle aynı olduğundan emin olun

## İletişim

Sorun devam ederse:
- ElasticEmail support ile iletişime geçin
- Bounce detaylarını ElasticEmail dashboard'undan kontrol edin
- Django log dosyalarını kontrol edin

