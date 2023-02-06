from rep.h2.data import tapd_iteration


def get_iteration_our(people, days):
    return people * days * 8


'''
  DY: 10人
  D：5人
  π：5人
'''


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
    story_dict = {}
    for iteration in iteration_arr:
        story_array = tapd_iteration.get_story_info(iteration)
        for story in story_array:
            # 需要的字段 产研线：custom_fiel'_six 预估工时：effort
            business_line = story['custom_field_six']
            story_time = float(story['effort'])
            if business_line in story_dict:
                story_dict[business_line] = story_dict[business_line] + story_time
            else:
                story_dict[business_line] = story_time
    print(story_dict)

    dy_time = 0
    for key in story_dict:
        if 'DY-' in key:
            dy_time += story_dict[key]
    print(dy_time)


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
