from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Name"),
        help_text=_("Name of the person contacting (optional)")
    )
    email = models.EmailField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("E-Mail"),
        help_text=_("Email address (optional)")
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Telefon"),
        help_text=_("Phone number (optional)")
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("Nachricht"),
        help_text=_("Message content (optional)")
    )
    consent = models.BooleanField(
        default=False,
        verbose_name=_("Einwilligung"),
        help_text=_("Data processing consent")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Erstellt am"),
        help_text=_("Date and time when the message was created")
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_("Gelesen"),
        help_text=_("Whether the message has been read")
    )

    class Meta:
        verbose_name = _("Kontaktnachricht")
        verbose_name_plural = _("Kontaktnachrichten")
        ordering = ['-created_at']

    def __str__(self):
        name_display = self.name if self.name else "Anonym"
        return f"{name_display} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
