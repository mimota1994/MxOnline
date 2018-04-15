#_*_encoding:utf-8_*_
from django.conf.urls import url

from .views import UserCenterInfoView,MyCourseView,MyFavCourseView,MyFavOrgView,MyFavTeacherView,MyMessageView,ImageUploadView

urlpatterns=[
    url(r'info/',UserCenterInfoView.as_view(),name='info'),

    url(r'mycourses/',MyCourseView.as_view(),name='my_courses'),

    url(r'myfavcourse/',MyFavCourseView.as_view(),name='my_fav_courses'),

    url(r'myfavorg/',MyFavOrgView.as_view(),name='my_fav_org'),

    url(r'myfavteacher/',MyFavTeacherView.as_view(),name='my_fav_teacher'),

    url(r'mymessage/',MyMessageView.as_view(),name='message'),

    #上传图片
    url(r'image/upload/',ImageUploadView.as_view(),name='image_upload'),
]