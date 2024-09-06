from django.shortcuts import redirect
from .utils import get_or_set_order_session


class RedirectZeroItem(object):
    def dispatch(self, request, *args, **kwargs):
        order = get_or_set_order_session(self.request)
        if order.items.all().count() < 1:
            return redirect("cart:cart-items")
        return super().dispatch(request, *args, **kwargs)
