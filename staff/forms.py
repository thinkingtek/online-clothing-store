from cProfile import label
from django import forms
from cart.imports.choices import COLORS, SIZES
from cart.models import Product, Category, Tag
# from cart.models import Product, Category, Tag, ColourVariation, SizeVariation


class CustomC(forms.ModelMultipleChoiceField):
    def label_from_instance(self, categories):
        return "%s" % categories.name


class AddProductForm(forms.ModelForm):
    categories = CustomC(queryset=Category.objects.all(),
                         widget=forms.CheckboxSelectMultiple(attrs={
                             'class': 'checkme',
                             'onclick': 'return validateCheck();',
                         }))
    tags = CustomC(queryset=Tag.objects.all(),
                   widget=forms.CheckboxSelectMultiple(attrs={
                       'class': 'checkme',
                       'onclick': 'return validateCheckTag();',
                   }))
    available_colours = forms.MultipleChoiceField(
        choices=COLORS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ('created_at', 'updated_at',
                   'active', 'most_rated', 'staff')

    def clean_categories(self):
        categories = self.cleaned_data.get("categories")
        if categories.count() > 2:
            raise forms.ValidationError(
                "You can only select two categories for a product")
        return categories

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        if tags.count() > 2:
            raise forms.ValidationError(
                "You can only select two tags for a product")
        return tags
