# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'man'),
        ('female', 'woman')
    )
    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name='nick_name', default='')
    # 生日，可以为空
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    gender = models.CharField(
        max_length=5,
        verbose_name='sex',
        choices=GENDER_CHOICES,
        default='female'
    )
    # 地址
    address = models.CharField(max_length=100, verbose_name='address', default='')
    # 电话
    moble = models.CharField(max_length=11, null=True, blank=True)
    # 头像，默认使用default.png
    image = models.ImageField(
        upload_to='image/%Y/%m',
        default='image/default.png',
        max_length=100
    )
    # meta信息，即后台栏目名
    class Meta:
        verbose_name = 'user_msg'
        verbose_name_plural = verbose_name

    # 重载str方法，打印实例会打印出username，username继承自abstractuser
    def __str__(self):
        return self.username


# 邮箱验证码model
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', 'register'),
        ('forget', 'forget_password')
    )
    code = models.CharField(max_length=20, verbose_name='verify_code')
    # 未设置null = true blank = true 默认不可为空（未懂
    email = models.EmailField(max_length=50, verbose_name='email')
    send_type = models.CharField(choices=SEND_CHOICES, max_length=10)
    # 这里的now不带括号，表示调用时才运行，而不是编译时运行
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'verify_code'
        verbose_name_plural = verbose_name


# 轮播图model
class Banner(models.Model):
    title = models.CharField(max)
    image = models.ImageField(
        upload_to='banner/%Y/%m', # 此参数表示图片的路径，参数 Ym 可能表示年月？
        verbose_name='banner',
        max_length=100
    )
    url = models.URLField(max_length=200, verbose_name='url_route')
    # 默认index很大靠后，想要靠前修改index值 （不懂，是否和后面相关),有无覆盖父类参数？
    index = models.IntegerField(default=100, verbose_name='order')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name='banner'
        verbose_name_plural = verbose_name
