import time

from rep.h2.data import tapd_parse
from rep.h2.db import tapd_db
from rep.h2.model import tapd_model


def getTasks():
    iteration_list = []
    story_list = []
    task_list = []

    iteration_arr = tapd_parse.get_iteration_info()
    for iteration in iteration_arr:
        # 存入相关迭代数据
        iteration_id = iteration['id']
        iteration_model = tapd_model.Iteration(iteration_id)
        iteration_model.name = iteration['name']
        iteration_model.start = int(str(iteration['startdate']).replace('-', ''))
        iteration_model.end = int(str(iteration['enddate']).replace('-', ''))
        iteration_list.append(iteration_model)
        # 遍历story
        story_array = tapd_parse.get_story_info(iteration)
        for story in story_array:
            # 存入相关需求数据
            story_effort = story['effort']
            if story_effort is None:
                continue
            product_line = story['custom_field_six']
            product_type = story['custom_field_three']
            story_id = story['id']
            story_model = tapd_model.Story(story_id)
            story_model.iteration_id = iteration_id
            story_model.name = story['name']
            story_model.effort = float(story_effort)
            story_model.product_line = product_line
            story_model.product_type = product_type
            story_list.append(story_model)
            # 请求任务列表
            time.sleep(1.5)
            task_arr = tapd_parse.get_task_info(iteration, story)
            for task in task_arr:
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
                task_model.story_id = story_id
                task_model.iteration_id = iteration_id
                task_model.begin = int(str(begin).replace('-', ''))
                task_model.due = int(str(due).replace('-', ''))
                task_list.append(task_model)

    tapd_db.iterationInsertOrUpdate(iteration_list)
    tapd_db.storyInsertOrUpdate(story_list)
    return task_list


def insertDB():
    task_list = getTasks()
    tapd_db.taskInsertOrUpdate(task_list)


insertDB()
