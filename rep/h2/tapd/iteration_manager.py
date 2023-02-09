from rep.h2.data import tapd_iteration


def get_iteration_our(people, days):
    return people * days * 8


'''
  DY: 10人
  D：5人
  π：5人
'''
dy_owner = {'王奕娇;', '王媛;', '高强;', '侯维维;', '林军;', '贾宇光;', '张伟;', '高哲;', '徐培帅;', '曹永胜;'}
df_owner = {'秦浩楠;', '万雪婷;', '李正祥;', '王成斌;', '苏帅龙;'}
pi_owner = {'吴华友;', '徐培帅;', '乔天良;', '马廉;', '张梦佳;'}

dy_stand_time = 8 * 17
df_stand_time = 8 * 12


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


def get_owner_time(owner_dict):
    get_time = 0
    get_time_pi = 0
    for key in owner_dict:
        effect = owner_dict[key]
        if key in dy_owner:
            time = effect - dy_stand_time
            if time != 0:
                get_time += time
                print(key, time)
        elif key in df_owner:
            time = effect - df_stand_time
            if time != 0:
                get_time += time
                print(key, time)
        else:
            get_time_pi += effect
            print(key, effect)
    print(get_time, get_time_pi)


def get_iteration_standard_percent():
    # DY V9.28 2月2日 - 2月24日
    dy_hour = get_iteration_our(10, 17)
    # DF V1.1 V1.8 2月2日 - 2月17日
    df_hour = get_iteration_our(5, 12)

    print('DY', dy_hour, '工时')
    print('DF', df_hour, '工时')


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
    # 获取D迭代总工时
    d_time = get_iteration_time('D-', business_dict)
    print('d', d_time)
    # 获取D迭代每个人的工时
    d_owner_time = get_iteration_owner_time('D-', business_owner_dict)
    print(d_owner_time)
    # 获取所有人的总工时 DY 136 D 96
    owner_dict = {}
    for key in dy_owner_time:
        if key in owner_dict:
            owner_dict[key] = owner_dict[key] + dy_owner_time[key]
        else:
            owner_dict[key] = dy_owner_time[key]
    for key in d_owner_time:
        if key in owner_dict:
            owner_dict[key] = owner_dict[key] + d_owner_time[key]
        else:
            owner_dict[key] = d_owner_time[key]
    print(owner_dict)
    get_owner_time(owner_dict)


# 迭代总工时 DY、DF占比
get_iteration_standard_percent()
# DY、DF 各自的占比
get_story_standard_percent()
