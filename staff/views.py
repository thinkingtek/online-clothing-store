from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView, TemplateView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from cart.utils import get_or_set_order_session
from django.urls import reverse_lazy
from cart.models import *
from .mixins import *


class Staff(LoginRequiredMixin, TemplateView):
    template_name = 'staff/staff-home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Staff Page"
        context["staff_active"] = True
        return context


class Products(LoginRequiredMixin, StaffUserMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'staff/products-list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | All products"
        context["staff_active"] = True
        return context


class Orders(LoginRequiredMixin, StaffUserMixin, ListView):
    queryset = Order.objects.filter(ordered=True).order_by('-ordered_date')
    context_object_name = "orders"
    template_name = "staff/order-list.html"
    paginate_by = 15

    # def test_func(self):
    #     user = self.request.user
    #     if user.groups.filter(name="staff").exists():
    #         return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Orders"
        context["staff_active"] = True
        return context


class OrderDetails(LoginRequiredMixin, DetailView):
    Model = Order
    context_object_name = "order"
    template_name = "staff/order-details.html"

    def get_object(self):
        return get_object_or_404(Order, ordered=True, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Orders"
        context["staff_active"] = True
        return context


class AddProduct(LoginRequiredMixin, StaffUserMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = "staff/add-product.html"
    success_url = reverse_lazy('staff:products')

    def form_valid(self, form):
        form.instance.staff = self.request.user
        messages.success(self.request, "Product added")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Add Products"
        context['view_name'] = 'Add Product'
        context["staff_active"] = True
        return context


class UpdateProduct(LoginRequiredMixin, StaffUserMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    template_name = "staff/add-product.html"
    success_url = reverse_lazy('staff:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Add Products"
        context['view_name'] = 'Update Product'
        context["staff_active"] = True
        return context


class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        product.delete()
        messages.info(self.request, "Product removed")
        return redirect("staff:products")
