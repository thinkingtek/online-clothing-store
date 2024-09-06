from django.contrib import admin
from .models import *


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method',
                    'amount', 'timestamp', 'successful')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'created_at', 'accepted')
