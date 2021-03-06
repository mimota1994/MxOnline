#_*_encoding:utf-8_*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from users.views import LoginView,RegisterView,ActiveUserView,ForgetpwdView,ResetView,ModifyPwdView,LogOutView
from organization.views import OrgView
from operation.views import IndexView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',IndexView.as_view(),name="index"),
    url('^login/$',LoginView.as_view(),name="login"),
    url('^logout/$',LogOutView.as_view(),name="logout"),
    url('^register/',RegisterView.as_view(),name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),
    url(r'forget/$',ForgetpwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$',ResetView.as_view(),name="reset_pwd"),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name="modify_pwd"),

    #课程机构首页
    url(r'^org/',include('organization.urls',namespace="org")),

    #课程列表首页
    url(r'course/',include('courses.urls',namespace="course")),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$',serve,{"document_root":MEDIA_ROOT}),

    #个人相关
    url(r'user/',include('users.urls',namespace='user'))

    #机构详情列表
    #url(r'^org/$',OrgDetailHomePageView.as_view(),name="org-detail-homepage")


]
