from django.shortcuts import render, redirect
from accounts.models import PROFILE
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm,UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.



def signup_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(username=data['user_name'], email=data['email'], first_name=data['first_name'],
                                     last_name=data['last_name'], password=data['password2'])
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
            return redirect('accounts:signin1')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signuppage.html', {'form': form})


def signin_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(
                    email=data['user_name'], password=data['password1']))

            except:
                user = authenticate(
                    request, username=data['user_name'], password=data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید!')
                return redirect("home:home1")
            else:
                messages.error(request, 'رمز یا نام کاربری اشتباه است')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('accounts:signin1')


@login_required(login_url='accounts:signin1')
def user_profile(request):
    profile = PROFILE.objects.get(user_id=request.user.id)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required(login_url='accounts:signin1')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'اطلاعات شما با موفقیت ذخیره شد')
            return redirect('accounts:profile1')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/updateuser.html', context)


@login_required(login_url='accounts:signin1')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'رمز تغییر یافت')
            return redirect('accounts:profile1')
        else:
            messages.error(request, 'رمز اشتباه است')
            return redirect('accounts:change1')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/Changepass.html', {'form': form})


def new_address(request) :
    profile = PROFILE.objects.get(user_id=request.user.id)
    return render(request, 'accounts/newaddres.html',{'profile': profile})