import json
from django.db.models import Q, Count
from rest_framework.decorators import api_view
from .serializers import ShippingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView, DetailView, UpdateView, View, FormView
from .mixins import RedirectZeroItem
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .utils import *
from django.urls import reverse_lazy
from .forms import *
from .models import *
from datetime import timedelta, date
from account.models import Address
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


# category and tag products list used in context also
def category_list(request):
    categories = Product.objects.filter(active=True).values(
        'categories__name').annotate(Count('categories__name'))[:10]
    tags = Product.objects.filter(active=True).values(
        'tags__name').annotate(Count('tags__name'))[:10]
    return {'categories': categories, 'tags': tags}


# clear orders that were not proceeded with after 1day
@login_required
def clearOrders(request):
    orders = Order.objects.filter(ordered=False)
    today = date.today()
    for order in orders:
        start_date = order.start_date.date()
        end_date = start_date + timedelta(days=1)

        if end_date < today:
            order.delete()
    return render(request, 'cart/delete_orders.html')


# Endpoint to a specific shipping price
@api_view(["GET"])
def shippingMethodApi(request, pk):
    try:
        method = ShippingMethod.objects.get(pk=pk)
    except ShippingMethod.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ShippingSerializer(method, many=False)
    return Response(serializer.data)


# func to get recent and similar products for product details page and update cart-item page
def productUtils(product):
    recent_products = Product.objects.filter(active=True)[:4]
    cats_name = product.categories.all()
    tags_name = product.tags.all()
    similar_products = Product.objects.filter(
        active=True, categories__in=cats_name, tags__in=tags_name).exclude(slug=product.slug)
    similar_products = similar_products.annotate(cat_count=Count(
        'categories'), tag_count=Count('tags')).order_by('-cat_count', '-tag_count', '-created_at')[:4]

    return recent_products, similar_products


class ProductList(ListView):
    context_object_name = 'products'
    template_name = 'cart/product-list.html'
    paginate_by = 8

    def get_queryset(self):
        products = Product.objects.filter(active=True)
        category = self.request.GET.get('category', None)
        tag = self.request.GET.get('tag', None)
        if category or tag:
            products = Product.objects.filter(Q(
                active=True, categories__name=category) |
                Q(active=True, tags__name=tag)).distinct()
        return products

    def get_context_data(self, **kwargs):
        categories = Product.objects.filter(active=True).values(
            'categories__name').annotate(Count('categories__name'))[:10]
        tags = Product.objects.filter(active=True).values(
            'tags__name').annotate(Count('tags__name'))[:10]
        category_name = self.request.GET.get('category', None)
        tag_name = self.request.GET.get('tag', None)
        context = super().get_context_data(**kwargs)
        context["tag_name"] = tag_name
        context["category_name"] = category_name
        context["categories"] = categories
        context["products_active"] = True
        context["tags"] = tags
        context["title"] = "Ebisco | All products"
        return context


class CategoryProductList(ListView):
    context_object_name = 'category_products'
    paginate_by = 8
    template_name = 'cart/category-products.html'

    def get_queryset(self):
        category = get_object_or_404(
            Category, name=self.kwargs.get('name'))
        return Product.objects.filter(active=True, categories=category)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(
            Category, name=self.kwargs.get('name'))
        context = super().get_context_data(**kwargs)
        context['category_name'] = category
        context['title'] = f" Ebisco | {category} products"
        return context


class TagProductList(ListView):
    context_object_name = 'tag_products'
    paginate_by = 8
    template_name = 'cart/tags-products.html'

    def get_queryset(self):
        tag = get_object_or_404(
            Tag, name=self.kwargs.get('name'))
        return Product.objects.filter(active=True, tags=tag)

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(
            Tag, name=self.kwargs.get('name'))
        context = super().get_context_data(**kwargs)
        context['tag_name'] = tag
        context['title'] = f" Ebisco | {tag} products"
        return context


class CartView(UpdateView):
    model = Order
    form_class = SelectShipping
    template_name = 'cart/cart-list.html'
    success_url = reverse_lazy('cart:checkout')

    def get_object(self):
        order = get_or_set_order_session(self.request)
        order_pk = order.pk
        if order_pk:
            return get_object_or_404(Order, pk=order.pk)
        get_or_set_order_session(self.request)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["title"] = "Ebisco | Cart items"
        context["shipping_methods"] = ShippingMethod.objects.all()
        return context


class UpdateCartItem(UserPassesTestMixin, UpdateView):
    form_class = AddToCartForm
    model = OrderItem
    template_name = 'cart/product-detail.html'
    success_url = reverse_lazy('cart:cart-items')

    def test_func(self):
        order = get_or_set_order_session(self.request)
        item = OrderItem.objects.get(pk=self.kwargs['pk'])
        if order == item.order:
            return True

    def get_form_kwargs(self):
        item = OrderItem.objects.get(pk=self.kwargs['pk'])
        product = get_object_or_404(Product, slug=item.product.slug)
        kwargs = super().get_form_kwargs()
        kwargs["product_id"] = product.pk
        return kwargs

    def form_valid(self, form):
        item = OrderItem.objects.get(pk=self.kwargs['pk'])
        product = get_object_or_404(Product, slug=item.product.slug)
        form.instance.ordered_item_price = product.price
        form.instance.ordered_item_discount_price = product.discount_price
        return super(UpdateCartItem, self).form_valid(form)

    def get_context_data(self, **kwargs):
        item = OrderItem.objects.get(pk=self.kwargs['pk'])
        product = get_object_or_404(Product, slug=item.product.slug)
        recent_products, similar_products = productUtils(product)
        context = super().get_context_data(**kwargs)
        context["similar_products"] = similar_products
        context["recent_products"] = recent_products
        context["title"] = f"Ebisco | {product.title}"
        context["product"] = product
        return context


class ProductDetail(FormView):
    form_class = AddToCartForm
    template_name = 'cart/product-detail.html'
    success_url = reverse_lazy('cart:cart-items')

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["product_id"] = self.get_object().pk
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        form.instance.order = order
        form.instance.product = product
        form.instance.ordered_item_price = product.price
        form.instance.ordered_item_discount_price = product.discount_price
        form.save()
        return super(ProductDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        product = self.get_object()
        recent_products, similar_products = productUtils(product)
        context = super().get_context_data(**kwargs)
        print(recent_products)
        context["similar_products"] = similar_products
        context["recent_products"] = recent_products
        context["title"] = f"Ebisco | {product.title}"
        context["product"] = product
        return context


class Checkout(LoginRequiredMixin, RedirectZeroItem, FormView):
    template_name = "cart/checkout.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy('payment:select-payment')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get(
            'selected_shipping_address')
        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                user=self.request.user,
                state=form.cleaned_data.get('state'),
                address_line=form.cleaned_data.get(
                    'address_line'),
                company_name=form.cleaned_data.get('company_name'),
                phone=form.cleaned_data.get('phone'),
                zip_code=form.cleaned_data.get('zip_code'),
                city=form.cleaned_data.get('city'),
                landmark=form.cleaned_data.get(
                    'landmark'),
                terms_and_conditions=form.cleaned_data.get(
                    'terms_and_conditions')
            )
            order.shipping_address = address
        updateOrederedPrice(order)
        order.save()
        messages.info(
            self.request, "You have successfully submitted your address for Shipping")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checkout_page"] = True
        context["title"] = "Ebisco | Checkout"
        return context


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, pk=kwargs['pk'])
        order_item.delete()
        return redirect("cart:cart-items")


class RemoveAllFromCart(View):
    def get(self, request, *args, **kwargs):
        order_item = get_or_set_order_session(self.request)
        order_item.delete()
        return redirect("cart:cart-items")


class Orders(LoginRequiredMixin, ListView):
    context_object_name = "orders"
    template_name = "cart/orders.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, ordered=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.request.user} | Orders"
        context["profile_active"] = True
        return context


class OrderDetails(LoginRequiredMixin, DetailView):
    Model = Order
    context_object_name = "order"
    template_name = "cart/order-details.html"

    def get_object(self):
        return get_object_or_404(Order, user=self.request.user, ordered=True, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.request.user} | Orders"
        context["profile_active"] = True
        return context
