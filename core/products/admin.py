from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    prepopulated_fields = {}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'seller', 'condition', 'status', 'created_at']
    list_filter = ['category', 'condition', 'status', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'description', 'price', 'category')
        }),
        ('Opération, état et statut', {
            'fields': ('operation', 'condition', 'status')
        }),
        ('Vendeur', {
            'fields': ('seller',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    list_editable = ['is_primary', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Aperçu"
