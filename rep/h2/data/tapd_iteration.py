import json
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
    print(res_dict)
    result_data = res_dict['data']
    iteration_arr = []
    for data in result_data:
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
    result_data = res_dict['data']
    story_arr = []
    for story in result_data:
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

# 获取需求用例
def get_tcase_info(iteration):
    result = tapd.get_story_tcase(iteration)
    rj = json.loads(result)
    rd = rj['data']
    for tcase in rd:
        print(tcase)

# 实现功能
def get_exception_info():
    iteration_arr = get_iteration_info()
    for iteration in iteration_arr:
        story_arr = get_story_info(iteration)
        get_tcase_info(iteration)


get_exception_info()
