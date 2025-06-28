from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'size', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Titre de votre produit'
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 5,
                'placeholder': 'Décrivez votre produit en détail...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.000',
                'step': '0.01',
                'min': '0'
            }),
            'size': forms.Select(attrs={
                'class': 'input-field',
            }),
            'category': forms.Select(attrs={
                'class': 'input-field'
            }),
            'condition': forms.Select(attrs={
                'class': 'input-field'
            })
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'price': 'Prix (FCFA)',
            'size': 'Taille',
            'category': 'Catégorie',
            'condition': 'État du produit'
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
                'class': 'input-field',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Description de l\'image'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
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