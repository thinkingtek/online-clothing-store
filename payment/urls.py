from .views import *
from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('confirm-order/', ConfirmOrder.as_view(), name='confirm-order'),
    path('thank-you/', ThankYou.as_view(), name='thank-you'),
    path('request-refund/', RequestRefund.as_view(), name='request-refund'),
    path('', SelectPayment.as_view(), name='select-payment'),
]
