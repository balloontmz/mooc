# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.
# 城市字典： 用来干嘛？
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    # 城市描述：备用不一定展示出来
    desc = models.CharField(max_length=200, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name


# 课程机构
class CourseOrg(models.Model):
    ORG_CHOICES = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
    )
    name = models.CharField(max_length=50, verbose_name='课程机构')
    # 机构描述，后面转换为富文本展示
    desc = models.TextField(verbose_name='机构描述')
    # 机构类型
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name='机构类型', default='pxjg')
    tag = models.CharField(max_length=10, default='国内名校', verbose_name='机构标签')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    # 当学生点击学习课程，找到所属机构，学习人数+1
    students = models.IntegerField(default=0, verbose_name='学习人数')
    # 当发布课程就+1
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name='封面',
        max_length=100
    )
    address = models.CharField(max_length=150, verbose_name='机构地址')
    # 一个城市可以有很多课程机构，通过将city设置为外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    # 一个机构会有很多老师，所以我们在讲师表添加外键并把课程机构名称保存下来
    # 可以使我们通过讲师找到对应的机构
    org = models.ForeignKey(CourseOrg, verbose_name='机构',  on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='教学年限')
    work_company = models.CharField(max_length=50, verbose_name='所在公司')
    work_position = models.CharField(max_length=50, verbose_name='所居职位')
    age = models.IntegerField(default=18, verbose_name='年龄')
    points = models.CharField(max_length=50, verbose_name='教学特色')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    image = models.ImageField(
        default='',
        upload_to='teacher/%Y/%m',
        verbose_name='头像',
        max_length=100
    )

    def __str__(self):  # 何处会调用呢
        return '{0}的教师>>{1}'.format(self.org, self.name)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
