#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


from .models import CourseOrg,CityDict
from .forms import UserAskForm
from operation.models import UserAsk
from courses.models import Course

# Create your views here.
class OrgView(View):
    #课程机构列表功能
    def get(self,request):
        #课程机构
        all_orgs=CourseOrg.objects.all()
        hot_orgs=all_orgs.order_by("click_nums")[:3]
        #城市
        all_citys=CityDict.objects.all()

        #筛选类别
        category=request.GET.get('ct','')
        if category:
            all_orgs=all_orgs.filter(category=category)

        #筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        sort=request.GET.get('sort',"")
        if sort:
            if sort =="students":
                all_orgs=all_orgs.order_by("-students")
            elif sort == "course_nums":
                all_orgs=all_orgs.order_by("-course_nums")

        #课程计数
        org_nums=all_orgs.count()

        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,2, request=request)

        orgs = p.page(page)
        return render(request,"org-list.html",{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })



class AddUserAskView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            userask=userask_form.save(commit=True)
            # name=request.POST.get("name","")
            # phone=request.POST.get("phone","")
            # course_name=request.POST.get("course_name","")
            #
            # user_ask = UserAsk()
            # user_ask.name = name
            # user_ask.phone=phone
            # user_ask.course_name=course_name
            # user_ask.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_courses=course_org.course_set.all()[0:3]
        all_teachers=course_org.teacher_set.all()[0:1]
        teacher_courses=all_teachers[0].course_set.all()[0:1]
        statue="home"
        return render(request,"org-detail-homepage.html",{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "teacher_courses":teacher_courses,
            "course_org":course_org,
            "statue":statue
        })

class OrgCourseView(View):
    """
    机构课程
    """
    def get(self,request,org_id):
        course_org=CourseOrg.objects.get(id=org_id)
        all_courses=course_org.course_set.all()
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
            "course_org":course_org,
            "statue": statue
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self,request,org_id):
        course_org=CourseOrg.objects.get(id=int(org_id))
        statue="describe"
        return render(request,"org-detail-desc.html",{
            "course_org":course_org,
            "statue":statue
        })
