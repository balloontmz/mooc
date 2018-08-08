# -*- coding: utf-8 -*-

import xadmin

from .models import CityDict, CourseOrg, Teacher

# 创建admin的管理类，这里不再继承admin，而是继承object
class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city', 'add_time']


# 创建admin的管理类，这里不再继承admin，而是继承object
class TeacherAdmin(object):
    list_display = [
        'org',
        'name',
        'work_years',
        'work_company',
        'work_position',
        'points',
        'click_num',
        'fav_nums',
        'add_time'
    ]
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_nums']
    list_filter = [
        'org',
        'name',
        'work_years',
        'work_company',
        'work_position',
        'points',
        'click_num',
        'fav_nums',
        'add_time'
    ]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)