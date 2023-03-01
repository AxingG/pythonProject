import mysql.connector
from rep.h2.model.tapd_model import Task

dbconfig = {
    'host': 'rm-bp1o78g1nf9kt6rhcto.mysql.rds.aliyuncs.com',
    'user': 'servicemanager',
    'password': 'xcQobpVVhKgXskQwTafbaan8',
    'database': 'serverops',
}

iteration_select_sql = "select * from tapd_iteration where iteration_id = %s"
iteration_insert_sql = """insert into tapd_iteration(iteration_id, name, start, end, created_at, update_at)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
iteration_update_sql = """update tapd_iteration set name = %s, start = %s, end = %s, update_at = %s
                        WHERE iteration_id = %s"""

story_select_sql = "select * from tapd_story where story_id = %s"
story_insert_sql = """insert into tapd_story(story_id, iteration_id, name, effort, product_line, product_type, 
                     created_at, update_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
story_update_sql = """update tapd_story set iteration_id = %s, name = %s, effort = %s, product_line = %s, 
                        product_type = %s, update_at = %s WHERE story_id = %s"""

task_select_sql = "select * from tapd_task where task_id = %s"
task_insert_sql = """insert into tapd_task(task_id, owner, effort, product_line,
                      product_type, story_id, iteration_id, created_at, update_at, begin, due)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
task_update_sql = """update tapd_task set owner = %s, effort = %s, product_line = %s, product_type = %s, 
              story_id = %s, iteration_id = %s, update_at = %s, begin = %s, due = %s
              WHERE task_id = %s"""

effort_insert_sql = """insert into tapd_effort(owner, add_effort, leave_effort, time_at, create_at, update_at)
                     VALUES (%s, %s, %s, %s, %s, %s)"""

data_delete_sql = """delete from tapd_task where begin >= %s and begin <= %s"""


def iterationInsertOrUpdate(iterations):
    if len(iterations) == 0:
        return
    db = mysql.connector.connect(**dbconfig)
    course = db.cursor()
    for iteration in iterations:
        # 查询
        course.execute(iteration_select_sql, (iteration.iteration_id,))
        result = course.fetchone()
        if result is None:
            # insert 数据
            result = sql(db, iteration_insert_sql, (iteration.iteration_id, iteration.name, iteration.start,
                                                    iteration.end, iteration.created_at, iteration.update_at))
            print('iteration_insert', iteration.iteration_id, result)
        elif iteration.checkInfo(result):
            # update 数据
            result = sql(db, iteration_update_sql, (iteration.name, iteration.start, iteration.end,
                                                    iteration.update_at, iteration.iteration_id))
            print('iteration_update', iteration.iteration_id, result)
        else:
            print('iteration_none')
    db.close()


def storyInsertOrUpdate(storys):
    if len(storys) == 0:
        return
    db = mysql.connector.connect(**dbconfig)
    course = db.cursor()
    for story in storys:
        # 查询
        course.execute(story_select_sql, (story.story_id,))
        result = course.fetchone()
        if result is None:
            # insert 数据
            result = sql(db, story_insert_sql, (story.story_id, story.iteration_id, story.name, story.effort,
                                                story.product_line, story.product_type, story.created_at,
                                                story.update_at))
            print('story_insert', story.story_id, result)
        elif story.checkInfo(result):
            # update 数据
            result = sql(db, story_update_sql, (story.iteration_id, story.name, story.effort, story.product_line,
                                                story.product_type, story.update_at, story.story_id))
            print('story_update', story.story_id, result)
        else:
            print('story_none')
    db.close()


def taskInsertOrUpdate(tasks):
    if len(tasks) == 0:
        return
    db = mysql.connector.connect(**dbconfig)
    course = db.cursor()
    for task in tasks:
        # 查询
        course.execute(task_select_sql, (task.task_id,))
        result = course.fetchone()
        if result is None:
            # insert 数据
            result = sql(db, task_insert_sql,
                         (task.task_id, task.owner, task.effort, task.product_line, task.product_type,
                          task.story_id, task.iteration_id, task.created_at, task.update_at,
                          task.begin, task.due))
            print('task_insert', task.task_id, result)
        elif task.checkInfo(result):
            # update 数据
            result = sql(db, task_update_sql, (task.owner, task.effort, task.product_line, task.product_type,
                                               task.story_id, task.iteration_id, task.update_at, task.begin,
                                               task.due,
                                               task.task_id))
            print('task_update', task.task_id, result)
        else:
            print('task_none', task.task_id)
    db.close()


def deleteTaskByDate(start, end):
    if start == 0 or end == 0 or start > end:
        print("时间错误")
        return
    db = mysql.connector.connect(**dbconfig)
    result = sql(db, data_delete_sql, (start, end))
    print('task_delete', result)


def ownerInsert(owner_info):
    db = mysql.connector.connect(**dbconfig)
    result = sql(db, effort_insert_sql, (owner_info.owner, owner_info.add_effort, owner_info.leave_effort,
                                         owner_info.time_at, owner_info.create_at, owner_info.update_at))
    print('owner_insert', result)


def sql(db, operation, params=()):
    course = db.cursor()
    try:
        course.execute(operation, params)
        db.commit()
        return True
    except Exception as e:
        print(str(e))
        db.rollback()
        return False
