>设计model的时候的__unicode__方法
def __str__(self):
    return self.name
   3.6也可以重载unicode，但是后台显示可能出问题

import pymysql
pymysql.install_as_MySQLdb()
