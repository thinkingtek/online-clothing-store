from django.urls import path
from .views import *


app_name = 'cart'

urlpatterns = [
    #     Api-endpoint to get shipping details
    path('api-shipping-details/<pk>/',
         shippingMethodApi, name='api-shipping-method'),

    # list of customers order
    path('orders/', Orders.as_view(), name='orders'),

    #     clear all customers others
    path('clear-orders/', clearOrders, name='clear-orders'),

    #     customer's order details
    path('order-details/<int:pk>', OrderDetails.as_view(), name='order-details'),
    path('category-products/<str:name>',
         CategoryProductList.as_view(), name='category-products'),
    path('tag-products/<str:name>',
         TagProductList.as_view(), name='tag-products'),

    # checkout page
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('cart-items/', CartView.as_view(), name='cart-items'),
    path('remove-cart/<int:pk>/', RemoveFromCart.as_view(), name='cart-remove'),
    path('remove-all-items/', RemoveAllFromCart.as_view(), name='remove-all-items'),

    #     update cart item
    path('<int:pk>/update-item', UpdateCartItem.as_view(),  name='update-cart-item'),

    #     product details and add to cart form
    path('<slug:slug>/', ProductDetail.as_view(),  name='product-detail'),

    path('', ProductList.as_view(),  name='product-list')

]
