from django.db import models
from cart.models import Order
from django.utils import timezone
from cart.imports.choices import PAYMENT_METHOD
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Payment(models.Model):
    reference = models.CharField(max_length=10)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    raw_response = models.TextField()

    # @property
    # def reference_number(self):
    #     return f"PAYMENT-{self.order}-{self.pk}"

    def __str__(self):
        return self.reference


class Refund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f" Refund {self.pk}"
