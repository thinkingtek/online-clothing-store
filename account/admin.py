from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from .models import *


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city')
    search_fields = ['name']


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    # Checking if admin enters more than one name in the form (first and lastname)
    def clean(self):
        firstname = self.cleaned_data.get('first_name').split(" ")
        lastname = self.cleaned_data.get('last_name').split(" ")
        if len(firstname) > 1:
            self.add_error('first_name', 'Firstname only')
        if len(lastname) > 1:
            self.add_error('last_name', 'Lastname only')
        return super().clean()


@admin.register(User)
class UsersAdmin(UserAdmin):
    form = userForm
    fieldsets = (
        (str, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('email_verified', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (str, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'email_verified', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'groups')
    ordering = ['email']


admin.site.register(Profile)
