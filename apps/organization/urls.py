#_*_encoding:utf-8_*_

from django.conf.urls import url,include

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherView,TeacherDetailView

urlpatterns=[
    url(r'^list/$',OrgView.as_view(),name="org_list"),
    url(r'^add_ask/$',AddUserAskView.as_view(),name="add_ask"),
    url(r'home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name="org_home"),
    url(r'course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name="org_courses"),
    url(r'desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name="org_desc"),
    url(r'teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name="org_teachers"),

    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    url(r'^teacher/$',TeacherView.as_view(),name="teachers"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(),name='teacher_detail')

]