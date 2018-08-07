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

>    class Meta:
        verbose_name = u"用户留言信息"
         # 指明复数信息，否则后台显示"用户留言s"
        verbose_name_plural = verbose_name
         # 这里我们让它自动生成所以不用指定db-table
        # db_table = user_message
         # ordering指定默认排序字段,如：
        # ordering = ['-object_id']
###

 on_delete=models.CASCADE 级联删除
 
 import sys
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
print(os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

>关于 makemigrations & migrate 数据库表的变动问题，还有许多疑问
修改过app的models之后，一定要记得运行上面命令，这样才能更新数据库，从而进行其他操作
###
setting中操作
# 语言改为中文
LANGUAGE_CODE = 'zh-hans'
# 时区改为上海
TIME_ZONE = 'Asia/Shanghai'
# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = False

新建的 model 对象的内嵌 类Meta的verbose_name字段用于在后台显示表名
为了适配xadmin，采用了降级django：
>pip install django==2.0.8
重置了数据库编码
alter database mooc3 character set utf8
/etc/mysql/mysql.conf.d mysql.cnf文件中加入如下配置
[mysqld]
character-set-server=utf8 
[client]
default-character-set=utf8 
[mysql]
default-character-set=utf8

删除了一次全部的migrations，因为之前初始化的时候编码有问题。。。

class EmailVerifyRecordAdmin(object):
    # 配置我们后台需要显示的列。
    list_display = ['code', 'email', 'send_type', 'send_time']
