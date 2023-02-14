import json
import time
from rep.h2.util import timer
from rep.h2.net import tapd

from enum import Enum


class Type(Enum):
    EXTENSION = 1
    DANGER = 2


# 获取当前迭代列表
def get_iteration_info():
    result = tapd.get_iteration()
    res_dict = json.loads(result)
    iteration_arr = []
    if 'data' in res_dict:
        for data in res_dict['data']:
            iteration = data['Iteration']
            bug_iteration_id = '1131316618001000340'  # 屏蔽线上bug迭代
            start_date = timer.struct_time(iteration['startdate'])
            end_date = timer.struct_time(iteration['enddate'])
            if iteration['id'] != bug_iteration_id and start_date < time.time() < end_date:
                iteration_arr.append(iteration)
    return iteration_arr


# 获取迭代需求列表
def get_story_info(iteration):
    result = tapd.get_iteration_story(iteration)
    res_dict = json.loads(result)
    story_arr = []
    if 'data' in res_dict:
        for story in res_dict['data']:
            story_arr.append(story['Story'])
    return story_arr


# 获取需求任务列表
def get_task_info(iteration, story):
    result = tapd.get_story_tasks(iteration=iteration, story=story)
    result_dict = json.loads(result)
    task_arr = []
    if 'error_msg' in result_dict:
        print(result_dict, story['name'])
        return task_arr
    if 'data' not in result_dict:
        return task_arr
    result_data = result_dict['data']
    for data in result_data:
        task = data['Task']
        task_arr.append(task)

    return task_arr


# 获取需求对应的测试用例关联关系
def get_story_test_info(iteration, story):
    result = tapd.get_story_tcase(iteration, story)
    rj = json.loads(result)
    tcase0_arr = []
    if 'data' in rj:
        rd = rj['data']
        tcase_id = []
        for test in rd:
            tcase = test['TestPlanStoryTcaseRelation']
            if tcase['tcase_id'] not in tcase_id:
                tcase_id.append(tcase['tcase_id'])
                case = get_tcase_info(iteration, tcase)
                if case is not None:
                    tcase0_arr.append(case)
    return tcase0_arr


# 获取用例计划对应测试用例
def get_tcase_info(iteration, tcase):
    result = tapd.get_tcase(iteration, tcase)
    rj = json.loads(result)
    if 'data' in rj:
        case = rj['data'][0]['Tcase']
        if case['priority'] == 'P0':
            return case
    return None
