from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Messages
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/new/<int:product_id>/', views.new_message, name='new_message'),
    path('api/unread-count/', views.unread_count, name='unread_count'),
    
    # Commandes
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('exchange/<int:product_id>/', views.propose_exchange, name='propose_exchange'),
    path('payment/', views.payment_simulation, name='payment_simulation'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-sales/', views.my_sales, name='my_sales'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/review/', views.leave_review, name='leave_review'),
    path('order/<int:order_id>/status/<str:new_status>/', views.update_order_status, name='update_order_status'),
]