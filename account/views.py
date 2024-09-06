from asyncio.windows_events import NULL
from django.urls import reverse_lazy
from .mixins import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
# from .forms import LoginForm, UserRegForm, UserUpdateForm, ProfileUpdateForm
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View
from .decorators import *
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from cart.models import Order
from django.contrib.auth import authenticate, get_user_model, login, logout
from datetime import timedelta, date
User = get_user_model()


def deleteInactiveUsers(request):
    users = User.objects.filter(is_active=False)
    today = date.today()
    for user in users:
        start_date = user.date_joined.date()
        end_date = start_date + timedelta(days=2)

        if end_date < today:
            User.objects.get(pk=user.pk).delete()
    return render(request, 'account/delete_inactive_users.html')


@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.instance.first_name = form.cleaned_data.get(
                'first_name').title()
            form.instance.last_name = form.cleaned_data.get(
                'last_name').title()
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
            return render(request, 'account/email_sent.html')
    else:
        form = UserRegForm()

    context = {
        'title': 'Sign-up',
        'form': form
    }
    return render(request, 'account/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        user.save()
        messages.success(
            request, f'{user.full_name} your account have been successfully activated  you can now login')
        return redirect('login')
    else:
        return HttpResponse('registered succesfully and activation sent')
        # return render(request, 'account/activation_invalid.html')


@redirect_authenticated_user
def loginView(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('ecomm:home')
    else:
        form = UserLoginForm()

    context = {'title': 'Login | Ebisco Fahion', 'form': form}
    return render(request, 'account/login.html', context)


@redirect_unauthenticated_user
def userLogout(request):
    messages.info(
        request, f"{request.user.full_name} You have successfully logged out")
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    user = request.user
    email = request.user.email
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'email': email,
        'title': f'{user.first_name} | Profile',
        'u_form': u_form,
        'p_form': p_form,
        'profile_active': True,
        'orders': Order.objects.filter(user=user, ordered=True)
    }
    return render(request, 'account/profile.html', context)


class PasswordChange(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password-change-done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'
    success_url = reverse_lazy('password-change-done')


class ResetPassword(RedirectAuthUser, SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = PasswordFormReset
    success_url = reverse_lazy('password-reset')
    success_message = 'An instruction has been sent to your email with  to reset your account password'


class ResetPasswordConfirm(RedirectAuthUser, PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password-reset-complete')


class ResetPasswordComplete(RedirectAuthUser, PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class ResetDoneView(RedirectAuthUser, PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    # This view isnt in use because i did a redirect to the same view that sent the email address which is PasswordResetView. But its just here just incase i decide to use it
