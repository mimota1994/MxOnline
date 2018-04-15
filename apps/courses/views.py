#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q


from .models import Course,Video
from operation.models import UserFavorite,UserCourse,CourseComments

# Create your views here.
class CourseView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by("add_time")

        #课程搜索
        search_keywords=request.GET.get('keywords', "")
        if search_keywords:
            #i 不区分大小写
            all_courses=all_courses.filter(Q(name__icontains=search_keywords)|Q(des__icontains=search_keywords)|Q(detail__icontains=search_keywords))

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

        #我要学习
        msg='我要学习'
        if request.user.is_authenticated():
            if UserCourse.objects.filter(user=request.user,course=course):
                msg='正在学习'

        #课程机构收藏显示
        org_msg="收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,fav_type=2):
                org_msg="已收藏"


        course_msg = "收藏"
        if request.user.is_authenticated():
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
            'msg':msg,
            'related_courses':relate_courses,
            'sa':'course'
        })


class AddLearnView(View):

    def post(self,request):
        user_id=request.user.id
        course_id = request.POST.get('course_id', 0)

        course = Course.objects.get(id=course_id)

        #增加学习课程的数据记录
        if request.user.is_authenticated():
            user_course=UserCourse()

            #判断是否存在记录
            exist_records = UserCourse.objects.filter(user_id=int(user_id), course_id=int(course_id))
            if not exist_records:
                user_course.user_id=user_id
                user_course.course_id=course_id
                user_course.save()
                #更新课程学习人数
                students=UserCourse.objects.filter(course_id=int(course_id)).count()
                course.students=students
                course.save()

                return HttpResponse('{"status":"transfer","msg":"正在学习"}', content_type='application/json')
            else:
                exist_records.delete()

                # 更新课程学习人数
                students = UserCourse.objects.filter(course_id=int(course_id)).count()
                course.students = students
                course.save()

                return HttpResponse('{"status":"concel","msg":"我要学习"}', content_type='application/json')


        else:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')


class CourseVideoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        return render(request,'course-video.html',{
            'course':course,
            'comment_or_video': "video",
            'sa':'course'
        })


class CourseCommentView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=course_id)
        all_comments=course.coursecomments_set.all()
        return render(request,'course-comment.html',{
            'course':course,
            'comment_or_video':"comment",
            'sa':'course',
            'all_comments':all_comments
        })


class AddCommentView(View):
    def post(self,request):
        course_id=request.POST.get('course_id',"0")
        comments=request.POST.get('comments',"")

        if request.user.is_authenticated():
            course_comments=CourseComments()
            course_comments.course_id=course_id
            course_comments.user_id=request.user.id
            course_comments.comments=comments
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"success","msg":"用户未登陆"}', content_type='application/json')


class VideoView(View):
    def get(self,request,video_id):
        if request.user.is_authenticated():
            video=Video.objects.get(id=video_id)
            course=video.lesson.course
            if UserCourse.objects.filter(user=request.user,course=course):
                return render(request,'video_things.html',{
                    'video_url':video.video_url
                })