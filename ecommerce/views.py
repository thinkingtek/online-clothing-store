from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from cart.utils import *
from .forms import *
from cart.models import Product
from django.conf import settings
# Create your views here.


def searchForm(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
    else:
        form = SearchForm()

    order = get_or_set_order_session(request)
    context = {
        'search_form': form,
        'order': order
    }
    return context


class IndexView(TemplateView):
    template_name = 'ecommerce/index.html'

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(active=True)[:8]
        recent_products = Product.objects.filter(active=True)[:4]
        most_rated = Product.objects.filter(active=True, most_rated=True)[:4]
        context = super().get_context_data(**kwargs)
        context['products'] = products
        context['recent_products'] = recent_products
        context['most_rated'] = most_rated
        context['form'] = SearchForm
        # context["order"] = get_or_set_order_session(self.request)
        context['title'] = 'Ebisco | fashionz'
        context['home_active'] = 'active_link'
        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'ecommerce/contact.html'
    success_url = reverse_lazy('ecomm:contact')

    def form_valid(self, form):
        messages.info(
            self.request, "Thanks for getting in touch with us, we receieved your message.")
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        full_name = f'{first_name} {last_name}'

        full_message = f"""
         Recieved message below from {full_name}, {email}
         ____________________________________
         {message}
        """
        send_mail(
            subject='Recieved contact us information',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["order"] = get_or_set_order_session(self.request)
        context["title"] = 'Ebisco | Contact Us'
        context["contact_active"] = True
        return context


# class view for search results
class SearchResults(ListView):
    paginate_by = 8
    template_name = 'ecommerce/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.filter(active=True)
        search = self.request.GET.get('search')
        return products.filter(
            Q(title__icontains=search) |
            Q(tags__name__icontains=search) |
            Q(categories__name__icontains=search)).distinct()

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ebisco | Search products'
        context["search"] = search
        return context


def searchProducts(request):
    products = Product.objects.filter(active=True)
    if request.method == "GET":
        search = request.GET.get('search')
        queryset = products.filter(
            Q(title__icontains=search) |
            Q(tags__name__icontains=search) |
            Q(categories__name__icontains=search)).distinct()
        page = request.GET.get('page')
        paginator = Paginator(queryset, 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    context = {
        'search': search,
        # 'form': form,
        'products': products,
        'title': 'Ebisco Fashionz | search results',
    }
    return render(request, 'ecommerce/search.html', context)


# def searchProducts(request):

#     search = request.GET.get('search')
#     products = Product.objects.filter(active=True)
#     # queryset = products
#     # paginator = Paginator(queryset, 1)
#     # try:
#     #     queryset = paginator.page(page)
#     # except EmptyPage:
#     #     queryset = paginator.page(paginator.num_pages)

#     if search:
#         queryset = []
#         page = request.GET.get('page', 1)
#         queryset = products.filter(
#         Q(title__icontains=search) |
#         Q(tags__name__icontains=search) |
#         Q(categories__name__icontains=search)).distinct()
#         paginator = Paginator(queryset, 1)
#         queryset = paginator.page(page)
#     else:
#         queryset = None

#     context = {
#         'search': search,
#         'products': queryset,
#         'title': 'Ebisco Fashionz | search results',
#     }
#     return render(request, 'ecommerce/search.html', context)
