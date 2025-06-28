from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    icon = models.CharField(max_length=10, default="📦", verbose_name="Icône")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.icon} {self.name}"

class ProductCondition(models.TextChoices):
    NEW = 'new', 'Neuf'
    LIKE_NEW = 'like_new', 'Comme neuf'
    GOOD = 'good', 'Bon état'
    FAIR = 'fair', 'État correct'
    POOR = 'poor', 'Mauvais état'

class ProductStatus(models.TextChoices):
    AVAILABLE = 'available', 'Disponible'
    RESERVED = 'reserved', 'Réservé'
    SOLD = 'sold', 'Vendu'

class ProductSize(models.TextChoices):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie")
    condition = models.CharField(
        max_length=20, 
        choices=ProductCondition.choices, 
        default=ProductCondition.GOOD,
        verbose_name="État"
    )
    status = models.CharField(
        max_length=20, 
        choices=ProductStatus.choices, 
        default=ProductStatus.AVAILABLE,
        verbose_name="Statut"
    )
    size = models.CharField(
        max_length=2, 
        choices=ProductSize.choices,
        default=ProductSize.M,
        blank=True, 
        verbose_name="Taille"
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vendeur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    slug = models.SlugField(max_length=255, blank=True, verbose_name="Slug")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # ✅ CORRECTION : Auto-générer le slug si manquant
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if self.slug:
            return reverse('products:detail_slug', kwargs={'pk': self.pk, 'slug': self.slug})
        return reverse('products:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Texte alternatif")
    is_primary = models.BooleanField(default=False, verbose_name="Image principale")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Image de produit"
        verbose_name_plural = "Images de produit"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image pour {self.product.title}"
