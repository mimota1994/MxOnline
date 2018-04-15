#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator,PageNotAnInteger

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetpwdForm,ModeifyPwdForm,UserModeifyForm,UserImageForm
from utils.email_send import send_register_email
from operation.models import UserFavorite,UserMessage
from courses.models import Course
from organization.models import Teacher,CourseOrg


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
                'four_in_one': 'info'

            })

    def post(self,request):
        user_modeify_form=UserModeifyForm(request.POST)
        nick_name = request.POST.get("nick_name", "")
        gender = request.POST.get("gender", "")
        address = request.POST.get("address", "")
        birthday = request.POST.get("birthday", "")
        mobile = request.POST.get("mobile", "")
        email = request.POST.get("email", "")
        if user_modeify_form.is_valid():
            nick_name = request.POST.get("nick_name", "")
            gender = request.POST.get("gender", "")
            address = request.POST.get("address", "")
            birthday = request.POST.get("birthday", "")
            mobile = request.POST.get("mobile", "")
            email = request.POST.get("email", "")

            if request.user.is_authenticated():
                user=UserProfile.objects.get(id=request.user.id)
                user.nick_name=nick_name
                user.gender = gender
                user.address = address
                user.birthday = birthday
                user.mobile =mobile
                user.email = email
                user.save()


                return render(request, 'usercenter-info.html', {


                })



class MyCourseView(View):
    def get(self,request):
        if request.user.is_authenticated():
            all_courses_id=request.user.usercourse_set.all()
            all_courses=[]
            for id in all_courses_id:
                all_courses.append(id.course)

            return render(request,'usercenter-mycourse.html',{
                'all_courses':all_courses,
                'four_in_one': 'course'
            })


class MyFavCourseView(View):
    def get(self,request):
        if request.user.is_authenticated():
            user_id=request.user.id
            all_fav_id=UserFavorite.objects.filter(user_id=user_id,fav_type=1)
            all_courses=[]
            for id in all_fav_id:
                all_courses.append(Course.objects.get(id=id.fav_id))


            return render(request,'usercenter-fav-course.html',{
                'all_courses':all_courses,
                'four_in_one': 'fav'
            })


class MyFavOrgView(View):
    def get(self,request):
        if request.user.is_authenticated():
            user_id=request.user.id
            all_fav_id=UserFavorite.objects.filter(user_id=user_id,fav_type=2)
            all_orgs=[]
            for id in all_fav_id:
                all_orgs.append(CourseOrg.objects.get(id=id.fav_id))

            return render(request,'usercenter-fav-org.html',{
                "all_orgs":all_orgs,
                'four_in_one':'fav'
            })


class MyFavTeacherView(View):
    def get(self,request):
        if request.user.is_authenticated():
            user_id = request.user.id
            all_fav_id = UserFavorite.objects.filter(user_id=user_id, fav_type=3)
            all_teachers = []

            for id in all_fav_id:
                all_teachers.append(Teacher.objects.get(id=id.fav_id))

            return render(request,'usercenter-fav-teacher.html',{
                'all_teachers':all_teachers,
                'four_in_one': 'fav'
            })

class MyMessageView(View):
    def get(self,request):
        if request.user.is_authenticated():
            user_id = request.user.id
            all_messages=UserMessage.objects.filter(user=user_id).order_by('-add_time')


            #分页
            try:
                page=request.GET.get('page',1)
            except PageNotAnInteger:
                page=1

            p=Paginator(all_messages,8,request=request)

            message=p.page(page)

            for mes in message.object_list:
                mes.has_read=True
                mes.save()

            not_read_nums = UserMessage.objects.filter(user=user_id, has_read=False).count()

        return render(request,'usercenter-message.html',{
            'four_in_one':'message',
            'all_messages':message,
            'not_read_nums':not_read_nums
        })


class ImageUploadView(View):
    def post(self,request):
        image_form=UserImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image=image_form.files['image']
            request.user.image=image
            request.user.save()
            return render(request, 'usercenter-info.html', {

            })

