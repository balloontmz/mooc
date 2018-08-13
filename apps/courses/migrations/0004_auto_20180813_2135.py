# Generated by Django 2.0.1 on 2018-08-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=20, verbose_name='课程类别'),
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=15, verbose_name='课程标签'),
        ),
    ]