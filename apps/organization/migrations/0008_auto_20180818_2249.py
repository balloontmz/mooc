# Generated by Django 2.0.1 on 2018-08-18 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_teacher_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='fav_num',
            new_name='fav_nums',
        ),
    ]