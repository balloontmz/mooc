from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin # 此类用于验证登录、还有登录后的重定向


# Create your views here.
class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')
        hot_courses = Course.objects.all().order_by('-students')[:3]  # 取前三位，此代码应该能优化
        # 尝试获取前台get请求传递过来的page参数
        # 如果不合法，默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #
        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_course': courses,  # 在html中注意采用object_list而不是objects
            'sort': sort,
            'hot_courses': hot_courses,

        })


# 课程详情处理view
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()
        # 是否收藏课程
        has_fav_course = False
        has_fav_org = False
        # 必须要用户已登录我们才需要判断
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 取出标签找到标签相同的course
        tag = course.tag
        if tag:
            # 从1开始否则会推荐自己？
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


# 处理课程章节信息页面的view, 增加登录鉴定（多重继承），定义重定向所需的网址
# login记得前置，否则没效果！！！
class CourseInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        # 此处的id为表默认为我们添加的值。
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否学习了该课，如果还未学习则加入用户课程表
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 查询课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)  # 重载该变量，因为这个变量之前的值已经没用了
        # 从关系中取出user_id -> 以上这句推测只是缓存关系，并未执行，以下执行并取出id保存到dict中备用
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程，外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        # exclude: 过滤掉满足条件的 filter：取得满足条件的
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums').exclude(id=course.id)[:4]
        # 是否收藏课程
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,  # 前端用course.courseresource_set.get_queryset代替了
            'relate_courses': relate_courses,
        })


# 评论界面
class CommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        # 此处course_id为url传入的值
        # objects 的三种方法（all、get、filter）需要多了解
        course = Course.objects.get(id=int(course_id))
        # 资源用来干嘛？ 看前端
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all().order_by('-add_time')
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)  # 重载该变量，因为这个变量之前的值已经没用了
        # 从关系中取出user_id -> 以上这句推测只是缓存关系，并未执行，以下执行并取出id保存到dict中备用
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程，外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        # exclude: 过滤掉满足条件的 filter：取得满足条件的
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums').exclude(id=course.id)[:4]

        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
        })


# ajax异步添加评论
class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，ajax跳转到登录页面
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # get只要取出一条数据，如果多条抛出异常，没有数据也抛出异常？
            # filter取出一个列表出来，queryset。没有数据返回空的queryset不会抛出异常
            course = Course.objects.get(id=int(course_id))
            # 外键写入要存入对象
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user # 网络上传输的只是user的特征值，user的传递都在服务器内部
            course_comments.save()
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')
