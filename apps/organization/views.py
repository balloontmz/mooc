# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg, CityDict
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from organization.forms import UserAskForm
from django.http import HttpResponse, JsonResponse


# Create your views here.
# 处理课程机构列表的view
class OrgView(View):
    def get(self, request):
        # 查找所有的课程机构
        all_orgs = CourseOrg.objects.all()

        # 热门机构，如果不加负号回事从小到大
        hot_orgs = all_orgs.order_by('-click_num')[:3]

        # 取出所有的城市
        all_citys = CityDict.objects.all()

        # 取出筛选 的城市，默认值为空
        city_id = request.GET.get('city', '')
        # 如果选择某个城市，也就是前端传回来了值
        if city_id:
            # 外键city在数据中叫city_id
            # 我们就在机构中作进一步筛选
            all_orgs = all_orgs.filter(city_id=int(city_id))  # 此处city_id关键字代表city外键的id属性，django所有,粗略测试模板不可采用此方法？

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 总共有多少加机构使用count进行统计
        org_num = all_orgs.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取出五个出来，每页显示五个
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


# 用户添加我要学习
class AddUserAskView(View):
    # 处理表单方法为post
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        # 判断form是否有效
        if userask_form.is_valid():
            # 这个form有model属性
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串，并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status": "fail", "msg": {0}}'.format(userask_form.errors), content_type='application/json')


# 某个机构的首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]  # 主页，所以只是节选，如果在列表页，应该就是全选了
        # 以下功能应该不是用在此处？？？应该是对应机构课程教师详情页？？？
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
        })


# 机构课程列表页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


# 机构描述详情页
class OrgDescView(View):
    def get(self, request, org_id):
        # 向前端传值，表示在desc页
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 向前端传值说明用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构讲师列表页
class OrgTeacherView(View):
    def get(self, request, org_id):
        # 向前端传值，表明在教师页
        current_page = 'teacher'
        # 通过id查找课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到教室
        all_teacher = course_org.teacher_set.all()
        # 向前端传值表明用户是否收藏。
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 添加收藏和取消收藏功能
class AddFavView(View):
    def post(self, request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)
        # 判断用户是否登录，即使未登录，request也会有一个匿名user
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "收藏"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            # 如果记录存在，则表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')

