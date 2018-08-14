# -*- coding: utf-8 -*-
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

from django.urls import path, re_path

app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)', CourseInfoView.as_view(), name='course_info'),
    re_path('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name='course_comments'),
    # 添加课程评论，已经把参数放到post当中了
    re_path('add_comment/', AddCommentsView.as_view(), name='add_comment')
]
