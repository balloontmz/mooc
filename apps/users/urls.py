# -*- coding: utf-8 -*-
from users.views import UserInfoView, UpdatePwdView, UploadImageView, SendEmailCodeView, UpdateEmailView,\
    MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView,MyMessageView
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
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 用户中心我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 我收藏的课程机构
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    # 我收藏的课程讲师
    path('myfav/teacher', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我收藏的课程
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的消息
    path('my_message/', MyMessageView.as_view(), name='my_message'),
]
