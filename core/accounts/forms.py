from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Size, User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
        'placeholder': 'votre@email.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
        'placeholder': 'Prénom'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
        'placeholder': 'Nom'
    }))
    size = forms.ChoiceField(
        choices=Size.choices,
        initial=Size.M,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'size', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
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
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Email'
            }),
            'size': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Téléphone'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical',
                'rows': 2,
                'placeholder': 'Adresse'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'w-full file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-black file:text-white hover:file:bg-gray-800 file:transition-colors file:duration-300',
                'accept': 'image/*'
            }),
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