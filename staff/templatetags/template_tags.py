from tokenize import group
from django import template
from account.views import register
from django.contrib.auth.models import Group
from cart.utils import get_or_set_order_session


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter
def cart_item_count(request):
    order = get_or_set_order_session(request)
    count = order.items.count()
    return count
