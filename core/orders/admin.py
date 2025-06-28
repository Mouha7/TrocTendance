from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Review, Message, Conversation

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'product', 'buyer', 'seller', 'total_price', 
                    'status', 'delivery_method', 'created_at']
    list_filter = ['status', 'delivery_method', 'created_at']
    search_fields = ['product__title', 'buyer__username', 'seller__username']
    list_editable = ['status']
    readonly_fields = ['commission', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('product', 'buyer', 'seller', 'quantity')
        }),
        ('Prix et commission', {
            'fields': ('total_price', 'commission')
        }),
        ('Statut et livraison', {
            'fields': ('status', 'delivery_method', 'delivery_address', 'pickup_location')
        }),
        ('Notes', {
            'fields': ('buyer_notes', 'seller_notes'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def order_number(self, obj):
        return f"#{obj.pk}"
    order_number.short_description = "N° Commande"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_info', 'rating_stars', 'reviewer', 'reviewed_user', 
                   'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = ['title', 'comment', 'reviewer__username', 'reviewed_user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Évaluation', {
            'fields': ('order', 'reviewer', 'reviewed_user', 'rating')
        }),
        ('Contenu', {
            'fields': ('title', 'comment', 'would_recommend')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def review_info(self, obj):
        return f"Avis pour commande #{obj.order.pk}"
    review_info.short_description = "Avis"
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(f'<span style="font-size: 16px;">{stars}</span>')
    rating_stars.short_description = "Note"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'product', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'content']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('sender', 'recipient', 'product')
        }),
        ('Message', {
            'fields': ('subject', 'content')
        }),
        ('Statut', {
            'fields': ('is_read', 'created_at', 'read_at')
        }),
    )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'product', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user1__username', 'user2__username', 'product__title']
    readonly_fields = ['created_at', 'updated_at']