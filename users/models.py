# -*- coding:utf-8 -*-
from django.db import models
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
