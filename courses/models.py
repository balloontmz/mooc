# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.
# 课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', 'primary'),
        ('zj', 'middle'),
        ('gj', 'high')
    )
    name = models.CharField(max_length=50, verbose_name='class_name')
    desc = models.CharField(max_length=300, verbose_name='class_desc')
    # TextField 允许我们不输入长度。可以输入到无限大。暂时定义为TextField, 之后更新为富文本？markdown？
    detail = models.TextField(verbose_name='class_detail')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2)
    # 使用分钟做后台记录，前台转换
    learn_times = models.IntegerField(default=0, verbose_name='learn_time(min)')
    # 保存学习人数：点击开始学习才算
    students = models.IntegerField(default=0, verbose_name='learn_num')
    fav_nums = models.IntegerField(default=0, verbose_name='fav_num')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name='cover',
        max_length=100
    )
    # 保存点击量，点进页面就酸
    click_nums = models.IntegerField(default=0, verbose_name='click_num')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='create_time')  # 课程创建时间？

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = verbose_name


#章节
class Lesson(models.Model):
    # 因为一个课程对应很多章节，所以在章节表中将课程设置为外键
    # 作为一个字段来让我们可以知道这个章节对应哪个课程
    course = models.ForeignKey(Course, verbose_name='course')
    name = models.CharField(max_length=100, verbose_name='lesson_name')
    # 课程添加时间？
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = verbose_name


# 每章视频
class Video(models.Model):
    # 因为一个章节对应很多视频，所以在视频表中将章节设置为外键
    # 作为一个字段来存储让我们知道这个视频对应哪个章节
    lesson = models.ForeignKey(Lesson, verbose_name='lesson')
    name = models.CharField(max_length=100, verbose_name='video_name')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name='video'
        verbose_name_plural = verbose_name


# 课程资源
class CourseResource(models.Model):
    # 因为一个课程对应很多资源，所以在课程资源表中将课程设置为外键。
    # 作为一个字段来让我们知道这个资源对应哪个课程
    course = models.ForeignKey(Course, verbose_name='course')
    name = models.CharField(max_length=100, verbose_name='resource_name')
    # 这里定义文件类型的field，后台管理系统中会直接有上传的按钮？
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name='resource_file',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = 'course_resource'
        verbose_name_plural = verbose_name
