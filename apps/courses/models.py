#_*_encoding:utf-8_*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):

    course_teacher=models.ForeignKey(Teacher,verbose_name=u"教师",null=True,blank=True)
    course_org=models.ForeignKey(CourseOrg,verbose_name=u"课程机构",null=True,blank=True)
    name=models.CharField(max_length=50,verbose_name=u"课程名")
    des=models.CharField(max_length=200,verbose_name=u"课程描述")
    degree=models.CharField(choices=(("gj",u"高级"),("zj",u"中级"),("cj",u"初级")),max_length=2)
    students=models.IntegerField(default=0,verbose_name=u"学习人数")
    learn_times=models.IntegerField(default=0,verbose_name=u"学习时常(分钟数)")
    # chapter_number=models.IntegerField(max_length=5,verbose_name=u"章节数")
    category=models.CharField(max_length=20,verbose_name=u"课程类别",null=True,blank=True)
    detail=models.TextField(verbose_name=u"课程详情")
    fav_nums=models.IntegerField(default=0,verbose_name=u"收藏")
    image=models.ImageField(upload_to="course/%Y/%m",verbose_name=u"封面图",max_length=100)
    click_nums=models.IntegerField(default=0,verbose_name=u"点击数")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
    tag=models.CharField(default="",verbose_name=u"课程标签",max_length=10)

    class Meta:
        verbose_name=u"课程"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name=models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"章节"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u"章节")
    name=models.CharField(max_length=100,verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    video_url=models.URLField(max_length=200,verbose_name="视频地址",default="",blank=True,null=True)

    class Meta:
        verbose_name=u"视频"
        verbose_name_plural=verbose_name


class CourseResource(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download=models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程资源"
        verbose_name_plural=verbose_name
