from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Ajouter les nouveaux champs aux formulaires d'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informations TrocTendance', {
            'fields': ('avatar', 'phone', 'address', 'seller_rating')
        }),
    )
    
    # Ajouter dans la liste d'affichage
    list_display = UserAdmin.list_display + ('phone', 'seller_rating')
    
    # Permettre de filtrer par note
    list_filter = UserAdmin.list_filter 
