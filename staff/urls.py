from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('products/', Products.as_view(), name='products'),
    path('orders/', Orders.as_view(), name='orders'),
    path('add-product/', AddProduct.as_view(), name='add-product'),
    path('product/<slug:slug>/update/',
         UpdateProduct.as_view(), name='update-product'),
    path('delete-product/<slug:slug>',
         DeleteProduct.as_view(), name='delete-product'),
    path('order-details/<int:pk>',
         OrderDetails.as_view(), name='order-details'),
    path('', Staff.as_view(),  name='staff-home'),

]
