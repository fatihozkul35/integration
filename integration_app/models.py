from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ad Soyad",
        help_text="İletişime geçen kişinin adı (isteğe bağlı)"
    )
    age = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Yaş",
        help_text="Yaş bilgisi"
    )
    marital_status = models.CharField(
        max_length=20,
        choices=[('bekar', 'Bekar'), ('evli', 'Evli')],
        blank=False,
        verbose_name="Medeni Durum",
        help_text="Medeni durum"
    )
    children_count = models.IntegerField(
        default=0,
        blank=False,
        verbose_name="Çocuk Sayısı",
        help_text="Çocuk sayısı"
    )
    driving_license = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Sürücü Belgesi Sınıfı",
        help_text="Sürücü belgesi sınıfı"
    )
    profession = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Meslek",
        help_text="Meslek bilgisi"
    )
    graduation = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Mezuniyet",
        help_text="Mezuniyet bilgisi"
    )
    email = models.EmailField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="E-Posta",
        help_text="E-posta adresi"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="İrtibat Numarası",
        help_text="Telefon numarası (isteğe bağlı)"
    )
    message = models.TextField(
        blank=True,
        verbose_name="Mesaj",
        help_text="Mesaj içeriği"
    )
    consent = models.BooleanField(
        default=False,
        blank=False,
        verbose_name="Onay",
        help_text="Veri işleme onayı"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma tarihi",
        help_text="Mesajın oluşturulduğu tarih ve saat"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Okundu",
        help_text="Mesajın okunup okunmadığı"
    )

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        name_display = self.name if self.name else "Anonym"
        return f"{name_display} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class SliderImage(models.Model):
    """Model to store slider images for the homepage"""
    image = models.ImageField(
        upload_to='slider/',
        verbose_name="Görsel",
        help_text="Slider görseli"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık",
        help_text="Slider başlığı"
    )
    description = models.TextField(
        verbose_name="Açıklama",
        help_text="Slider açıklaması"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Sıralama",
        help_text="Görsellerin gösterim sırası (küçük sayı önce gösterilir)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif",
        help_text="Bu görsel slider'da gösterilsin mi?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma tarihi",
        help_text="Görselin oluşturulduğu tarih ve saat"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncellenme tarihi",
        help_text="Görselin son güncellendiği tarih ve saat"
    )

    class Meta:
        verbose_name = "Slider Görseli"
        verbose_name_plural = "Slider Görselleri"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} (Sıra: {self.order})"