from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from .models import Product, Category
from .forms import ProductForm, ProductImageFormSet

def index(request):
    """Page d'accueil avec liste des produits et filtres"""
    
    # Récupérer tous les paramètres de recherche et filtres
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    size_filter = request.GET.get('size', '')  # Pour les futurs filtres de taille
    sort_by = request.GET.get('sort', '-created_at')  # Par défaut, tri par date décroissante
    
    # Base query : seulement les produits disponibles
    products = Product.objects.filter(status='available').select_related('category', 'seller')
    
    # Filtrage par recherche
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filtrage par catégorie
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)
    
    # Tri des produits
    sort_options = {
        '-created_at': '-created_at',  # Plus récents
        'created_at': 'created_at',    # Plus anciens
        'price': 'price',              # Prix croissant
        '-price': '-price',            # Prix décroissant
        'title': 'title',              # Alphabétique
    }
    
    # Tri par taille
    size_sort_options = {
        'S': 'size',  # Taille S
        'M': 'size',  # Taille M
        'L': 'size',  # Taille L
        'XL': 'size', # Taille XL
    }
    
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    
    # Filtrage par taille (à implémenter si nécessaire)
    if size_filter in size_sort_options:
        products = products.filter(size=size_filter)
    
    # Pagination (8 produits par page)
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer toutes les catégories pour le filtre
    categories = Category.objects.all().order_by('name')
    
    # Statistiques rapides
    total_products = Product.objects.filter(status='available').count()
    total_categories = categories.count()
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'current_sort': sort_by,
        'current_sort_size': size_filter,
        'total_products': total_products,
        'total_categories': total_categories,
        'sort_options_size': [
            ['ALL', 'Toutes les tailles'],
            ('S', 'Taille S'),
            ('M', 'Taille M'),
            ('L', 'Taille L'),
            ('XL', 'Taille XL'),
        ],
        'sort_options': [
            ('-created_at', 'Plus récents'),
            ('created_at', 'Plus anciens'),
            ('price', 'Prix croissant'),
            ('-price', 'Prix décroissant'),
            ('title', 'Alphabétique'),
        ]
    }
    
    return render(request, 'products/index.html', context)

def product_detail(request, pk, slug=None):
    """Page de détail d'un produit"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'seller').prefetch_related('images'),
        pk=pk
    )
    
    # Produits similaires (même catégorie, excluant le produit actuel)
    similar_products = Product.objects.filter(
        category=product.category,
        status='available'
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'products/detail.html', context)

@login_required
def product_create(request):
    """Créer un nouveau produit"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            print('Form data:', request.POST)
            try:
                with transaction.atomic():
                    # Créer le produit
                    product = form.save(commit=False)
                    product.seller = request.user
                    product.save()
                    
                    # Créer les images
                    formset.instance = product
                    formset.save()
                    
                    # Vérifier qu'il y a au moins une image principale
                    primary_images = product.images.filter(is_primary=True)
                    if not primary_images.exists():
                        # Définir la première image comme principale
                        first_image = product.images.first()
                        if first_image:
                            first_image.is_primary = True
                            first_image.save()
                    
                    messages.success(request, f'Produit "{product.title}" créé avec succès!')
                    return redirect('products:my_products')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de la création: {str(e)}')
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Ajouter un produit',
        'button_text': 'Publier le produit'
    }
    return render(request, 'products/product_form.html', context)

@login_required
def product_update(request, pk):
    """Modifier un produit existant"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    product = form.save()
                    formset.save()
                    
                    # Vérifier qu'il y a au moins une image principale
                    primary_images = product.images.filter(is_primary=True)
                    if not primary_images.exists():
                        first_image = product.images.first()
                        if first_image:
                            first_image.is_primary = True
                            first_image.save()
                    
                    messages.success(request, f'Produit "{product.title}" modifié avec succès!')
                    return redirect('products:my_products')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de la modification: {str(e)}')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    
    context = {
        'form': form,
        'formset': formset,
        'product': product,
        'title': 'Modifier le produit',
        'button_text': 'Sauvegarder les modifications'
    }
    return render(request, 'products/product_form.html', context)

@login_required
def product_delete(request, pk):
    """Supprimer un produit"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        product_title = product.title
        product.delete()
        messages.success(request, f'Produit "{product_title}" supprimé avec succès!')
        return redirect('products:my_products')
    
    context = {
        'product': product
    }
    return render(request, 'products/product_confirm_delete.html', context)

@login_required
def my_products(request):
    """Page "Mes annonces" du vendeur"""
    # Récupérer les paramètres de filtrage
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    # Base query : produits de l'utilisateur connecté
    products = Product.objects.filter(seller=request.user).select_related('category').prefetch_related('images')
    
    # Filtrage par statut
    if status_filter != 'all':
        products = products.filter(status=status_filter)
    
    # Filtrage par recherche
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Tri par date de création (plus récents en premier)
    products = products.order_by('-created_at')
    
    # Pagination (6 produits par page)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    stats = {
        'total': Product.objects.filter(seller=request.user).count(),
        'available': Product.objects.filter(seller=request.user, status='available').count(),
        'sold': Product.objects.filter(seller=request.user, status='sold').count(),
        'reserved': Product.objects.filter(seller=request.user, status='reserved').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': [
            ('all', 'Tous'),
            ('available', 'Disponibles'),
            ('reserved', 'Réservés'),
            ('sold', 'Vendus'),
        ]
    }
    return render(request, 'products/my_products.html', context)