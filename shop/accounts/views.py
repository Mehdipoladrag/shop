from django.shortcuts import render, redirect
# Model
from accounts.models import CustomProfileModel, CustomUser
# Form
from accounts.forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm, UserChangePassForm,CustomUserForm
# Serializers
from accounts.serializers import ProfileSerializer, UserSerializer, LoginSerializer
# Permissions
from accounts.permissions import IsSuperUser
from rest_framework.permissions import AllowAny, IsAdminUser
#
from shop.models import Order, OrderItem
#
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import views as auth_views
# For APIS
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
# Manage Login with username 
    # add Email for Login Users
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
        
        #orders_count = Order.objects.filter(customer=request.user).count()
        context = {
            'profile': profile,
          #  'orders_count': orders_count,
        }
        return render(request, self.template_name, context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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
    form_class = UserChangePassForm
    template_name = 'accounts/Changepass.html'
    login_url = ('accounts:signin1')
    success_url = reverse_lazy('accounts:profile1')




class UserAddressView(LoginRequiredMixin, View) : 
    def get(self, request) : 
        user = request.user
        user_info_address = CustomProfileModel.objects.get(user_id = user)
        context = {
            'profile' : user_info_address,
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

## API Custom Profile
class ProfileUSerlistmixin(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView) :
    queryset = CustomProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSuperUser]
    def get(self, request) : 
        return self.list(request) 
    def post(self, request) :
        return self.create(request)
class ProfileDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView) :
    queryset = CustomProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSuperUser]
    def get(self, request, pk) :
        return self.retrieve(request, pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request, pk) :
         return self.destroy(request,pk)
    
# User API 
class UserListmixin(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView) :
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['username']
    search_fields = ['username']
    ordering_fields = ['username', 'email']
    ordering_fields = '__all__'
    def get(self, request) : 
        return self.list(request) 
    def post(self, request) :
        return self.create(request)
    
class UserDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView) :
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk) :
        return self.retrieve(request, pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request, pk) :
         return self.destroy(request,pk)
    
class LoginAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    