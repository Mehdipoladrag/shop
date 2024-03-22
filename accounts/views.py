from django.shortcuts import render, redirect
from accounts.models import CustomProfileModel, CustomUser
from accounts.forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm, UserChangePassForm
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
#from accounts.serializers import ProfileSerializer,UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from shop.models import Order, OrderItem
# Create your views here.

#Signup
class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts:signin1')
    template_name = 'accounts/signuppage.html'
    success_message = 'حساب کاربری با موفقیت ساخته شد'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
#Login
class LoginUserView(LoginView) : 
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
        return reverse_lazy('home:home1')
    
# LogOut
class UserLogOutView(LoginRequiredMixin,LogoutView):
    login_required = True 
    next_page = reverse_lazy('accounts:signin1')


#UpdateInformation
class UserProfileView(LoginRequiredMixin,View) :
    template_name = 'accounts/profile.html'
    login_required = True
    def get(self, request, *args, **kwargs):
        try:
            profile = CustomProfileModel.objects.get(user=request.user)
        except CustomProfileModel.DoesNotExist:
            raise Http404("مشخصات کاربری پیدا نشد.")
        
        #orders_count = Order.objects.filter(customer=request.user).count()
        context = {
            'profile': profile,
          #  'orders_count': orders_count,
        }
        return render(request, self.template_name, context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomProfileModel
    form_class = ProfileUpdateForm
    template_name = 'accounts/updateuser.html'
    success_url = reverse_lazy('accounts:profile1')

    def get_object(self):
        return self.request.user.customprofilemodel

    def form_valid(self, form):
        # بررسی تکمیل بودن پروفایل و ذخیره تغییرات
        profile = form.save(commit=False)
        if profile.is_complete:
            profile.is_complete = True
        profile.save()
        messages.success(self.request, 'اطلاعات شما با موفقیت ذخیره شد')
        return super().form_valid(form)


class UserChangePasswordView(PasswordChangeView) : 
    form_class = UserChangePassForm
    template_name = 'accounts/Changepass.html'
    login_required = True
    
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