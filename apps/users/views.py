from django.shortcuts import render
from django.contrib.auth import authenticate, login  # 在类中重载了为何还要导入，为何要在setting中加入本文件中重载的类以及方法
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.http import HttpResponseRedirect # 加载重定向类

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
                request, 'login.html',{
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
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


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
