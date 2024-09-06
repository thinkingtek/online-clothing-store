from .models import *
from account.models import Address
from django import forms
from cart.imports.choices import STATES
from django.contrib.auth import get_user_model

User = get_user_model()


class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "min": 1, "value": 1
    }))

    class Meta:
        model = OrderItem
        fields = ('quantity', 'colour', 'size')

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        super().__init__(*args, **kwargs)

    def clean(self):
        product = Product.objects.get(pk=self.product_id)
        quantity = self.cleaned_data.get('quantity')
        if product.stock < quantity:
            raise forms.ValidationError(
                f"The maximum stock in store is {product.stock}")


class SelectShipping(forms.ModelForm):
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.all(), widget=forms.Select(attrs={
            'onchange': 'updateTotalPrice()',
            'id': 'select-shipping'
        }))

    class Meta:
        model = Order
        fields = ['shipping_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_method'].empty_label = 'Select Shipping'


class ShippingAddressForm(forms.Form):
    state = forms.ChoiceField(choices=STATES, required=False)
    address_line = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Shipping Address'
    }))
    company_name = forms.CharField(required=False, help_text='If any*', widget=forms.TextInput(attrs={
        'placeholder': 'Person/Company Name'
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Phone No.'
    }))
    zip_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Zip / Postal code'
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Town or City'
    }))
    landmark = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Landmark'
    }))

    terms_and_conditions = forms.BooleanField(
        label_suffix='', label='Terms and Conditions', widget=forms.CheckboxInput())

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=False
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("user_id")
        user = User.objects.get(pk=user_id)
        super().__init__(*args, **kwargs)
        shipping_address_qs = Address.objects.filter(
            user=user)

        self.fields['selected_shipping_address'].queryset = shipping_address_qs
        self.fields['selected_shipping_address'].empty_label = 'Select a shipping address'

    def clean(self):
        data = self.cleaned_data
        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('state', None):
                self.add_error('state',
                               'Pls fill in this field')
            if not data.get('address_line', None):
                self.add_error('address_line',
                               'Pls fill in this field')
            if not data.get('phone', None):
                self.add_error('phone',
                               'Pls fill in this field')
            if not data.get('zip_code', None):
                self.add_error('zip_code',
                               'Pls fill in this field')
            if not data.get('city', None):
                self.add_error('city',
                               'Pls fill in this field')
            if not data.get('landmark', None):
                self.add_error('landmark',
                               'Pls fill in this field')
