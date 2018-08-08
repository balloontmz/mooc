# -*- coding: utf-8 -*-

import xadmin

from .models import Course, Lesson, Video, CourseResource


# 创建Course的admin管理器
class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students'
    ]
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = [
        'name',
        'desc',
        'detail',
        'learn_times',
        'students'
    ]


class LessonAdmin(object):
    # 配置我们后台需要显示的列。
    list_display = ['course', 'name', 'add_time']
    # 配置搜索字段，不做时间搜索
    search_fields = ['course', 'name']
    # 配置筛选字段 __name代表使用外键中的name字段
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)