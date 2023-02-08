from rep.h2.data import tapd_iteration


def get_iteration_our(people, days):
    return people * days * 8


'''
  DY: 10人
  D：5人
  π：5人
'''


# 检查具体需求里面的某个人的异常
def get_story_time(iteration, story):
    business_line = story['custom_field_six']
    name = story['name']
    if business_line != 'DY-商业线' or '需求5' not in name:
        return
    task_arr = tapd_iteration.get_task_info(iteration, story)
    story_time = story['effort']
    task_time = 0
    owner_dict = {}
    for task in task_arr:
        effort = task['effort']
        owner = task['owner']
        owner_time = float(effort)
        task_time += owner_time
        if owner in owner_dict:
            owner_dict[owner] = owner_dict[owner] + owner_time
        else:
            owner_dict[owner] = owner_time
        if '高强' in owner:
            print(task['name'], owner_time)
    print(story_time, task_time, owner_dict)


# 添加产研线对应工时
def add_story_dict(story, story_dict):
    # 需要的字段 产研线：custom_fiel'_six 预估工时：effort
    business_line = story['custom_field_six']
    effort = story['effort']
    if effort is not None:
        story_time = float(effort)
        if business_line in story_dict:
            story_dict[business_line] = story_dict[business_line] + story_time
        else:
            story_dict[business_line] = story_time
    return story_dict


# 计算迭代总工时
def get_iteration_time(iteration_name, story_dict):
    dy_time = 0
    for key in story_dict:
        if iteration_name in key:
            dy_time += story_dict[key]
    return dy_time


def get_iteration_owner_time(iteration_name, business_owner_dict):
    iteration_owner_dict = {}
    for business_key in business_owner_dict:
        if iteration_name in business_key:
            owner_dict = business_owner_dict[business_key]
            for owner_key in owner_dict:
                if owner_key in iteration_owner_dict:
                    iteration_owner_dict[owner_key] = iteration_owner_dict[owner_key] + owner_dict[owner_key]
                else:
                    iteration_owner_dict[owner_key] = owner_dict[owner_key]
    return iteration_owner_dict


# 计算迭代中所有员工的工时
def get_iteration_task_time(business_owner_dict, iteration, story):
    business_line = story['custom_field_six']
    owner_dict = {}
    task_arr = tapd_iteration.get_task_info(iteration, story)
    # 如果已经存在该产研线，取出字段直接操作
    if business_line in business_owner_dict:
        owner_dict = business_owner_dict[business_line]
    for task in task_arr:
        owner = task['owner']
        effort = task['effort']
        if owner is None or effort is None:
            continue
        owner_time = float(effort)
        if owner in owner_dict:
            owner_dict[owner] = owner_dict[owner] + owner_time
        else:
            owner_dict[owner] = owner_time
    # 更新
    business_owner_dict[business_line] = owner_dict
    return business_owner_dict


def get_iteration_standard_percent():
    # DY V9.28 2月2日 - 2月24日
    dy_hour = get_iteration_our(10, 17) + 8 * 8 + 4
    # DF V1.1 V1.8 2月2日 - 2月17日
    df_hour = get_iteration_our(5, 12)

    dy_percent = str(round(dy_hour / (dy_hour + df_hour) * 100)) + '%'
    df_percent = str(round(df_hour / (dy_hour + df_hour) * 100)) + '%'

    print('DY', dy_hour, '工时')
    print('DF', df_hour, '工时')
    print('DY', dy_percent)
    print('DF', df_percent)


def get_story_standard_percent():
    iteration_arr = tapd_iteration.get_iteration_info()
    business_dict = {}
    business_owner_dict = {}
    for iteration in iteration_arr:
        story_array = tapd_iteration.get_story_info(iteration)
        for story in story_array:
            # 添加产研线对应工时
            business_dict = add_story_dict(story, business_dict)
            # 添加产研线对应员工的对应工时
            business_owner_dict = get_iteration_task_time(business_owner_dict, iteration, story)
    print(business_dict)
    print(business_owner_dict)
    # 获取DY迭代总工时
    dy_time = get_iteration_time('DY-', business_dict)
    print('dy', dy_time)
    # 获取DY迭代每个人的工时
    dy_owner_time = get_iteration_owner_time('DY-', business_owner_dict)
    print(dy_owner_time)



# 迭代总工时 DY、DF占比
get_iteration_standard_percent()
# DY、DF 各自的占比
get_story_standard_percent()

# if task['due'] is not None:
#     end_time = int(timer.struct_time(task['due']))
#     if task['status'] == 'done':
#         print('done')
#         continue
#     if type == Type.EXTENSION and timer.get_today_zero() > end_time:
#         # 已经延期的 08:30 执行
#         day = int((timer.get_today_zero() - end_time) / 86400)
#         print('已经延期的', iteration['name'], story['name'], task['owner'], task['name'], '延期', day, '天')
#     if type == Type.DANGER and timer.get_today_zero() == end_time:
#         # 当天结束目前还未完成 18:00 执行
#         print('当天结束目前还未完成', iteration['name'], story['name'], task['owner'], task['name'],
#               task['due'])
