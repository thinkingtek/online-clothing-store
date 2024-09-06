from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.groups.filter(name="staff").exists():
            return redirect("ecomm:home")
        return super().dispatch(request, *args, **kwargs)
