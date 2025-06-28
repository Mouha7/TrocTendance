from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Size, User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input-field',
        'placeholder': 'votre@email.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'input-field',
        'placeholder': 'Prénom'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'input-field',
        'placeholder': 'Nom'
    }))
    size = forms.ChoiceField(
        choices=Size.choices,
        initial=Size.M,
        widget=forms.Select(attrs={
            'class': 'input-field',
            'placeholder': 'Taille'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'size', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Confirmer le mot de passe'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.size = self.cleaned_data['size']
        user.is_active = True  # Activer l'utilisateur par défaut
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'size', 'email', 'phone', 'address', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}),
            'size': forms.Select(attrs={'class': 'input-field'}),
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Téléphone'}),
            'address': forms.Textarea(attrs={'class': 'input-field', 'rows': 2, 'placeholder': 'Adresse'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'size': 'Taille',
            'phone': 'Téléphone',
            'address': 'Adresse',
            'avatar': 'Photo de profil',
        }