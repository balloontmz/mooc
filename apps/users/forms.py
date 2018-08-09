# -*- coding: utf-8 -*-
from django import forms


# 登录表单验证
class LoginForm(forms.Form):
    # 用户密码不能为空
    # 这两个参数名应该与传入的参数名一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
