# -*- coding: utf-8 -*-
from courses.views import CourseListView

from django.urls import path

app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
]
