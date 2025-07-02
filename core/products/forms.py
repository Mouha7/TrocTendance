from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'size', 'category', 'condition', 'operation']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Titre de votre produit'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white resize-vertical min-h-[100px]',
                'rows': 5,
                'placeholder': 'Décrivez votre produit en détail...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': '0.000',
                'step': '0.01',
                'min': '0'
            }),
            'size': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
            }),
            'operation': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white appearance-none'
            })
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'price': 'Prix (FCFA)',
            'size': 'Taille',
            'category': 'Catégorie',
            'condition': 'État du produit',
            'operation': 'Type d\'opération'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Choisir une catégorie"

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-black file:text-white hover:file:bg-gray-800 file:transition-colors file:duration-300',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-black focus:ring-0 transition-colors duration-300 text-black bg-white',
                'placeholder': 'Description de l\'image'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-black bg-gray-100 border-gray-300 focus:ring-black focus:ring-2 rounded'
            })
        }
        labels = {
            'image': 'Image',
            'alt_text': 'Description',
            'is_primary': 'Image principale'
        }

# Formset pour gérer plusieurs images
ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage, 
    form=ProductImageForm,
    fields=['image', 'alt_text', 'is_primary'],
    extra=3,  # 3 champs d'images par défaut
    max_num=5,  # Maximum 5 images
    can_delete=True
)