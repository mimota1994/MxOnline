#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-04 16:56'

import xadmin

from .models import CityDict,Teacher,CourseOrg

class CityDictAdmin(object):
    list_display=['name','des','add_time']
    search_fields=['name','des']
    list_filter=['name','des','add_time']

class TeacherAdmin(object):
    list_display = ['name', 'org','work_years','work_company','work_position',
                    'points','click_nums','fav_nums', 'add_time']
    search_fields = ['name', 'org','work_years','work_company','work_position',
                    'points','click_nums','fav_nums']
    list_filter = ['name', 'org','work_years','work_company','work_position',
                    'points','click_nums','fav_nums', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'address', 'image', 'city',
                     'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'address', 'image', 'desc', 'city',
                     'click_nums', 'fav_nums']
    list_filter = ['name', 'address', 'image', 'desc', 'city',
                     'click_nums', 'fav_nums', 'add_time']
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)