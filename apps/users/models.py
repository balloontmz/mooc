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
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    # 生日，可以为空
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        verbose_name='性别',
        choices=GENDER_CHOICES,
        default='female'
    )
    # 地址
    address = models.CharField(max_length=100, verbose_name='地址', default='')
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
        verbose_name = '用户信息'  # 此处用于后台显示
        verbose_name_plural = verbose_name

    # 重载str方法，打印实例会打印出username，username继承自abstractuser
    def __str__(self):
        return self.username


# 邮箱验证码model
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', '注册'),
        ('forget', '忘记密码'),
        ('update_email', '修改邮箱'),
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    # 未设置null = true blank = true 默认不可为空（未懂
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name='验证码类型')
    # 这里的now不带括号，表示调用时才运行，而不是编译时运行
    send_time = models.DateTimeField(default=datetime.now)
    # 某种类型的调用对象时的返回值？？？

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name


# 轮播图model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(
        upload_to='banner/%Y/%m', # 此参数表示图片的路径，参数 Ym 可能表示年月？
        verbose_name='轮播图',
        max_length=100
    )
    url = models.URLField(max_length=200, verbose_name='URL')
    # 默认index很大靠后，想要靠前修改index值 （不懂，是否和后面相关),有无覆盖父类参数？
    index = models.IntegerField(default=100, verbose_name='页码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

