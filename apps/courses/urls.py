# -*- coding: utf-8 -*-
from courses.views import CourseListView, CourseDetailView, CourseInfoView

from django.urls import path, re_path

app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)', CourseInfoView.as_view(), name='course_info')
]
