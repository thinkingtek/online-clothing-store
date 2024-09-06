import random
import string
from .models import Order


# update the subtotal and overal total in Orders
def updateOrederedPrice(order):
    if order.ordered is False:
        order.ordered_subtotal = order.get_subtotal()
        order.ordered_overall_total = order.get_overall_total()


# cart session
def get_or_set_order_session(request):
    order_id = request.session.get('order_id', None)

    if order_id is None:
        order = Order()
        order.save()
        request.session['order_id'] = order.pk
    else:
        try:
            order = Order.objects.get(pk=order_id, ordered=False)
        except Order.DoesNotExist:
            order = Order()
            order.save()
            request.session['order_id'] = order.pk

    if request.user.is_authenticated and order.user is None:
        order.user = request.user
        order.save()
    return order


# generate reference code for orders
def create_ref_code():

    return "".join(random.choices(string.ascii_lowercase + string.digits, k=15))


# getting the order count
def cart_item_count(request):
    order = get_or_set_order_session(request)
    if order:
        count = order.items.count()
        return count
