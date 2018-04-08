# _*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from operation.models import UserAsk, UserFavorite
from courses.models import Course


# Create your views here.
class OrgView(View):
    # 课程机构列表功能
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("click_nums")[:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 筛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "course_nums":
                all_orgs = all_orgs.order_by("-course_nums")

        # 课程计数
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "sa":"org",
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            # name=request.POST.get("name","")
            # phone=request.POST.get("phone","")
            # course_name=request.POST.get("course_name","")
            #
            # user_ask = UserAsk()
            # user_ask.name = name
            # user_ask.phone=phone
            # user_ask.course_name=course_name
            # user_ask.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):

        course_org = CourseOrg.objects.get(id=int(org_id))

        #显示是否收藏
        has_fav = False
        msg = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                msg="已收藏"


        all_courses = course_org.course_set.all()[0:3]
        all_teachers = course_org.teacher_set.all()[0:1]
        if all_teachers:
            teacher_courses = all_teachers[0].course_set.all()[0:1]
        else:
            teacher_courses = []
        statue = "home"
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "teacher_courses": teacher_courses,
            "course_org": course_org,
            "statue": statue,
            "msg":msg
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)

        # 显示是否收藏
        has_fav = False
        msg = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                msg = "已收藏"


        all_courses = course_org.course_set.all()
        statue = "course"
        # 对机构所有课程进行分页
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #
        # # Provide Paginator with the request object for complete querystring generation
        #
        # p = Paginator(org_all_courses, 4, request=request)
        #
        # courses = p.page(page)
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses,
            "course_org": course_org,
            "statue": statue,
            "msg":msg
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 显示是否收藏
        has_fav = False
        msg = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                msg = "已收藏"



        statue = "describe"
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "statue": statue,
            "msg": msg
        })


class OrgTeacherView(View):
    """
    机构教师
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 显示是否收藏
        has_fav = False
        msg = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                msg = "已收藏"


        all_teachers = course_org.teacher_set.all()
        statue = "teachers"
        return render(request, "org-detail-teachers.html", {
            "all_teachers": all_teachers,
            "course_org": course_org,
            "statue": statue,
            "msg": msg
        })


class AddFavView(View):
    """
    用户收藏，二次点击认为是取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登陆
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user=request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')

