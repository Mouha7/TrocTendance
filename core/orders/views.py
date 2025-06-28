from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exchange, Order, OrderStatus, Review
from django.utils import timezone
from django.db.models import Q, Max
from django.core.paginator import Paginator
from django.db import transaction 
from core.products.models import Product
from .models import Message, Conversation, Order
from .forms import CheckoutForm, MessageForm, PaymentSimulationForm, QuickMessageForm, ReviewForm
from django.views.decorators.http import require_POST

@login_required
def inbox(request):
    """Boîte de réception - liste des conversations"""
    # Récupérer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).prefetch_related('product', 'user1', 'user2')
    
    # Ajouter les informations sur les messages non lus
    conversation_data = []
    for conv in conversations:
        other_user = conv.get_other_user(request.user)
        unread_count = conv.get_unread_count(request.user)
        last_message = conv.get_messages().last()
        
        conversation_data.append({
            'conversation': conv,
            'other_user': other_user,
            'unread_count': unread_count,
            'last_message': last_message,
        })
    
    # Tri par dernière activité
    conversation_data.sort(key=lambda x: x['conversation'].updated_at, reverse=True)
    
    # Pagination
    paginator = Paginator(conversation_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    total_unread = sum(item['unread_count'] for item in conversation_data)
    
    context = {
        'page_obj': page_obj,
        'conversations': page_obj.object_list,
        'total_unread': total_unread,
    }
    return render(request, 'orders/inbox.html', context)

@login_required
def conversation_detail(request, conversation_id):
    """Détail d'une conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Vérifier que l'utilisateur fait partie de la conversation
    if request.user not in [conversation.user1, conversation.user2]:
        messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect('orders:inbox')
    
    # Marquer tous les messages reçus comme lus
    unread_messages = conversation.get_messages().filter(
        recipient=request.user, 
        is_read=False
    )
    for message in unread_messages:
        message.mark_as_read()
    
    # Traiter le formulaire de réponse
    if request.method == 'POST':
        form = QuickMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = conversation.get_other_user(request.user)
            message.product = conversation.product
            message.subject = f"Re: {conversation.product.title}"
            message.save()
            
            # Mettre à jour la conversation
            conversation.updated_at = timezone.now()
            conversation.save()
            
            messages.success(request, 'Message envoyé !')
            return redirect('orders:conversation_detail', conversation_id=conversation.id)
    else:
        form = QuickMessageForm()
    
    # Récupérer tous les messages de la conversation
    conversation_messages = conversation.get_messages()
    
    context = {
        'conversation': conversation,
        'other_user': conversation.get_other_user(request.user),
        'messages': conversation_messages,
        'form': form,
    }
    return render(request, 'orders/conversation_detail.html', context)

@login_required
def new_message(request, product_id):
    """Créer un nouveau message pour un produit"""
    product = get_object_or_404(Product, id=product_id)
    
    # Vérifier que l'utilisateur n'essaie pas de se contacter lui-même
    if product.seller == request.user:
        messages.error(request, "Vous ne pouvez pas vous envoyer un message à vous-même.")
        return redirect('products:detail', pk=product.id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Créer le message
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = product.seller
            message.product = product
            message.save()
            
            # Créer ou récupérer la conversation
            conversation, created = Conversation.objects.get_or_create(
                user1=min(request.user, product.seller, key=lambda u: u.id),
                user2=max(request.user, product.seller, key=lambda u: u.id),
                product=product
            )
            conversation.updated_at = timezone.now()
            conversation.save()
            
            messages.success(request, f'Message envoyé à {product.seller.get_full_name() or product.seller.username} !')
            return redirect('orders:conversation_detail', conversation_id=conversation.id)
    else:
        # Pré-remplir le sujet
        initial_subject = f"Intéressé(e) par: {product.title}"
        form = MessageForm(initial={'subject': initial_subject})
    
    context = {
        'form': form,
        'product': product,
        'recipient': product.seller,
    }
    return render(request, 'orders/new_message.html', context)

@login_required
def unread_count(request):
    """API pour récupérer le nombre de messages non lus"""
    from django.http import JsonResponse
    
    count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'unread_count': count})

@login_required
def checkout(request, product_id):
    """Page de commande d'un produit"""
    product = get_object_or_404(Product, id=product_id, status='available')
    
    # Vérifier que l'utilisateur n'essaie pas d'acheter son propre produit
    if product.seller == request.user:
        messages.error(request, "Vous ne pouvez pas acheter votre propre produit.")
        return redirect('products:detail', pk=product.id)
    
    # Calculer les frais (TOUJOURS en Decimal)
    product_price = product.price
    commission_rate = Decimal('0.05')  # 5%
    commission = (product_price * commission_rate).quantize(Decimal('0.01'))
    total_price = (product_price + commission).quantize(Decimal('0.01'))
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Sauvegarder les données de commande en session
            request.session['checkout_data'] = {
                'product_id': product.id,
                'delivery_method': form.cleaned_data['delivery_method'],
                'delivery_address': form.cleaned_data['delivery_address'],
                'pickup_location': form.cleaned_data['pickup_location'],
                'buyer_notes': form.cleaned_data['buyer_notes'],
                'product_price': str(product_price),
                'commission': str(commission),
                'total_price': str(total_price),
            }
            return redirect('orders:payment_simulation')
    else:
        form = CheckoutForm()
    
    context = {
        'product': product,
        'form': form,
        'product_price': product_price,
        'commission': commission,
        'total_price': total_price,
        'commission_rate': commission_rate * 100,  # Pour affichage en %
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def payment_simulation(request):
    """Page de paiement (simulation masquée)"""
    # Récupérer les données de commande
    checkout_data = request.session.get('checkout_data')
    print("Checkout price : ", checkout_data)  # Debugging line
    
    if not checkout_data:
        messages.error(request, "Session expirée. Veuillez recommencer votre commande.")
        return redirect('products:index')
    
    product = get_object_or_404(Product, id=checkout_data['product_id'])
    
    if request.method == 'POST':
        form = PaymentSimulationForm(request.POST)
        if form.is_valid():
            # Récupérer le résultat de simulation depuis cleaned_data
            simulation_result = form.cleaned_data.get('simulation_result')
                        
            if simulation_result == 'success':
                # Créer la commande
                try:
                    with transaction.atomic():
                        # Créer la commande
                        order = Order.objects.create(
                            buyer=request.user,
                            seller=product.seller,
                            product=product,
                            total_price=Decimal(str(checkout_data['total_price'])),
                            commission=Decimal(str(checkout_data['commission'])),
                            delivery_method=checkout_data['delivery_method'],
                            delivery_address=checkout_data['delivery_address'],
                            pickup_location=checkout_data['pickup_location'],
                            buyer_notes=checkout_data['buyer_notes'],
                            status='pending'
                        )
                        
                        # Marquer le produit comme vendu
                        product.status = 'sold'
                        product.save()
                        
                        # Nettoyer la session
                        del request.session['checkout_data']
                        
                        # Message de succès
                        messages.success(
                            request, 
                            f'🎉 Paiement confirmé ! Votre commande #{order.id} a été enregistrée.'
                        )
                        
                        return redirect('orders:order_success', order_id=order.id)
                        
                except Exception as e:
                    messages.error(request, f"Erreur lors du traitement de votre commande: {str(e)}")
                    
            elif simulation_result == 'failure':
                messages.error(
                    request, 
                    "❌ Paiement refusé. Veuillez vérifier vos informations ou essayer un autre mode de paiement."
                )
                
            elif simulation_result == 'error':
                messages.error(
                    request, 
                    "⚠️ Une erreur est survenue lors du traitement. Veuillez réessayer dans quelques instants."
                )
        else:
            # Afficher les erreurs de validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur {field}: {error}")
                    
        # Rediriger vers la page de paiement pour réessayer en cas d'erreur
        return redirect('orders:payment_simulation')
    else:
        form = PaymentSimulationForm()
    
    context = {
        'product': product,
        'form': form,
        'checkout_data': checkout_data,
    }
    return render(request, 'orders/payment_simulation.html', context)

@login_required
def order_success(request, order_id):
    """Page de confirmation de commande"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_success.html', context)

@login_required
def my_orders(request):
    """Mes commandes (acheteur)"""
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    paginator = Paginator(orders, 3)  # 3 commandes par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notif = request.session.pop('notif', None)
    return render(request, "orders/my_orders.html", {
        "orders": page_obj.object_list,
        "page_obj": page_obj,
        "notif": notif
    })

@login_required
def my_sales(request):
    """Mes ventes (vendeur)"""
    orders = Order.objects.filter(seller=request.user).order_by('-created_at')
    paginator = Paginator(orders, 3)  # 3 ventes par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "orders/my_sales.html", {
        "orders": page_obj.object_list,
        "page_obj": page_obj
    })

@login_required
def order_detail(request, order_id):
    """Détail d'une commande"""
    order = get_object_or_404(Order, 
        Q(buyer=request.user) | Q(seller=request.user), 
        id=order_id
    )
    
    # Déterminer le rôle de l'utilisateur
    is_buyer = order.buyer == request.user
    is_seller = order.seller == request.user
    
    context = {
        'order': order,
        'is_buyer': is_buyer,
        'is_seller': is_seller,
    }
    return render(request, 'orders/order_detail.html', context)

@login_required
def create_order(request):
    # Simulation d'un paiement réussi
    if request.method == "POST":
        # Ici, on suppose que le produit et le prix sont connus
        order = Order.objects.create(
            buyer=request.user,
            seller=request.user,  
            product="Produit Test",
            total_price=50.00,
            status=OrderStatus.PENDING
        )
        messages.success(request, "Commande créée ! En attente de confirmation du vendeur.")
        # Notification simulée
        request.session['notif'] = f"Nouvelle commande #{order.pk} à confirmer."
        return redirect('orders:my_orders')
    return render(request, "orders/create_order.html")

@require_POST
@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    user = request.user

    # Vendeur : peut confirmer/refuser/expédier
    if user == order.seller:
        if new_status == 'confirmed' and order.status == 'pending':
            order.status = 'confirmed'
            order.confirmed_at = timezone.now()
            messages.success(request, "Commande acceptée !")
        elif new_status == 'cancelled' and order.status == 'pending':
            order.status = 'cancelled'
            order.cancelled_at = timezone.now()
            # Remettre le produit en vente
            order.product.status = 'available'
            order.product.save()
            messages.warning(request, "Commande refusée. Le produit est de nouveau visible.")
        elif new_status == 'shipped' and order.status == 'confirmed':
            order.status = 'shipped'
            order.shipped_at = timezone.now()
            messages.success(request, "Commande marquée comme expédiée.")
    # Acheteur : peut marquer comme livrée
    elif user == order.buyer:
        if new_status == 'delivered' and order.status == 'shipped':
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            messages.success(request, "Commande marquée comme livrée.")
    order.save()
    return redirect('orders:order_detail', order_id=order.id)

@login_required
def leave_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    # Prévention faux avis : un seul avis par commande, seulement si livrée
    if hasattr(order, 'review'):
        messages.warning(request, "Vous avez déjà laissé un avis pour cette commande.")
        return redirect('orders:order_detail', order_id=order.id)
    if order.status != 'delivered':
        messages.error(request, "Vous ne pouvez laisser un avis que pour une commande livrée.")
        return redirect('orders:order_detail', order_id=order.id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.reviewer = request.user
            review.reviewed_user = order.seller
            review.save()
            messages.success(request, "Merci pour votre avis !")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = ReviewForm()
    return render(request, 'orders/leave_review.html', {'form': form, 'order': order})

@login_required
def propose_exchange(request, product_id):
    product = get_object_or_404(Product, pk=product_id, status='available')
    # Lister les produits de l'utilisateur disponibles pour échange
    my_products = Product.objects.filter(seller=request.user, status='available')
    if request.method == 'POST':
        my_product_id = request.POST.get('product_id')
        my_product = get_object_or_404(Product, pk=my_product_id, seller=request.user)
        
        # Créer l'objet Exchange (à adapter selon ton modèle)
        Exchange.objects.create(
            product_offered=my_product,
            product_requested=product,
            proposer=request.user,
            recipient=product.seller,
            status='pending'
        )
        messages.success(request, "Proposition d'échange envoyée au vendeur.")
        return redirect('products:detail', pk=product.pk)
    return render(request, 'orders/propose_exchange.html', {
        'product': product,
        'my_products': my_products
    })