from django.urls import path
# from cart.views import ProductDetail
from .views import *
from cart.views import ProductDetail

app_name = 'ecomm'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('search-products', SearchResults.as_view(), name='search-items'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    # path('search-products/', searchProducts, name='search-items'),
]
