from django import forms
from cart.imports.choices import EMAIL_SUBJECTS


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search produtcs'}))

    class Meta:
        fields = "__all__"


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Firstname"
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Lastname"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Your Email Address"
    }))
    subject = forms.ChoiceField(choices=EMAIL_SUBJECTS)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Type in your message"
    }))
