from PIL import Image
from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
from account.models import Address
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from .imports.choices import *

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=10, unique=True,)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Product(models.Model):
    staff = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=260, unique=True)
    description = models.TextField()
    image_1 = models.ImageField(upload_to='product_img', validators=[
        FileExtensionValidator(['jpg', 'jpeg'])])
    image_2 = models.ImageField(upload_to='product_img', null=True, blank=True, validators=[
        FileExtensionValidator(['jpg', 'jpeg'])])
    image_3 = models.ImageField(upload_to='product_img', null=True, blank=True, validators=[
        FileExtensionValidator(['jpg', 'jpeg'])])
    image_4 = models.ImageField(upload_to='product_img', null=True, blank=True, validators=[
        FileExtensionValidator(['jpg', 'jpeg'])])
    stock = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    available_colours = MultiSelectField(
        choices=COLORS)
    available_size = MultiSelectField(
        choices=SIZES)
    most_rated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def save(self):
        super().save()
        img_1 = Image.open(self.image_1.path)
        if img_1.height > 450 or img_1.width > 450:
            output_size = (450, 450)
            img_1.thumbnail(output_size)
            img_1.save(self.image_1.path)
        if self.image_2:
            img_2 = Image.open(self.image_2.path)
            if img_2.height > 450 or img_2.width > 450:
                output_size = (450, 450)
                img_2.thumbnail(output_size)
                img_2.save(self.image_2.path)
        if self.image_3:
            img_3 = Image.open(self.image_3.path)
            if img_3.height > 450 or img_3.width > 450:
                output_size = (450, 450)
                img_3.thumbnail(output_size)
                img_3.save(self.image_3.path)
        if self.image_4:
            img_4 = Image.open(self.image_4.path)
            if img_4.height > 450 or img_4.width > 450:
                output_size = (450, 450)
                img_4.thumbnail(output_size)
                img_4.save(self.image_4.path)

    def get_absolute_url(self):
        return reverse('ecomm:product-detail', kwargs={'slug': self.slug})

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def stock_count(self):
        return self.stock > 1

    def get_absolute_url(self):
        return reverse('cart:product-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('staff:product-update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('staff:product-delete', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    colour = models.CharField(max_length=20, choices=COLORS)
    size = models.CharField(max_length=20, choices=SIZES)

    # order items details
    order_item_name = models.CharField(
        null=True, blank=True, max_length=50)
    ordered_item_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_item_discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_item_subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    def get_item_price(self):
        if self.ordered_item_discount_price:
            price = self.ordered_item_discount_price
        else:
            price = self.ordered_item_price
        return price

    def get_amount_saved(self):
        price = self.ordered_item_price
        discount_price = self.ordered_item_discount_price
        if discount_price:
            saved = price * self.quantity - discount_price * self.quantity
            return saved

    def save(self, *args, **kwargs):
        if self.order.ordered is False:
            self.order_item_name = self.product.title
            self.ordered_item_subtotal = self.get_item_price() * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} * {self.product.title}"


class ShippingMethod(models.Model):
    name = models.CharField(max_length=26)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    ref_code = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_method = models.ForeignKey(
        ShippingMethod, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default='packaging')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)
    request_refund = models.BooleanField(default=False)
    ordered_shipping_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    ordered_subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_overall_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_shipping_fee(self):
        return self.ordered_shipping_fee

    def get_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.ordered_item_subtotal
        return total

    def get_overall_total(self):
        if self.shipping_method:
            return self.get_subtotal() + self.shipping_method.price
        return self.get_subtotal()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Order, self).save(*args, **kwargs)
        if self.ordered is False and self.shipping_method:
            self.ordered_shipping_fee = self.shipping_method.price
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        if self.ref_code:
            return self.ref_code
        return self.reference_number
