# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login  # 在类中重载了为何还要导入，为何要在setting中加入本文件中重载的类以及方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect  # 加载重定向类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.email_send import send_register_email
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher


# Create your views here.
# 重载登录方式，在setting中加载
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Q 采用并集运算，只能取到其中一个（不懂）
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中对密码加密，所以不能password=password
            # UserProfile继承的AbstractUser中有 def check_password(self, raw_password)

            if user.check_password(password):
                return user
        except Exception as e:
            return None


def user_login(request):
    # 前端向后端发送的请求方式: get 或post

    # 登录提交表单为post
    if request.method == "POST":
        # 取不到时为空，username，password为前端页面name值
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        # 成功返回user对象,失败返回null
        user = authenticate(username=user_name, password=pass_word)

        # 如果不是null说明验证成功
        if user is not None:
            # login_in 两参数：request, user
            # 实际是对request写了一部分东西进去，然后在render的时候：
            # request是要render回去的。这些信息也就随着返回浏览器。完成登录
            login(request, user)
            return render(request, "index.html")
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误! "})
        # 获取登录页面为get
    elif request.method == "GET":
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})


# 添加登录重定向 next参数经过next(view)->redict_url(get)->next(view)->redict_url(post)
class LoginView(View):
    # 该类能直接调用get方法免去判断

    def get(self, request):
        # render 就是渲染html 返回用户
        # render三变量： request 模板名称 一个传递参数的字典
        redirect_url = request.GET.get('next', '')
        return render(request, 'login.html', {
            'redirect_url': redirect_url,  # 此参数在post中重加为next？
        })

    def post(self, request):
        # 该类实例化需要一个字典dict： request.POST就是一个QueryDict所以直接传入
        # POST中的username、password，会对应到form中
        login_form = LoginForm(request.POST)
        # is_valid判断我们字段是否有错
        if login_form.is_valid():
            # 取不到时为空
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 成功返回user对象
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null表示验证成功
            if user is not None:
                # 以下函数实际是吧user写入request
                login(request, user)
                # 增加重定向回原网页
                redirect_url = request.POST.get('next', '')
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                # 跳转到首页，此时的request带上了user对象的状态
                return render(request, 'index.html')
            # 仅当账户密码出错的时候
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！ '})
        # 没有成功说明有值是None，并再次跳转回主页面
        else:
            return render(
                request, 'login.html', {
                    'login_form': login_form
                }
            )


class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为false
            user_profile.is_active = False

            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册mooc'
            user_message.save()

            # 发送注册激活邮件
            send_register_email(user_name, 'register')

            # 跳转到登录页面
            return render(request, 'login.html')
        # 注册邮箱form验证失败
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        # active_form = ActiveForm(request.Get)  报错'WSGIRequest' object has no attribute 'Get'
        active_form = ActiveForm()
        if all_record:
            for record in all_record:
                # 获取相应的邮箱
                email = record.email
                # 查找邮箱对应的user
                user = UserProfile.objects.get(username=email)
                user.is_active = True
                user.save()
                # 激活成功跳转页面
                return render(request, 'login.html', {'msg': '激活成功，请登录'})
        else:
            return render(request, 'register.html', {'msg': '您的激活链接无效', 'active_form': active_form})


# 用户忘记密码的处理view
class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码邮件
            send_register_email(email, 'forget')
            # 发送完毕返回登录页面并显示发送邮件成功
            return render(request, 'login.html', {'msg': '重置密码邮件发送成功，请注意查收'})
        # 如果表单失败则是验证码验证失败等
        else:
            return render(request, 'forgetpwd.html', {
                'forget_form': forget_form})


# 重置密码的view
class ResetView(View):
    def get(self, request, active_code):
        # 验证邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm()
        if all_record:
            for record in all_record:
                # 获取对应的邮箱
                email = record.email
                # 将email传回来
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(
                request, 'forgetpwd.html', {
                    'msg': '您的链接无效，请重新请求', 'active_form': active_form,
                }
            )


# 改变密码的view
class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            # 如果密码一致
            user = UserProfile.objects.get(username=email)
            # 加密成密文
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html', {'email': email, 'modifypwd_form': modifypwd_form})
        # 验证失败说明密码位数不够
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwd_form': modifypwd_form})


# 用户个人信息view
class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        # 此处不是添加一个新的user，需要指明instance，不然无法修改名，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            # 通过json的dumps方法把字典转换成json字符串
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 用户上传图片的view，用于修改头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        # 这时候用户上传的文件就已经保存到imageform了，为modelform添加instance值直接保存
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # 取出clean_data中的值，一个dict。(此dict为通过了form验证的数据)
            # 以下提供了修改用户image的另一种方法，匹配单一不带modelform，可查看debug
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


# 在个人中新修改用户密码
class UpdatePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pw1 = request.POST.get('password1', '')
            pw2 = request.POST.get('password2', '')
            # 如果两次密码不相等，返回错误信息
            if pw1 != pw2:
                return HttpResponse('{"static": "fail", "msg": "密码不一致"}', content_type='application/json')
            # 如果密码一致
            user = request.user
            # 加密成django密码形式
            user.password = make_password(pw1)
            # save保存到数据库
            user.save()
            return HttpResponse('{"static": "success"}', content_type='application/json')
        # 验证失败说明位数不够
        else:
            # 通过json的dumps方法将字典转换为json字符串
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送邮箱验证码的view（修改用户邮箱的时候）:
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        # 取出需要发送的邮件
        email = request.GET.get('email', '')

        # 不能使已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


# 修改邮箱的view：
class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'  # 此属性用于自动跳转登录时的重定向？？？

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '') # 此code应该是手动输入的四位数，取自邮件

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码无效"}', content_type='application/json')


# 个人中心我的课程
class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


# 我收藏的机构
class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


# 我收藏的老师
class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # 上面的fav只是存放了id。我们还需要id找到机构对象
        for fav_teacher in fav_teachers:
            # 取出fav_id也就是教师的id
            teacher_id = fav_teacher.fav_id
            # 获取这个机构对象
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


# 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        # 上面的fav只是存放了id。我们还需要id找到机构对象
        for fav_course in fav_courses:
            # 取出fav_id也就是教师的id
            course_id = fav_course.fav_id
            # 获取这个机构对象
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_message = UserMessage.objects.filter(user = request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })
