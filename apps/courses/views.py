from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course, CourseResource
from operation.models import UserFavorite


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


# 处理课程章节信息页面的view
class CourseInfoView(View):
    def get(self, request, course_id):
        # 此处的id为表默认为我们添加的值。
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        # 是否收藏课程
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,  # 前端用course.courseresource_set.get_queryset代替了
        })
