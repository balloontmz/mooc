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

verbose_name属性好像能够热更新？？？也就是该字段应该不输入数据库，只接受Django调用
推测该属性只用于后台显示？？？网站前台是否有用？

apps.py配置app的显示名称
每个app下执行同样操作:

# encoding: utf-8
from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = u"课程"

新建app时并没有引用apps的配置

在app下的init.py中添加:

default_app_config = "operation.apps.OperationConfig"

> <form action="{% url 'login' %}" method="post" autocomplete="off">
                    <div class="form-group marb20 {% if login_form.username.errors %} errorput{% endif %}">
                        <label>用&nbsp;户&nbsp;名</label>
                        <input name="username" id="account_l" type="text" placeholder="手机号/邮箱" />
                    </div>
                    <div class="form-group marb8 {% if login_form.password.errors %} errorput{% endif %}">
                        <label>密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</label>
                        <input name="password" id="password_l" type="password" placeholder="请输入您的密码" />
                    </div>
<div class="error btns login-form-tips" id="jsLoginTips">
{% for key, error in login_form.errors.items %}
{{ error }}
{% endfor %}
{{ msg }}</div>
                     <div class="auto-box marb38">

                        <a class="fr" href="{% url "forget_pwd" %}">忘记密码？</a>
                     </div>
                     <input class="btn btn-green" id="jsLoginBtn" type="submit" value="立即登录 > " />  #此处代码如果加上id就会post->'/user/login'不知道为什么                                  
                <input type="hidden" name="next" value="{{ redirect_url }}" />
                {% csrf_token %}
                </form>

写了一个类继承Django的view，然后写了get post方法(get/post的if是Django替我们完成的)
在url中调用Loginview的as_view方法需要加上括号，进行调用。
Django的form进行表单验证并把error值传到前台。
is_valid方法，验证表单


EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '1956354744@qq.com'
EMAIL_HOST_PASSWORD = 'sjujbnzdrdaaegjb'
EMAIL_USE_TLS = True
EMAIL_FROM = '1956354744@qq.com'
此处的EMAIL_FROM必须和登录账户相同，不然无法发送验证邮件

建议自行走一遍注册，登录，忘记密码。重置密码。
错误的激活链接，错误的重置链接。值回填，form报错

更多: 重置密码链接是否被点击过，过期时间。


django.db.migrations.exceptions.InconsistentMigrationHistory: Migration
admin.0001_initial is applied before its dependency users.0001_initial on
database 'default'
此错误出现在已经初始化users之后再在setting中重新设置users

# 重载authenticate的配置
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
setting 149行   实现能够用邮箱登录

{% ifequal city_id city.id|stringformat:'i' %} 此方法格式化了city.id(整型)，把其变成string类型？？？

setting中加入(用于图片加载等用途)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 此处文件路径设置很重要，主要体现在页面文件调用和上传
'django.template.context_processors.media',  # 添加图片处理器
re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),  # 处理图片显示的url，使用django自带的serve # 猜测还可以使用静态文件路由
template中： <img width="200" height="120" class="scrollLoading" data-url="{{ MEDIA_URL }}{{ course_org.image }}"/>
pagnization也有一些配置，没用到，暂没配置
注意json传输格式，字符串采用双引号。。。标准格式总没错，不标准可能造成bug

收藏功能的实现view在org下   url为 org:add_fav  需要参数为  fav_type 整数 fav_id  此处为整数，应该重构的

class CourseInfoView(LoginRequiredMixin, View): 多重继承，跟顺序相关，首先得继承前置类，最后继承后置类
以上继承的第一个类的源码很简单，但是没看懂
在static/css/muke/common-less.css中删除了如下片段，该片段导致了某些加载该css的模块无法显示logo。。。手动加粗
.logo a {
    display: block;
    height: 60px;
    width: 140px;
    background: url('/static/images/footlogo.png') no-repeat center center;
    text-indent: 100%;
    white-space: nowrap;
    overflow: hidden;
}
.logo a {
    -webkit-transition: background-color 0.2s;
    -moz-transition: background-color 0.2s;
    transition: background-color 0.2s;
}
.logo a:hover {
    background-color: #363c41;
} 


current_page(用于org的所有界面、每个界面都有自定义)和request.path(用于主页的几个界面，无需定义，直接在template中比较)
两者都是取出当前页面的特征值，用来做比较或者别的事。前者是自己在view中定义的传出k-v，后者是在模板选择器中加入request，然后模板中调用

应该是由于js的问题，搜索功能无法正常使用，在deco-common.js中
