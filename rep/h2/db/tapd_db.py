import mysql.connector
from rep.h2.model.tapd_task import Task

dbconfig = {
    'host': 'rm-bp1o78g1nf9kt6rhcto.mysql.rds.aliyuncs.com',
    'user': 'servicemanager',
    'password': 'xcQobpVVhKgXskQwTafbaan8',
    'database': 'serverops',
}

select_sql = "SELECT * FROM tapd_task WHERE task_id ='%s'"

def connect_db():
    db = mysql.connector.connect(**dbconfig)
    return db.cursor()


'''
建表
    1. 员工表：姓名  日期  工时  产研线  任务id
    2. 迭代表：迭代版本、定版时间
'''


def insertOrUpdate(tasks):
    course = connect_db()
    for task in tasks:
        # 查询
        sql = select_sql % task.task_id
        result = course.execute(sql)
        print(result)


def create_table(cursor):
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)


connect_db()
