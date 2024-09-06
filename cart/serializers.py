from rest_framework import serializers
from .models import ShippingMethod


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = "__all__"
