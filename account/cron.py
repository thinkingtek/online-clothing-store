
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()


# def delete_users(self, *args, **options):
#     unverified_users = User.objects.filter(email_verified=False)
#     for user in unverified_users:
#         start_date = user.date_joined
#         end_date = start_date + timedelta(minutes=2)
#         if end_date < now():
#             user.delete()
#             print("User deleted")

# def delete_users():
#     unverified_users = User.objects.filter(email_verified=False)
#     for user in unverified_users:
#         user.delete()
#         print("User deleted")


def delete_users():
    print("=====  User deleted =======")
