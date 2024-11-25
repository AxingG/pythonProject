import json
from enum import Enum

from rep.h2.net import tapd


class Type(Enum):
    EXTENSION = 1
    DANGER = 2


def get_task_iteration(iteration_id):
    result = tapd.get_iteration(iteration_id)
    res_dict = json.loads(result)
    if 'data' in res_dict:
        for data in res_dict['data']:
            return data['Iteration']


# 获取迭代需求列表
def get_task_story(story_id):
    result = tapd.get_story(story_id)
    res_dict = json.loads(result)
    if 'data' in res_dict:
        for story in res_dict['data']:
            return story['Story']

# 获取需求任务列表
def get_date_tasks(date):
    result = tapd.get_story_tasks_by_date(date)
    result_dict = json.loads(result)
    task_arr = []
    if 'error_msg' in result_dict:
        print(result_dict, date)
        return task_arr
    if 'data' not in result_dict:
        return task_arr
    result_data = result_dict['data']
    for data in result_data:
        task = data['Task']
        task_arr.append(task)
    return task_arr
