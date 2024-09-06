from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def redirect_unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(
                request, "You've not logged-In'")
            return redirect('ecomm:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def redirect_authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(
                request, "You can't access the sign-In page while logged-in")
            return redirect('ecomm:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('accounts:user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
