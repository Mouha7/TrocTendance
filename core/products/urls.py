from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Gestion des produits
    path('my-products/', views.my_products, name='my_products'),
    path('create/', views.product_create, name='create'),
    path('product/<int:pk>/edit/', views.product_update, name='update'),
    path('product/<int:pk>/delete/', views.product_delete, name='delete'),
    
    path('product/<int:pk>/', views.product_detail, name='detail'),
    path('product/<int:pk>/<slug:slug>/', views.product_detail, name='detail_slug'),
]