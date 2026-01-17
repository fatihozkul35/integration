from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, SliderImage, AppConfig

# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'phone', 'profession', 'marital_status', 'created_at', 'is_read')
    list_filter = ('is_read', 'consent', 'marital_status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'profession', 'graduation')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': ('name', 'age', 'marital_status', 'children_count')
        }),
        ('İletişim Bilgileri', {
            'fields': ('email', 'phone')
        }),
        ('Mesleki Bilgiler', {
            'fields': ('profession', 'graduation', 'driving_license')
        }),
        ('Mesaj', {
            'fields': ('message',)
        }),
        ('Durum', {
            'fields': ('consent', 'is_read', 'created_at')
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Okundu olarak işaretle"
    
    actions = [mark_as_read]


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')
    ordering = ['order', 'created_at']
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    
    fieldsets = (
        ('Görsel', {
            'fields': ('image', 'image_preview')
        }),
        ('İçerik', {
            'fields': ('title', 'description')
        }),
        ('Ayarlar', {
            'fields': ('order', 'is_active')
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "Görsel yok"
    image_preview.short_description = "Önizleme"


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    """Admin interface for AppConfig singleton model"""
    
    def has_add_permission(self, request):
        """Only allow one instance"""
        return not AppConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of singleton"""
        return False
        
    
    list_display = ('company_name', 'founder_name', 'is_active', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'founder_image_preview')
    
    fieldsets = (
        ('Şirket Bilgileri', {
            'fields': ('company_name', 'company_type', 'address', 'phone', 'email', 'website')
        }),
        ('Hukuki Bilgiler', {
            'fields': ('tax_id', 'trade_register')
        }),
        ('Kurucu Bilgileri', {
            'fields': ('founder_name', 'founder_image', 'founder_image_preview', 'founder_bio')
        }),
        ('Ayarlar', {
            'fields': ('is_active',)
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def founder_image_preview(self, obj):
        if obj.founder_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 8px;" />',
                obj.founder_image.url
            )
        return "Görsel yok"
    founder_image_preview.short_description = "Kurucu Görseli Önizleme"
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to edit view if instance exists, or create if not"""
        if AppConfig.objects.exists():
            obj = AppConfig.load()
            return admin.ModelAdmin.changeform_view(self, request, object_id=str(obj.pk), extra_context=extra_context)
        return admin.ModelAdmin.add_view(self, request, extra_context=extra_context)
