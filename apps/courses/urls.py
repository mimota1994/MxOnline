#_*_encoding:utf-8_*_
from django.conf.urls import url,include

from .views import CourseView,CourseDetailView,AddLearnView,CourseVideoView,CourseCommentView,AddCommentView,VideoView

urlpatterns=[
    url(r'^list/',CourseView.as_view(),name="course_list"),
    url(r'detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name="course_detail"),
    url(r'addlearn/$', AddLearnView.as_view(), name="addlearn"),
    url(r'video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="video"),
    url(r'comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(),name="comment"),
    url(r'add_comment/',AddCommentView.as_view(),name='add_comment'),
    url(r'video_things/(?P<video_id>\d+)/$',VideoView.as_view(),name="video_things"),
]