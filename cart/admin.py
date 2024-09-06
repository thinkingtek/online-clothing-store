from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


def remove_most_rated_product(modeladmin, request, queryset):
    queryset.update(most_rated=False)


def most_rated_product(modeladmin, request, queryset):
    queryset.update(most_rated=True)


remove_most_rated_product.short_description = 'Remove product as most rated'
most_rated_product.short_description = 'Make product as most rated'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock', 'price', 'discount_price',
                    'most_rated', 'active', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ['title']}
    actions = (most_rated_product, remove_most_rated_product)


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at',
                    'updated_at')


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(request_refund=True)


make_refund_accepted.short_description = 'Update Refund request'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display_links = ('ref_code', 'user')
    list_filter = ('ordered', 'request_refund')
    actions = [make_refund_accepted]
    list_display = ('ref_code', 'user', 'start_date', 'ordered_date',
                    'ordered', 'request_refund')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'colour', 'size')
    list_display_links = ('order', 'product')
    search_fields = ('product__title',)
