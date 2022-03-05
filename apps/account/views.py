from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserForm
from django.contrib import messages


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
            login(request, user)
            next_url = request.POST.get('next')
            return redirect(next_url)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', context={'form': form, 'next': request.GET.get('next') or 'homepage'})
