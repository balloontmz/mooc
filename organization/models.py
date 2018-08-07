# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.
# 城市字典： 用来干嘛？
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='city')
    # 城市描述：备用不一定展示出来
    desc = models.CharField(max_length=200, verbose_name='desc')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = verbose_name


# 课程机构
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='course_org')
    # 机构描述，后面转换为富文本展示
    desc = models.TextField(verbose_name='org_desc')
    click_num = models.IntegerField(default=0, verbose_name='click_num')
    fav_num = models.IntegerField(default=0, verbose_name='fav_num')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name='cover',
        max_length=100
    )
    address = models.CharField(max_length=150, verbose_name='org_addr')
    # 一个城市可以有很多课程机构，通过将city设置为外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(CityDict, verbose_name='the_city')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'org'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    # 一个机构会有很多老师，所以我们在讲师表添加外键并把课程机构名称保存下来
    # 可以使我们通过讲师找到对应的机构
    org = models.ForeignKey(CourseOrg, verbose_name='org')
    name = models.CharField(max_length=50, verbose_name='teacher_name')
    work_years = models.IntegerField(default=0, verbose_name='teacher_year')
    work_company = models.CharField(max_length=50, verbose_name='work_company')
    work_position = models.CharField(max_length=50, verbose_name='work_position')
    points = models.CharField(max_length=50, verbose_name='points')
    click_num = models.IntegerField(default=0, verbose_name='click_num')
    fav_nums = models.IntegerField(default=0, verbose_name='fav_num')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = verbose_name
