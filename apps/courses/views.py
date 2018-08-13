from django.shortcuts import render
from django.views.generic.base import View
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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

