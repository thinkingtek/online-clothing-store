from background_task import background
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from cart.models import Order

User = get_user_model()


# func to delete unpaid orders after 30days
@background(schedule=100)
def delete_unpaid_orders():
    print("=========== Unpaid orders started running ============")
    orders = Order.objects.filter(ordered=False)
    for order in orders:
        start_date = order.created_at
        end_date = start_date + timedelta(days=30)
        if end_date < now():
            order.delete()
            print("==== Unpaid Order deleted after 30days ========")


# This function is made to delete users whose email is'nt verified after signup, it is Schedule to run in the next 5mins from when started
@background(schedule=300)
def delete_unverified_users():
    print("=========== deleting users function started running ============")
    unverified_users = User.objects.filter(email_verified=False)
    for user in unverified_users:
        start_date = user.date_joined
        end_date = start_date + timedelta(days=10)
        if end_date < now():
            user.delete()
            print("==== Email not verified yet, so User deleted ===========")
