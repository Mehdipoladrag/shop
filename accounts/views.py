from django.http import HttpResponse
from django.shortcuts import render, redirect
#from accounts.models import PROFILE, Message
#from accounts.forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm,UserUpdateForm
from accounts.forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, mixins
#from accounts.serializers import ProfileSerializer,UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from shop.models import Order, OrderItem
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts:signin1')
    template_name = 'accounts/signuppage.html'
    success_message = 'حساب کاربری با موفقیت ساخته شد'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class LoginUserView(LoginView) : 
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_message = 'با موفقیت وارد شدید'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def get_success_url(self):
        return reverse_lazy('home:home1')
    
def signin_page(request):
    # if request.method == 'POST':
    #     form = UserLoginForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         try:
    #             user = authenticate(request, username=User.objects.get(
    #                 email=data['user_name'], password=data['password1']))

    #         except:
    #             user = authenticate(
    #                 request, username=data['user_name'], password=data['password1'])
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, 'با موفقیت وارد شدید!')
    #             return redirect("home:home1")
    #         else:
    #             messages.error(request, 'رمز یا نام کاربری اشتباه است')
    # else:
    #     form = UserLoginForm()
    return render(request, 'accounts/login.html') #{'form': form})

class UserLogOutView(LogoutView):
    next_page = reverse_lazy('accounts:signin1')

# def user_logout(request):
#     logout(request)
#     messages.success(request, 'با موفقیت خارج شدید')
#     return redirect('accounts:signin1')


@login_required(login_url='accounts:signin1')
def user_profile(request):
    # profile = PROFILE.objects.get(user_id=request.user.id)
    # user = request.user
    # message_user = Message.objects.filter(user=user).count()
    # orders = Order.objects.filter(customer=user).count()
    # context =  {
    #     'profile': profile,
    #     'message_user' : message_user,
    #     'orders' : orders,
    # }
    return render(request, 'accounts/profile.html')


@login_required(login_url='accounts:signin1')
# views.py
def user_update(request):
    # if request.method == 'POST':
    #     user_form = UserUpdateForm(request.POST, instance=request.user)
    #     profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'اطلاعات شما با موفقیت ذخیره شد')
    #         return redirect('accounts:profile1')
    # else:
    #     user_form = UserUpdateForm(instance=request.user)
    #     profile_form = ProfileUpdateForm(instance=request.user.profile)
    # context = {
    #     'user_form': user_form,
    #     'profile_form': profile_form
    # }
    return render(request, 'accounts/updateuser.html')

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
            return redirect('accounts:profile1')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/Changepass.html', {'form': form})


def new_address(request) :
    #profile = PROFILE.objects.get(user_id=request.user.id)
    user = request.user
    #message_count = Message.objects.filter(user=user).count()
    orders = Order.objects.filter(customer=user).count()
    context = {
    #    'profile': profile,
        'orders': orders,
   #     'message_count': message_count,
    }
    return render(request, 'accounts/newaddres.html',context)

def order_list(request):
    user = request.user
    #message_count = Message.objects.filter(user=user).count()
    orders = Order.objects.filter(customer=user).prefetch_related('orderitem_set__product')
    
    context =  {
        'orders': orders,
     #   'message_count': message_count,
    }
    return render(request, 'accounts/order_list.html',context)

def user_message_info(request) :
    user = request.user 
   # messages = Message.objects.filter(user=user)
    orders = Order.objects.filter(customer=user).count()
    context = {
        'message_user' : messages,
        'orders': orders,
    }
    return render(request,'accounts/message_user.html', context)

## API
# class ProfilePermission(IsAdminUser) : 
#     pass 
# class ProfileUSerlistmixin(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ProfilePermission) :
#     queryset = PROFILE.objects.all()
#     serializer_class = ProfileSerializer
#     def get(self, request) : 
#         return self.list(request) 
#     def post(self, request) :
#         return self.create(request)
# class ProfileDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView,ProfilePermission) :
#     queryset = PROFILE.objects.all()
#     serializer_class = ProfileSerializer
#     def get(self, request, pk) :
#         return self.retrieve(request, pk) 
#     def put(self, request, pk) :
#         return self.update(request,pk)
#     def delete(self, request, pk) :
#          return self.destroy(request,pk)
    
# ###### User 
# class UserListmixin(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ProfilePermission) :
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
#     filterset_fields = ['username']
#     search_fields = ['username']
#     ordering_fields = ['username', 'email']
#     ordering_fields = '__all__'
#     def get(self, request) : 
#         return self.list(request) 
#     def post(self, request) :
#         return self.create(request)
# class UserDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView,ProfilePermission) :
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def get(self, request, pk) :
#         return self.retrieve(request, pk) 
#     def put(self, request, pk) :
#         return self.update(request,pk)
#     def delete(self, request, pk) :
#          return self.destroy(request,pk)