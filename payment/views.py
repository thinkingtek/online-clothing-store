import json
from .mixins import RedirectZeroItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from cart.forms import *
from .models import *
from django.urls import reverse_lazy
from .models import Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib import messages
from cart.models import Order
from django.conf import settings
from cart.utils import get_or_set_order_session, create_ref_code
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView, TemplateView, FormView


class SelectPayment(LoginRequiredMixin, RedirectZeroItem, TemplateView):
    template_name = "payment/select-payment.html"

    def get_context_data(self, **kwargs):
        order = get_or_set_order_session(self.request)
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Payment"
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context["PAYSTACK_PUBLIC_KEY"] = settings.PAYSTACK_PUBLIC_KEY
        context["PAYSTACK_SECRET_KEY"] = settings.PAYSTACK_SECRET_KEY
        context["total_amount_kobo"] = order.ordered_overall_total * 100
        context["order"] = get_or_set_order_session(self.request)
        context["REVERSE_URL"] = reverse("cart:orders")
        return context


class ConfirmOrder(View):

    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        print(body)
        Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            reference=body["reference"],
            amount=order.get_overall_total(),
            payment_method='paystack'
        )
        order.ordered = True
        order.ref_code = create_ref_code()
        order.ordered_date = timezone.now()
        order.save()
        return JsonResponse({"data": "success"})


class ThankYou(TemplateView):
    template_name = 'cart/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ebisco | Thanks for payment"
        context["CALLBACK_URL"] = reverse("cart:thank-you")
        return context


class RequestRefund(LoginRequiredMixin, FormView):
    template_name = 'cart/request-refund.html'
    form_class = RefundForm
    success_url = reverse_lazy('cart:orders')

    def form_valid(self, form):
        ref_code = form.cleaned_data.get('ref_code')
        message = form.cleaned_data.get('message')
        order = Order.objects.get(ordered=True, ref_code=ref_code)
        order.request_refund = True
        order.save()
        refund = Refund(
            order=order,
            reason=message,
            user=self.request.user
        )
        refund.save()
        messages.info(
            self.request, f'Request for this order has been receieved we will get back to you in no time')
        return redirect('cart:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.request.user} | Request refund"
        context["profile_active"] = True
        return context
