from django.shortcuts import render
from django.contrib.auth import authenticate, login  # 在类中重载了为何还要导入，为何要在setting中加入本文件中重载的类以及方法
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q


# Create your views here.
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


