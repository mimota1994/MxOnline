#_*_encoding:utf-8_*_
from django.conf.urls import url,include

from .views import CourseView

urlpatterns=[
    url(r'^list/$',CourseView.as_view(),name="course_list"),
]