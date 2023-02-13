import time

from rep.h2.data import tapd_iteration
from rep.h2.db import tapd_db
from rep.h2.model import tapd_task


def getTasks():
    task_list = []
    iteration_arr = tapd_iteration.get_iteration_info()
    for iteration in iteration_arr:
        iteration_id = iteration['id']
        story_array = tapd_iteration.get_story_info(iteration)
        for story in story_array:
            time.sleep(1.5)
            product_line = story['custom_field_six']
            product_type = story['custom_field_three']
            story_id = story['id']
            task_arr = tapd_iteration.get_task_info(iteration, story)
            for task in task_arr:
                if len(task_list) == 1:
                    return task_list
                owner = task['owner']
                effort = task['effort']
                if owner is None or effort is None:
                    continue
                if ';' in owner:
                    owner = str(owner).replace(';', '')
                task_id = task['id']
                print(task)
                task_model = tapd_task.Task(task_id, owner, float(effort), product_line,
                                            product_type, story_id, iteration_id)
                task_list.append(task_model)
    return task_list


def insertDB():
    task_list = getTasks()
    # tapd_db.insertOrUpdate(task_list)


insertDB()
