from audioop import reverse
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings

from apps.account.models import Account
from .forms import RegistrationForm, UserForm
from apps.account.utils import generate_token


def home(request):
    return render(request, 'base.html')

def send_activation_email(user: Account, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/verify.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    EmailMessage(
        subject=email_subject, 
        body=email_body, 
        from_email=settings.EMAIL_FROM_USER, 
        to=[user.email]
    )


def log_user_in(request):
    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = UserForm()
    return render(request, 'accounts/login.html', context={'form':form})


def log_user_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or 'homepage'
        return redirect(next_url)
    if request.method == 'POST':
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            user.save()
            send_activation_email()
            login(request, user)
            next_url = request.POST.get('next')
            return redirect(next_url)
        else:
            form = RegistrationForm(request.POST,request.FILES)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', context={'form': form, 'next': request.GET.get('next') or 'homepage'})


def activate_user(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = Account.objects.get(pk=uid)
    except Exception as e:
        user=None

    if user and generate_token.check_token(user, token):
        user.is_email_verified=True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, you can login now')
        return redirect(reverse('login'))

    return render(request, 'accounts/activation-failed.html', {'user': user})