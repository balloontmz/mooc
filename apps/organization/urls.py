# -*- coding: utf-8 -*-
from organization.views import OrgView, AddUserAskView
from django.urls import path, re_path

app_name = 'organization'  # 解决没有app_name的问题

urlpatterns = [
    # 课程机构列表url
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask')
]
