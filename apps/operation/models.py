#_*_encoding:utf-8_*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course
from organization.models import Teacher
from organization.models import CourseOrg

# Create your models here.


class UserAsk(models.Model):
    name =models.CharField(max_length=20, verbose_name=u"姓名")
    mobile =models.IntegerField(max_length=11, verbose_name=u"手机")
    course_name =models.CharField(max_length=50, verbose_name=u"课程名")
    add_time =models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"用户咨询"
        verbose_name_plural=verbose_name


class CourseComments(models.Model):
    # 课程评论
    user=models.ForeignKey(UserProfile,verbose_name=u"用户")
    course=models.ForeignKey(Course,verbose_name=u"课程")
    comments=models.CharField(max_length=200,verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程评论"
        verbose_name_plural=verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course=models.ForeignKey(Course,verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"用户课程"
        verbose_name_plural=verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id=models.IntegerField(default=0,verbose_name=u"数据id")
    fa_type=models.IntegerField(choices=((1,"课程"),(2,"课程机构"),(3,"讲师")),default=1,verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    # course = models.ForeignKey(Course, verbose_name=u"课程")
    # teacher=models.ForeignKey(Teacher,verbose_name=u"教师")
    # courseorg=models.ForeignKey(CourseOrg,verbose_name=u"授课机构")
    # fav_type=

    class Meta:
        verbose_name=u"用户收藏"
        verbose_name_plural=verbose_name


# class message(models.Model):
#     add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
#     txt=models.TextField(verbose_name=u"消息")
#
#     class Meta:
#         verbose_name=u"消息"
#         verbose_name_plural=verbose_name


class UserMessage(models.Model):
    user=models.IntegerField(default=0,verbose_name=u"接收用户")
    message=models.CharField(max_length=500,verbose_name=u"消息内容")
    has_read=models.BooleanField(default=False,verbose_name=u"是否已读")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"用户消息"
        verbose_name_plural=verbose_name