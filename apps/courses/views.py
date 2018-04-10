#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite

# Create your views here.
class CourseView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by("add_time")
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
            elif sort == "students":
                all_courses = all_courses.order_by("-students")

        # 课程计数
        course_nums = all_courses.count()

        # 热门课程
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)


        return render(request,"course-list.html",{
            'sa':'course',
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort':sort
            })


class CourseDetailView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))

        #点击数逻辑
        course.click_nums=course.click_nums+1
        course.save()

        #课程机构收藏显示
        org_msg="收藏"
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,fav_type=2):
                org_msg="已收藏"


        course_msg = "收藏"
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_msg = "已收藏"

        #推荐课程
        relate_courses=[]
        tag=course.tag
        if tag:
            relate_courses=Course.objects.filter(tag=tag)
            relate_courses=relate_courses.exclude(id=course_id)

        return render(request,'course-detail.html',{
            'course':course,
            'course_id':course_id,
            'course_msg':course_msg,
            'org_msg':org_msg,
            'related_courses':relate_courses
        })

