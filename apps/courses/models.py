# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher


# Create your models here.
# 课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', 'primary'),
        ('zj', 'middle'),
        ('gj', 'high')
    )
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    # TextField 允许我们不输入长度。可以输入到无限大。暂时定义为TextField, 之后更新为富文本？markdown？
    detail = models.TextField(verbose_name='课程细节')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2)
    # 使用分钟做后台记录，前台转换
    learn_times = models.IntegerField(default=0, verbose_name='学习时间（分钟）')
    # 保存学习人数：点击开始学习才算
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏次数')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name='课程封面',
        max_length=100
    )
    # 保存点击量，点进页面就酸
    click_nums = models.IntegerField(default=0, verbose_name='点击量')  # 对该功能的实现方式很好奇
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    tag = models.CharField(max_length=15, verbose_name='课程标签', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')  # 课程创建时间？
    # 后来添加的
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构', null=True, blank=True)  # 由于是后增的，null和blank属性为true
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师', null=True, blank=True)
    you_need_know = models.CharField(max_length=300, default='一颗勤学的心是本课程的必要前提', verbose_name='=课程须知')
    teacher_tell = models.CharField(max_length=300, default='什么都可以学到，按时交作业，不然叫家长', verbose_name='=老师告诉你')

    def __str__(self):  # 此处暂时用于后台外键显示的名称
        return self.name

    class Meta:
        verbose_name = '课程'  # 该类的后台显示名称
        verbose_name_plural = verbose_name


#章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节，所以在章节表中将课程设置为外键
    # 作为一个字段来让我们可以知道这个章节对应哪个课程
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名称')
    # 课程添加时间？
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


# 每章视频
class Video(models.Model):
    # 因为一个章节对应很多视频，所以在视频表中将章节设置为外键
    # 作为一个字段来存储让我们知道这个视频对应哪个章节
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    # 后加的
    url = models.CharField(max_length=200, default='http://blog.mtianyan.cn/', verbose_name='视频地址')
    # 课程所需时间
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')

    def __str__(self):  # 此处暂时用于后台外键显示
        return self.name

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


# 课程资源
class CourseResource(models.Model):
    # 因为一个课程对应很多资源，所以在课程资源表中将课程设置为外键。
    # 作为一个字段来让我们知道这个资源对应哪个课程
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='资源名称')
    # 这里定义文件类型的field，后台管理系统中会直接有上传的按钮？
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name='资源明细',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):  # 此处暂时用于后台外键显示
        return self.name

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
