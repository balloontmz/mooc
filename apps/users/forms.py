# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField


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
