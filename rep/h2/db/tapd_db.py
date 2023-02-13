import mysql.connector
from rep.h2.model.tapd_task import Task

dbconfig = {
    'host': 'rm-bp1o78g1nf9kt6rhcto.mysql.rds.aliyuncs.com',
    'user': 'servicemanager',
    'password': 'xcQobpVVhKgXskQwTafbaan8',
    'database': 'serverops',
}

select_sql = "SELECT * FROM tapd_task WHERE task_id ='%s'"
insert_sql = """INSERT INTO tapd_task(task_id, owner, effort, product_line,
                      product_type, story_id, iteration_id, created_at)
                     VALUES ('%s', '%s', %d, '%s', '%s', '%s', '%s', %d)"""
update_sql = "UPDATE tapd_task SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')

'''
建表
    1. 员工表：姓名  日期  工时  产研线  任务id
    2. 迭代表：迭代版本、定版时间
'''


def insertOrUpdate(tasks):
    db = mysql.connector.connect(**dbconfig)
    course = db.cursor()
    for task in tasks:
        # 查询
        s_sql = select_sql % task.task_id
        print(s_sql)
        course.execute(s_sql)
        result = course.fetchone()
        if result is None:
            # insert 数据
            c_sql = insert_sql % (task.task_id, task.owner, task.effort, task.product_line,
                                  task.product_type, task.story_id, task.iteration_id, task.created_at)
            print(c_sql)
            try:
                course.execute(c_sql)
                db.commit()
            except:
                db.rollback()
        else:
            # update 数据
            u_sql = update_sql
    db.close()
