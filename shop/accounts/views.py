from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import views as auth_views
# Model
from accounts.models import CustomProfileModel, CustomUser
# Form
from accounts.forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm, UserChangePassForm,CustomUserForm
# Permissions
#
from shop.models import Order, OrderItem
#


# Create your views here.

#Signup
class SignUpView(generic.CreateView):

    """ 
        A class is for the registration form and 
        page where the user must enter the relevant information
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts:signin1')
    template_name = 'accounts/signuppage.html'
    success_message = 'حساب کاربری با موفقیت ساخته شد'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


#Login
class LoginUserView(LoginView):

    """
        The task of this class is to authenticate the user
    """

    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_message = 'با موفقیت وارد شدید'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        user = form.get_user()
        if not CustomProfileModel.objects.filter(user=user).exists():
            CustomProfileModel.objects.create(user=user)
        return response

    def get_success_url(self):
        return reverse('home:home1')
    
# LogOut
class UserLogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:signin1')


#UpdateInformation
class UserProfileView(LoginRequiredMixin,View) :



    template_name = 'accounts/profile.html'
    login_required = True
    def get(self, request, *args, **kwargs):
        try:
            profile = CustomProfileModel.objects.get(user=request.user)
        except CustomProfileModel.DoesNotExist:
            raise Http404("مشخصات کاربری پیدا نشد.")
        context = {
            'profile': profile,

        }
        return render(request, self.template_name, context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    

    """
        The task of this class is to allow the 
        user to record or even edit personal information
    """

    template_name = 'accounts/updateuser.html'
    success_url = reverse_lazy('accounts:profile1')

    def get(self, request, *args, **kwargs):
        user_form = CustomUserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.customprofilemodel)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.customprofilemodel)

        if user_form.is_valid() and profile_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.is_complete = True
            profile_instance.save()
            messages.success(request, 'اطلاعات شما با موفقیت ذخیره شد')
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form
            })

class UserChangePasswordView(LoginRequiredMixin ,auth_views.PasswordChangeView) : 

    """
        The user can change the account password
    """

    form_class = UserChangePassForm
    template_name = 'accounts/Changepass.html'
    login_url = ('accounts:signin1')
    success_url = reverse_lazy('accounts:profile1')




class UserAddressView(LoginRequiredMixin, View) : 

    """
        Add user address information to the page
    """

    def get(self, request) : 
        user = request.user
        user_info_address = CustomProfileModel.objects.get(user_id = user)
        context = {
            'profile' : user_info_address,
        }
        return render(request, 'accounts/newaddres.html',context)


class UserOrderView(View):
    
    """
        The user's previous order history
    """
    
    template_name = 'accounts/order_list.html'
    def get(self, request): 
        user = request.user
        orders = Order.objects.filter(customer=user).prefetch_related('orderitem_set__product')
        user_info_address = CustomProfileModel.objects.get(user_id = user)
        context =  {
            'orders': orders,
            'profile' : user_info_address,
        }
        return render(request, self.template_name ,context)
