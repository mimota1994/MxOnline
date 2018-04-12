#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetpwdForm,ModeifyPwdForm,UserModeifyForm,UserImageForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))#get 只能get到一个
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    def get(self,request):
        return render(request,"login.html",{})

    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html",{"user_name":user_name})
                else:
                    return render(request,"login.html",{"msg":"用户未激活"})
            else:
                return render(request,"login.html",{"msg":"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class LogOutView(View):
    def get(self,request):
        logout(request)
        return render(request,'index.html')


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{"register_form":register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name=request.POST.get("email","")
            pass_word=request.POST.get("password","")
            user=UserProfile.objects.filter(email=user_name)
            if user:
                return  render(request,"register.html",{"msg":"用户已存在","register_form":register_form})
            else:
                user_profile=UserProfile()
                user_profile.username=user_name
                user_profile.email=user_name
                user_profile.password=make_password(pass_word)
                user_profile.is_active=0
                user_profile.save()

                send_register_email(user_name,"register")
                return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")

class ForgetpwdView(View):
    def get(self,request):
        forgetpwd_form=ForgetpwdForm(request.POST)
        return render(request,"forgetpwd.html",{"forgetpwd_form":forgetpwd_form})

    def post(self,request):
        forgetpwd_form=ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email=request.POST.get("email","")
            user=UserProfile.objects.filter(email=email)
            if user:
                send_register_email(email,send_type="forget")
                return render(request,"send_success.html")
            else:
                return render(request,"forgetpwd.html",{"msg":"用户不存在"})
        else:
            return render(request,"forgetpwd.html",{"forgetpwd_form":forgetpwd_form})

class ResetView(View):
    def get(self,request,reset_code):
        all_records=EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email=record.email
            return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"active_fail.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModeifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1","")
            pwd2=request.POST.get("password2","")
            email=request.POST.get("email","")
            if pwd1!=pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd1)
            user.save()
            return render(request,"login.html")
        else:
            email=request.POST.get("email","")
            return render(request,"password_reset.html",{"email":email,"modify_form":modify_form})


#个人主页
class UserCenterInfoView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'usercenter-info.html', {

            })

    def post(self,request):
        user_modeify_form=UserModeifyForm(request.POST)
        if user_modeify_form.is_valid():
            nick_name = request.POST.get("nick_name", "")
            gender = request.POST.get("gender", "")
            address = request.POST.get("address", "")
            birthday = request.POST.get("birthday", "")
            mobile = request.POST.get("mobile", "")
            email = request.POST.get("email", "")

            if request.user.is_authenticated():
                user=request.user
                user.nick_name=nick_name
                user.gender = gender
                user.address = address
                user.birthday = birthday
                user.mobile =mobile
                user.email = email
                user.save

        user_image_form=UserImageForm(request.POST)
        if user_image_form.is_valid():
            image=request.POST.get('image','')


            return render(request,'usercenter-info.html',{

            })

            #     if user is not None:
            #         if user.is_active:
            #             login(request, user)
            #             return render(request, "index.html", {"user_name": user_name})
            #         else:
            #             return render(request, "login.html", {"msg": "用户未激活"})
            #     else:
            #         return render(request, "login.html", {"msg": "用户名或密码错误"})
            # else:
            #     return render(request, "login.html", {"login_form": login_form})
# Create your views here.


