from django import forms
from .models import Message, Order, Review

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Sujet de votre message'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 5,
                'placeholder': 'Écrivez votre message ici...'
            })
        }
        labels = {
            'subject': 'Sujet',
            'content': 'Message'
        }

class QuickMessageForm(forms.ModelForm):
    """Formulaire rapide sans sujet pour répondre"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 3,
                'placeholder': 'Tapez votre réponse...'
            })
        }
        labels = {
            'content': 'Votre réponse'
        }

class CheckoutForm(forms.ModelForm):
    """Formulaire de commande simplifié"""
    class Meta:
        model = Order
        fields = ['delivery_method', 'delivery_address', 'pickup_location', 'buyer_notes']
        widgets = {
            'delivery_method': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none',
                'id': 'delivery-method'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 3,
                'placeholder': 'Votre adresse complète de livraison'
            }),
            'pickup_location': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 3,
                'placeholder': 'Lieu de rendez-vous souhaité'
            }),
            'buyer_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 3,
                'placeholder': 'Questions ou instructions particulières...'
            })
        }
        labels = {
            'delivery_method': 'Mode de livraison',
            'delivery_address': 'Adresse de livraison',
            'pickup_location': 'Lieu de rendez-vous',
            'buyer_notes': 'Message au vendeur'
        }

class PaymentSimulationForm(forms.Form):
    """Formulaire de simulation de paiement (masqué comme vrai)"""
    PAYMENT_CHOICES = [
        ('success', '💳 Carte bancaire'),
        ('failure', '📱 PayPal'),
        ('error', '🏦 Virement bancaire'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'w-4 h-4 text-black bg-gray-100 border-gray-300 focus:ring-black focus:ring-2'
        }),
        label="Mode de paiement",
        initial='success'
    )
    
    # Champs de carte
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': '1234 5678 9012 3456',
            'pattern': r'[0-9\s]{13,19}',
            'id': 'card-number'
        }),
        label="Numéro de carte"
    )
    
    card_expiry = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': 'MM/AA',
            'pattern': '[0-9]{2}/[0-9]{2}',
            'id': 'card-expiry'
        }),
        label="Date d'expiration"
    )
    
    card_cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': '123',
            'pattern': '[0-9]{3,4}',
            'id': 'card-cvv'
        }),
        label="Code CVV"
    )
    
    card_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': 'NOM PRÉNOM',
            'id': 'card-name'
        }),
        label="Nom sur la carte"
    )
    
    accept_terms = forms.BooleanField(
        required=True,
        label="J'accepte les conditions générales de vente",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-black bg-gray-100 border-gray-300 focus:ring-black focus:ring-2 rounded'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        # Validation conditionnelle selon le mode de paiement
        if payment_method == 'success':  # Carte bancaire
            card_number = cleaned_data.get('card_number')
            card_expiry = cleaned_data.get('card_expiry')
            card_cvv = cleaned_data.get('card_cvv')
            card_name = cleaned_data.get('card_name')
            
            # Validation basique pour la carte (simulation)
            if not card_number or len(card_number.replace(' ', '')) < 13:
                raise forms.ValidationError("Veuillez saisir un numéro de carte valide.")
            if not card_expiry or len(card_expiry) != 5:
                raise forms.ValidationError("Veuillez saisir une date d'expiration valide (MM/AA).")
            if not card_cvv or len(card_cvv) < 3:
                raise forms.ValidationError("Veuillez saisir un code CVV valide.")
            if not card_name or len(card_name.strip()) < 2:
                raise forms.ValidationError("Veuillez saisir le nom du porteur de la carte.")
                
            # Simulation : succès
            cleaned_data['simulation_result'] = 'success'
            
        elif payment_method == 'failure':  # PayPal = échec simulé
            cleaned_data['simulation_result'] = 'failure'
            
        else:  # Virement = erreur simulée
            cleaned_data['simulation_result'] = 'error'
            
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': "Note",
            'comment': "Votre avis",
        }
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f"{i} ⭐") for i in range(1, 6)],
                attrs={
                    'class': 'w-4 h-4 text-black bg-gray-100 border-gray-300 focus:ring-black focus:ring-2'
                }
            ),
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': "Votre commentaire...", 
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical'
            }),
        }

