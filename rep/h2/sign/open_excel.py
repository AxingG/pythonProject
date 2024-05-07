import pandas as pd
import os
from rep.h2.db import tapd_db
from rep.h2.model import tapd_model

sign_list = []


def find_project_root():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    # 定义一个标识文件名
    marker_file = "rep"
    # 不断向上遍历目录，直到找到包含标识文件的目录
    while current_directory:
        potential_project_root = os.path.join(current_directory, marker_file)
        if os.path.exists(potential_project_root):
            return current_directory
        current_directory = os.path.dirname(current_directory)

    # 如果没有找到标识文件，返回当前脚本所在的目录
    return os.path.dirname(os.path.realpath(__file__))


def excel_data():
    # 文档数据
    file_path = find_project_root() + '/develop_data.xlsx'
    if not os.path.exists(file_path):
        print('文件不存在！')
        return
    name = '姓名'
    date = '日期'
    time = '时长'
    selected_columns = [name, date, time]
    # 员工数据
    developer = {}
    other = ['温旭峰', '柳诗尧', '赵嘉兴', '项朝龙']
    # 处理excel
    df = pd.read_excel(file_path, usecols=selected_columns)
    for index, row in df.iterrows():
        name_value = row[name]
        date_value = row[date]
        time_value = row[time]
        if name_value in other:
            continue
        if name_value == '高强强':
            name_value = '高强'
        sign_model = tapd_model.Sign()
        sign_model.owner = name_value
        sign_model.time_at = date_value
        sign_model.hour = time_value
        sign_list.append(sign_model)
        print(sign_model.owner, sign_model.time_at, sign_model.hour)
    tapd_db.developerSignInsert(sign_list)

# excel_data()


def single():
    sign_model = tapd_model.Sign()
    sign_model.owner = '高启航'
    sign_model.time_at = 202404
    sign_model.hour = 104
    sign_list.append(sign_model)
    tapd_db.developerSignInsert(sign_list)

# single()
