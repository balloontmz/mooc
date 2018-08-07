# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

# 引入我们CourseComments所需的外键models
from users.models import UserProfile
from courses.models import Course


# Create your models here.
# 用户我要学习表单
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='')
    mobile = models.CharField(max_length=11, verbose_name='tele_num')
    course_name = models.CharField(max_length=50, verbose_name='course_name')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'user_consult'
        verbose_name_plural = verbose_name


# 用于用户评论
class CourseComments(models.Model):

    # 会涉及两个外键：1.用户、2.课程。import进来
    course = models.ForeignKey(Course, verbose_name='course', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    comments = models.CharField(max_length=250, verbose_name='comments')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = verbose_name


# 用于对于课程，机构，讲师的收藏
class UserFavorite(models.Model):
    # 涉及四个外键：用户、课程、机构、讲师  实际只用到了一个？
    TYPE_CHOICES =(
        (1, 'course'),
        (2, 'org'),
        (3, 'teacher')
    )

    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    #  保存fav的对象的id
    fav_id = models.IntegerField(default=0)
    # 表明收藏的是哪种类型
    fav_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='fav_type'
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'user_fav'
        verbose_name_plural = verbose_name


# 用户消息表
class UserMessage(models.Model):
    # 因为我们的消息有两种：发给全员的和发给某个用户的。
    # 所以如果我们使用外键，每个消息会对应要有用户。很难实现全员消息。

    # 为 0 则 发给所有用户，不为0 则发给指定id
    user = models.IntegerField(default=0, verbose_name='accept_user')
    message = models.CharField(max_length=500, verbose_name='msg_content')

    # 是否已读
    has_read = models.BooleanField(default=False, verbose_name='has_read')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'user_msg'
        verbose_name_plural =verbose_name


# 用户课程表
class UserCourse(models.Model):
    # 会涉及两个外键：1.用户，2.课程。
    course = models.ForeignKey(Course, verbose_name='course', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='user', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'user_course'
        verbose_name_plural = verbose_name
