from datetime import timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone 
from core.products.models import Product

User = get_user_model()

class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'En attente'
    CONFIRMED = 'confirmed', 'Confirmée'
    SHIPPED = 'shipped', 'Expédiée'
    DELIVERED = 'delivered', 'Livrée'
    COMPLETED = 'completed', 'Terminée'
    CANCELLED = 'cancelled', 'Annulée'

class DeliveryMethod(models.TextChoices):
    PICKUP = 'pickup', 'Retrait en main propre'
    DELIVERY = 'delivery', 'Livraison à domicile'

class Order(models.Model):
    # Relations principales
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='orders_as_buyer', verbose_name="Acheteur")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='orders_as_seller', verbose_name="Vendeur")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    
    # Informations de la commande
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total (FCFA)")
    commission = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Commission (FCFA)")
    
    # Statut et livraison
    status = models.CharField(max_length=20, choices=OrderStatus.choices,
                            default=OrderStatus.PENDING, verbose_name="Statut")
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethod.choices,
                                    default=DeliveryMethod.PICKUP, verbose_name="Mode de livraison")
    
    # Adresses
    delivery_address = models.TextField(blank=True, verbose_name="Adresse de livraison")
    pickup_location = models.TextField(blank=True, verbose_name="Lieu de rendez-vous")
    
    # Notes et messages
    buyer_notes = models.TextField(blank=True, verbose_name="Notes de l'acheteur")
    seller_notes = models.TextField(blank=True, verbose_name="Notes du vendeur")
    
    # Dates importantes
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de confirmation")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'expédition")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de livraison")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'achèvement")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'annulation")
    
    def __str__(self):
        return f"Commande #{self.pk} - {self.product.title}"
    
    def calculate_commission(self):
        """Calcule la commission troctendance (5% par défaut)"""
        commission_rate = Decimal(0.05)  # 5%
        return self.total_price * commission_rate
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement la commission
        self.commission = self.calculate_commission()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

class ReviewRating(models.IntegerChoices):
    ONE = 1, '⭐'
    TWO = 2, '⭐⭐'
    THREE = 3, '⭐⭐⭐'
    FOUR = 4, '⭐⭐⭐⭐'
    FIVE = 5, '⭐⭐⭐⭐⭐'

class Review(models.Model):
    # Relations
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Commande")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='reviews_given', verbose_name="Évaluateur")
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='reviews_received', verbose_name="Utilisateur évalué")
    
    # Contenu de l'évaluation
    rating = models.IntegerField(choices=ReviewRating.choices, verbose_name="Note")
    title = models.CharField(max_length=200, verbose_name="Titre de l'avis")
    comment = models.TextField(verbose_name="Commentaire")
    
    # Recommandation
    would_recommend = models.BooleanField(default=True, verbose_name="Recommande cet utilisateur")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'avis")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    def __str__(self):
        return f"Avis {self.rating}⭐ de {self.reviewer.username} pour {self.reviewed_user.username}"
    
    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        ordering = ['-created_at']
        # Un utilisateur ne peut donner qu'un seul avis par commande
        unique_together = ['order', 'reviewer']

class Message(models.Model):
    # Relations
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='sent_messages', verbose_name="Expéditeur")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='received_messages', verbose_name="Destinataire")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                              verbose_name="Produit concerné")
    
    # Contenu du message
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    content = models.TextField(verbose_name="Message")
    
    # Statut et dates
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière activité")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Lu le")
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.subject}"
    
    def get_other_user(self, current_user):
        """Retourne l'autre utilisateur de la conversation"""
        return self.recipient if self.sender == current_user else self.sender
    
    def get_messages(self):
        """Retourne tous les messages de cette conversation"""
        return Message.objects.filter(
            models.Q(sender=self.sender, recipient=self.recipient, product=self.product) |
            models.Q(sender=self.recipient, recipient=self.sender, product=self.product)
        ).order_by('created_at')
    
    def get_unread_count(self, user):
        """Nombre de messages non lus pour un utilisateur"""
        return self.get_messages().filter(recipient=user, is_read=False).count()
    
    def mark_as_read(self):
        """Marquer le message comme lu"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

class Conversation(models.Model):
    """Modèle pour grouper les messages par conversation"""
    # Participants
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='conversations_as_user1', verbose_name="Utilisateur 1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='conversations_as_user2', verbose_name="Utilisateur 2")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Produit concerné")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière activité")
    
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']
        unique_together = ['user1', 'user2', 'product']
    
    def __str__(self):
        return f"Conversation {self.user1.username} ↔ {self.user2.username} - {self.product.title}"
    
    def get_other_user(self, current_user):
        """Retourne l'autre utilisateur de la conversation"""
        return self.user2 if self.user1 == current_user else self.user1
    
    def get_messages(self):
        """Retourne tous les messages de cette conversation"""
        return Message.objects.filter(
            models.Q(sender=self.user1, recipient=self.user2, product=self.product) |
            models.Q(sender=self.user2, recipient=self.user1, product=self.product)
        ).order_by('created_at')
    
    def get_unread_count(self, user):
        """Nombre de messages non lus pour un utilisateur"""
        return self.get_messages().filter(recipient=user, is_read=False).count()

class Exchange(models.Model):
    """Modèle pour les échanges de produits"""
    product_offered = models.ForeignKey(
        Product, 
        related_name='exchanges_offered', 
        on_delete=models.CASCADE,
        verbose_name="Produit proposé"
    )
    product_requested = models.ForeignKey(
        Product, 
        related_name='exchanges_requested', 
        on_delete=models.CASCADE,
        verbose_name="Produit demandé"
    )
    proposer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='exchanges_proposed', 
        on_delete=models.CASCADE,
        verbose_name="Proposeur"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='exchanges_received', 
        on_delete=models.CASCADE,
        verbose_name="Destinataire"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('accepted', 'Accepté'),
            ('rejected', 'Refusé'),
            ('completed', 'Échangé'),
            ('cancelled', 'Annulé'),
        ],
        default='pending',
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Échange"
        verbose_name_plural = "Échanges"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.proposer} propose {self.product_offered} contre {self.product_requested} ({self.get_status_display()})"

