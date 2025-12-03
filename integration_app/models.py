from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="İsim",
        help_text="İletişime geçen kişinin adı (isteğe bağlı)"
    )
    email = models.EmailField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="E-Posta",
        help_text="E-posta adresi (isteğe bağlı)"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telefon",
        help_text="Telefon numarası (isteğe bağlı)"
    )
    message = models.TextField(
        blank=True,
        verbose_name="Mesaj",
        help_text="Mesaj içeriği (isteğe bağlı)"
    )
    consent = models.BooleanField(
        default=False,
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
