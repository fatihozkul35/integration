# E-posta Spam Önleme Kılavuzu

E-postalarınızın spam klasörüne düşmemesi için bu kılavuzu takip edin.

## 🔴 Spam'a Düşme Nedenleri

E-postalar genellikle şu nedenlerle spam klasörüne düşer:

1. **SPF/DKIM/DMARC kayıtları eksik** (En önemli)
2. **Gönderen e-posta adresi doğrulanmamış**
3. **E-posta başlıkları eksik veya yanlış**
4. **Domain reputation düşük**
5. **E-posta içeriği spam filtrelerini tetikliyor**

## ✅ Çözüm Adımları

### 1. SPF (Sender Policy Framework) Kaydı Ekleme

SPF kaydı, domain'inizden hangi sunucuların e-posta gönderebileceğini belirtir.

**ElasticEmail için SPF kaydı:**

1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **Domains** bölümüne gidin
3. Domain'inizi ekleyin (eğer eklemediyseniz)
4. ElasticEmail size bir SPF kaydı verecek, örneğin:
   ```
   v=spf1 include:spf.elasticemail.com ~all
   ```
5. Bu kaydı domain DNS ayarlarınıza ekleyin (TXT kaydı olarak)

**DNS Kaydı Örneği:**
```
Type: TXT
Name: @ (veya domain adınız)
Value: v=spf1 include:spf.elasticemail.com ~all
TTL: 3600
```

### 2. DKIM (DomainKeys Identified Mail) Kaydı Ekleme

DKIM, e-postalarınızın gerçekten sizin domain'inizden geldiğini doğrular.

**ElasticEmail için DKIM kaydı:**

1. ElasticEmail dashboard'unda **Settings** > **Domains** bölümüne gidin
2. Domain'inizi seçin
3. DKIM kayıtlarınızı görüntüleyin (genellikle 2-3 kayıt)
4. Bu kayıtları DNS'e ekleyin (TXT kayıtları olarak)

**DNS Kaydı Örneği:**
```
Type: TXT
Name: elasticemail._domainkey (veya ElasticEmail'den verilen isim)
Value: [ElasticEmail'den verilen uzun string]
TTL: 3600
```

### 3. DMARC (Domain-based Message Authentication) Kaydı Ekleme

DMARC, SPF ve DKIM sonuçlarına göre e-postaların nasıl işleneceğini belirtir.

**DMARC kaydı ekleme:**

1. DNS'e aşağıdaki TXT kaydını ekleyin:

```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com; sp=quarantine; aspf=r;
TTL: 3600
```

**DMARC Politikaları:**
- `p=none` - Sadece raporla, e-postayı engelleme
- `p=quarantine` - Şüpheli e-postaları karantinaya al (önerilen başlangıç)
- `p=reject` - Şüpheli e-postaları tamamen reddet (sadece test sonrası)

**Başlangıç için önerilen:**
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; pct=100; ruf=mailto:dmarc@yourdomain.com; fo=1; sp=quarantine; aspf=r;
```

### 4. ElasticEmail'de Domain Doğrulama

1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **Domains** bölümüne gidin
3. Domain'inizi ekleyin
4. DNS kayıtlarınızı (SPF, DKIM) ekleyin
5. ElasticEmail domain'i doğrulayacak (24-48 saat sürebilir)

### 5. Gönderen E-posta Adresini Doğrulama

1. ElasticEmail hesabınıza giriş yapın
2. **Settings** > **Verified Senders** bölümüne gidin
3. Gönderen e-posta adresinizi ekleyin
4. E-posta adresinize gelen doğrulama linkine tıklayın
5. `.env` dosyasında `DEFAULT_FROM_EMAIL` adresinin doğrulanmış adresle aynı olduğundan emin olun

### 6. E-posta İçeriği İyileştirmeleri

✅ **Yapılması Gerekenler:**
- Düzgün HTML yapısı kullanın
- Text ve HTML versiyonlarını birlikte gönderin
- Spam kelimelerden kaçının (FREE, CLICK HERE, vb.)
- Görsel/ağırlık oranını dengeli tutun
- Link'leri açık ve anlaşılır yapın

❌ **Yapılmaması Gerekenler:**
- Tüm büyük harflerle yazmayın
- Çok fazla ünlem işareti kullanmayın (!!!)
- "Spam" kelimesini içermeyin
- Çok fazla link eklemeyin
- Şüpheli URL'ler kullanmayın

## 🔍 DNS Kayıtlarını Kontrol Etme

DNS kayıtlarınızın doğru eklendiğini kontrol etmek için:

### Online Araçlar:
- **MXToolbox**: https://mxtoolbox.com/spf.aspx
- **DMARC Analyzer**: https://www.dmarcanalyzer.com/
- **DKIM Validator**: https://www.dmarcanalyzer.com/dkim-check/

### Komut Satırı ile Kontrol:

**SPF Kontrolü:**
```bash
nslookup -type=TXT yourdomain.com
```

**DKIM Kontrolü:**
```bash
nslookup -type=TXT elasticemail._domainkey.yourdomain.com
```

**DMARC Kontrolü:**
```bash
nslookup -type=TXT _dmarc.yourdomain.com
```

## 📊 E-posta Deliverability Testi

E-postalarınızın spam skorunu test etmek için:

1. **Mail-Tester**: https://www.mail-tester.com/
   - Test e-postası gönderin
   - Spam skorunuzu görün (10/10 hedefleyin)

2. **GlockApps**: https://glockapps.com/
   - Farklı e-posta sağlayıcılarında test edin

3. **ElasticEmail Dashboard**:
   - Gönderim istatistiklerinizi kontrol edin
   - Bounce ve spam şikayetlerini izleyin

## 🛠️ Kod İyileştirmeleri (Yapıldı)

Aşağıdaki iyileştirmeler kodda yapıldı:

✅ **Reply-To header eklendi** - Admin direkt kullanıcıya cevap verebilir
✅ **Uygun e-posta başlıkları eklendi** - X-Mailer, Importance, vb.
✅ **Subject line iyileştirildi** - Türkçe karakterler yerine Almanca kullanıldı

## 📝 Kontrol Listesi

E-postalarınızın spam'a düşmemesi için:

- [ ] SPF kaydı DNS'e eklendi ve doğrulandı
- [ ] DKIM kayıtları DNS'e eklendi ve doğrulandı
- [ ] DMARC kaydı DNS'e eklendi
- [ ] Domain ElasticEmail'de doğrulandı
- [ ] Gönderen e-posta adresi ElasticEmail'de doğrulandı
- [ ] `.env` dosyasında `DEFAULT_FROM_EMAIL` doğru
- [ ] DNS kayıtları yayıldı (24-48 saat beklendi)
- [ ] Mail-Tester ile test edildi (skor 8+/10)
- [ ] E-posta içeriği spam kelimeler içermiyor

## 🚨 Acil Durum Çözümleri

### E-postalar hala spam'a düşüyorsa:

1. **DNS kayıtlarını tekrar kontrol edin**
   - SPF, DKIM, DMARC kayıtlarının doğru eklendiğinden emin olun
   - DNS propagation için 24-48 saat bekleyin

2. **ElasticEmail reputation kontrolü**
   - ElasticEmail dashboard'unda domain reputation'unuzu kontrol edin
   - Bounce oranınızı düşük tutun (%2'nin altında)

3. **E-posta gönderim sıklığı**
   - Çok fazla e-posta göndermeyin
   - Rate limiting uygulayın

4. **E-posta içeriğini gözden geçirin**
   - Mail-Tester ile test edin
   - Spam kelimeleri kaldırın

5. **Warm-up süreci**
   - Yeni domain/hesap için günde az sayıda e-posta göndererek başlayın
   - Zamanla gönderim hacmini artırın

## 📞 Destek

Sorun devam ederse:
- ElasticEmail Support: https://elasticemail.com/support/
- DNS sağlayıcınızın destek ekibi
- Mail-Tester sonuçlarını paylaşın

## 🔗 Faydalı Linkler

- [ElasticEmail Domain Setup](https://elasticemail.com/support/account-management/domain-authentication/)
- [SPF Record Syntax](https://www.ietf.org/rfc/rfc4408.txt)
- [DKIM Overview](https://dkim.org/)
- [DMARC Guide](https://dmarc.org/wiki/FAQ)

