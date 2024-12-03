from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from account.tasks import delete_inactive_users

User = get_user_model()


# class Command(BaseCommand):
#     help = "Delete unverified users every 1minutes"

#     def handle(self, *args, **kwargs):
#         delete_inactive_users(repeat=60)

# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         unverified_users = User.objects.filter(email_verified=False)
#         for user in unverified_users:
#             start_date = user.date_joined
#             end_date = start_date + timedelta(minutes=2)
#             if end_date < now():
#                 user.delete()
#                 print("User deleted")


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         print("====== cron command running -=======")
