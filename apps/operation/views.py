#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic.base import View

from courses.models import Course
from organization.models import CourseOrg
# Create your views here.

#首页逻辑
class IndexView(View):
    def get(self,request):

        all_courses=Course.objects.all()
        banner_courses = all_courses[:2]
        all_courses=all_courses[2:]
        all_orgs=CourseOrg.objects.all()
        return render(request,'index.html',{
            'all_courses':all_courses,
            'all_orgs':all_orgs,
            'banner_courses':banner_courses
        })


