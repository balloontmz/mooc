# -*- coding: utf-8 -*-
from courses.views import CourseListView, CourseDetailView

from django.urls import path, re_path

app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
]
