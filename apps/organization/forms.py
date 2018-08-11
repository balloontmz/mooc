# -*- coding: utf-8 -*-
from django import forms
import re
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    # 继承之余还可以添加字段
    # 相比普通的form增加了save方法
    # 是由哪个model转换的
    class Meta:
        model = UserAsk
        # 需要验证的字段
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')

