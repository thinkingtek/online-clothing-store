from .models import *
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RefundForm(forms.ModelForm):
    ref_code = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={"placeholder": "Type in your Order ref code"}))
    message = forms.CharField(required=True, help_text="* You can only send a Request once for a specific order", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Tell us your reason for refund.',
        'rows': 7,
    }))

    class Meta:
        model = Refund
        fields = ('ref_code', 'message')

    def clean(self):
        ref_code = self.cleaned_data.get('ref_code')
        try:
            order = Order.objects.get(ref_code=ref_code)
            if order.request_refund == True:
                self.add_error(
                    'ref_code', 'A refund request has been sent for this order we will get back to you soon, Thank you.')
        except Order.DoesNotExist:
            self.add_error(
                'ref_code', 'An Order with this ref code does not exist in our database.')
