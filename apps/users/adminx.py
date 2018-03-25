#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-04 14:51'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner

class BaseSetting(object):
    enable_themes=True
    # use_bootswatch=T rue

class GlobalSettings(object):
    site_title="慕学后台管理系统"
    site_footer="慕学在线网"
    menu_style="accordion"

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(Banner,BannerAdmin)

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)