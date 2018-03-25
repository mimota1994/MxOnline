#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg,CityDict
from .forms import UserAskForm
from operation.models import UserAsk

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
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            name=request.POST.get("name","")
            phone=request.POST.get("phone","")
            course_name=request.POST.get("course_name","")

            user_ask = UserAsk()
            user_ask.name = name
            user_ask.phone=phone
            user_ask.course_name=course_name
            user_ask.save()

