import time

from rep.h2.data import tapd_parse
from rep.h2.db import tapd_db
from rep.h2.model import tapd_model
from dateutil.parser import parse
# 需求池、线上问题 对应的4个迭代
other_iteration = ["1131316618001000423", "1131316618001000424", "1131316618001000425", "1131316618001000184"]
# 产品
other_owner = ["刘庆华", "史伟峰", "陈书秀", "张益豪", "杨国花"]
# 产品工时
other_owner_effort = {}

t_list = []

task_model_list = []
story_model_list = []
iteration_model_list = []


def initTask(story):
    story_id = story['id']
    product_line = story['custom_field_six']
    product_type = story['custom_field_three']
    for task in t_list:
        if task['story_id'] == story_id:
            owner = task['owner']
            effort = task['effort']
            begin = task['begin']
            due = task['due']
            if owner is None or effort is None or begin is None or due is None:
                continue
            if ';' in owner:
                owner = str(owner).replace(';', '')
            task_id = task['id']
            task_model = tapd_model.Task(task_id)
            task_model.owner = owner
            task_model.effort = float(effort)
            task_model.product_line = product_line
            task_model.product_type = product_type
            task_model.story_id = task['story_id']
            task_model.iteration_id = task['iteration_id']
            task_model.begin = int(str(begin).replace('-', ''))
            task_model.due = int(str(due).replace('-', ''))
            task_model_list.append(task_model)


def initStory(story):
    story_effort = story['effort']
    if story_effort is None:
        return
    story_id = story['id']
    # 需求工时减去产品工时
    other_effort = other_owner_effort.setdefault(story_id, None)
    if other_effort is not None:
        story_effort = float(story_effort) - other_effort
    story_model = tapd_model.Story(story_id)
    story_model.iteration_id = story['iteration_id']
    story_model.name = story['name']
    story_model.effort = float(story_effort)
    story_model.product_line = story['custom_field_six']
    story_model.product_type = story['custom_field_three']
    story_model_list.append(story_model)


def initIteration(iteration):
    iteration_id = iteration['id']
    iteration_model = tapd_model.Iteration(iteration_id)
    iteration_model.name = iteration['name']
    iteration_model.start = int(str(iteration['startdate']).replace('-', ''))
    iteration_model.end = int(str(iteration['enddate']).replace('-', ''))
    iteration_model_list.append(iteration_model)


def insertDB():
    tapd_db.iterationInsertOrUpdate(iteration_model_list)
    tapd_db.storyInsertOrUpdate(story_model_list)
    tapd_db.taskInsertOrUpdate(task_model_list)


def getTask(start, end):
    story_id_list = []
    iteration_id_list = []
    for num in range(start, end):
        date = parse(str(num))
        time.sleep(1)
        task_arr = tapd_parse.get_date_tasks(date)
        for task in task_arr:
            iteration_id = task['iteration_id']
            task_owner = task['owner']
            story_id = task['story_id']
            effort = task['effort']
            if iteration_id in other_iteration or effort is None:
                continue
            if ';' in task_owner:
                task_owner = str(task_owner).replace(';', '')
            if task_owner in other_owner:
                # 记录产品任务总工时
                other_effort = other_owner_effort.setdefault(story_id, 0)
                other_effort = other_effort + float(effort)
                other_owner_effort.update({story_id: other_effort})
                continue
            t_list.append(task)
            if story_id not in story_id_list and story_id is not None:
                story_id_list.append(story_id)
            if iteration_id not in iteration_id_list and iteration_id is not None:
                iteration_id_list.append(iteration_id)

    for s_id in story_id_list:
        time.sleep(1)
        story = tapd_parse.get_task_story(s_id)
        if story is None:
            print('需求有问题', s_id)
            continue
        initTask(story)
        initStory(story)

    for it_id in iteration_id_list:
        time.sleep(1)
        iteration = tapd_parse.get_task_iteration(it_id)
        if iteration is None:
            print('迭代有问题', it_id)
            continue
        initIteration(iteration)

    insertDB()
    return


def deleteTask(start, end):
    """
        删除tapd_task表的数据，依据begin做条件查询，其中：
        start:  开始时间
        end:    结束时间
    """
    tapd_db.deleteTaskByDate(start, end)


# deleteTask(20231013, 20231018)
# getTask(20231101, 20231131)


def addOtherInfo():
    owner_info = tapd_model.Owner()
    owner_info.owner = '王奕娇'
    owner_info.add_effort = 0
    owner_info.leave_effort = 0
    owner_info.time_at = 20231125
    owner_info.department = 1  # 1. 技术研发中心 2. 非技术研发中心
    tapd_db.ownerInsert(owner_info)


# addOtherInfo()
