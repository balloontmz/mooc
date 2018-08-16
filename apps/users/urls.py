# -*- coding: utf-8 -*-
from users.views import UserInfoView, UpdatePwdView, UploadImageView, SendEmailCodeView, UpdateEmailView
from django.urls import path

app_name = 'users'

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    path('upload/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 专门用于发送验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email')
]
