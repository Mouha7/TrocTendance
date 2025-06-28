from django.contrib.auth.models import AbstractUser
from django.db import models

class Size(models.TextChoices):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'

class User(AbstractUser):
    # Champs supplémentaires pour troctendance
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Photo de profil")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    size = models.CharField(
        max_length=2,
        choices=Size.choices,
        default=Size.M,
        verbose_name="Taille"
    )
    
    @property
    def seller_rating(self):
        reviews = self.reviews_received.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"