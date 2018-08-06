>设计model的时候的__unicode__方法
def __str__(self):
    return self.name
   3.6也可以重载unicode，但是后台显示可能出问题

import pymysql
pymysql.install_as_MySQLdb()
CharField必须有max_length, Imagefield实际也是charfield所以也要有max_length

Tools->manage.py Task
startapps users

###setting设置INSTALLED_APPS & AUTH_USER_MODEL。
在INSTALLED_APPS中注册app
重载AUTH_USER_MODEL (用来干嘛？) 为了使UserProfile生效：可能和后面相关？
AUTH_USER_MODEL = 'users.UserProfile'
如下报错：
>django.db.migrations.exceptions.InconsistentMigrationHistory: Migration
admin.0001_initial is applied before its dependency users.0001_initial on
database 'default'

解决方案: 删表.重新初始化数据表

###根据
先startapp users，
然后编辑models加入 UserProfile
setting中加入app 和 AUTH_USER_MODEL
然后初始化数据库表
###的顺序完成的初始化，没有了auth_user这张表。。。