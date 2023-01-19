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
            start_date = timer.struct_time(iteration['startdate'])
            end_date = timer.struct_time(iteration['enddate'])
            if start_date < time.time() < end_date:
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
def get_task_info(iteration, story, type):
    result = tapd.get_story_tasks(iteration=iteration, story=story)
    result_dict = json.loads(result)
    result_data = result_dict['data']
    for data in result_data:
        task = data['Task']
        if task['due'] is not None:
            end_time = int(timer.struct_time(task['due']))
            if task['status'] == 'done':
                print('done')
                continue
            if type == Type.EXTENSION and timer.get_today_zero() > end_time:
                # 已经延期的 08:30 执行
                day = int((timer.get_today_zero() - end_time) / 86400)
                print('已经延期的', iteration['name'], story['name'], task['owner'], task['name'], '延期', day, '天')
            if type == Type.DANGER and timer.get_today_zero() == end_time:
                # 当天结束目前还未完成 18:00 执行
                print('当天结束目前还未完成', iteration['name'], story['name'], task['owner'], task['name'],
                      task['due'])
    return


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


# 实现功能
def get_exception_info():
    iteration_arr = get_iteration_info()
    for iteration in iteration_arr:
        story_arr = get_story_info(iteration)
        for story in story_arr:
            get_task_info(iteration, story, Type.EXTENSION)
            # tcase0_arr = get_story_test_info(iteration, story)
            # print(story)
            # print(tcase0_arr)
            # print(len(tcase0_arr), '\n')


get_exception_info()
