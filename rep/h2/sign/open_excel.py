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
    name = '姓名'
    date = '打卡日期'
    time = '打卡时间'
    selected_columns = [name, date, time]
    # 员工数据
    developer = {}
    other = ['温旭峰', '柳诗尧', '赵嘉兴']
    # 处理excel
    df = pd.read_excel(file_path, usecols=selected_columns)
    for index, row in df.iterrows():
        name_value = row[name]
        date_value = row[date]
        time_value = row[time]
        if name_value in other:
            continue
        if name_value not in developer:
            developer[name_value] = tapd_model.Developer(name_value, date_value, time_value)
        else:
            developer[name_value].check_date(date_value, time_value)
    for key, dev in developer.items():
        dev.get_hour()
        sign_model = tapd_model.Sign()
        sign_model.owner = key
        sign_model.time_at = dev.time
        sign_model.hour = dev.hour
        sign_list.append(sign_model)
    tapd_db.developerSignInsert(sign_list)


excel_data()
