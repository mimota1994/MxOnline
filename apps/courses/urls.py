#_*_encoding:utf-8_*_
from django.conf.urls import url,include

from .views import CourseView,CourseDetailView

urlpatterns=[
    url(r'^list/',CourseView.as_view(),name="course_list"),
    url(r'detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name="course_detail")
]