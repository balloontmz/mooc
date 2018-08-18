# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile


# 登录表单验证
class LoginForm(forms.Form):
    # 用户密码不能为空
    # 这两个参数名应该与传入的参数名一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField()


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码 自定义输出key必须与异常一样 不懂
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 忘记密码验证码实现
class ForgetForm(forms.Form):
    # 此处email与前端name保持一致
    email = forms.EmailField(required=True)
    # 应用验证码 自定义错误输出key必须与异常保持一致
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 重置密码的form实现
class ModifyPwdForm(forms.Form):
    # 密码不能小于5位
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 用于文件上传， 修改头像
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']


# 用于个人中心修改个人信息
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
