import datetime

import pandas as pd
import os


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


def time_to_seconds(str_time):
    if type(str_time) is int:
        return str_time
    elif type(str_time) is str:
        hours, minutes, seconds = map(int, str_time.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    elif type(str_time) is datetime.time:
        hours, minutes, seconds = str_time.hour, str_time.minute, str_time.second
        return hours * 3600 + minutes * 60 + seconds
    else:
        print(str_time, type(str_time))
        return str_time


class Develop:

    def __init__(self, init_name, init_date, init_time):
        self.time = {}
        self.total_seconds = {}
        self.name = init_name
        date_str = init_date.strftime('%Y-%m-%d')
        self.date = [date_str]
        self._add_time(date_str, init_time)

    def _add_time(self, new_date, new_time):
        check_second = time_to_seconds("14:00:00")
        new_second = time_to_seconds(new_time)
        if new_second > check_second:
            # 下班打卡
            time_key = new_date + "_下班"
        else:
            # 上班打卡
            time_key = new_date + "_上班"

        if time_key not in self.time:
            # 没有key
            self.time[time_key] = new_second
        else:
            ori_second = time_to_seconds(self.time[time_key])
            if '上班' in time_key:
                # 上班，谁小用谁
                self.time[time_key] = min(ori_second, new_second)
            else:
                # 下班，谁大用谁
                self.time[time_key] = max(ori_second, new_second)

    def check_date(self, new_date, new_time):
        date_str = new_date.strftime('%Y-%m-%d')
        if date_str not in self.date:
            self.date.append(date_str)
        self._add_time(date_str, new_time)

    def get_hour(self):
        total_seconds = 0
        if self.name in other:
            return
        for value in self.date:
            if value + "_上班" not in self.time:
                self.time[value + "_上班"] = down
            elif value + "_下班" not in self.time:
                self.time[value + "_下班"] = up
            up_time = self.time.get(value + "_上班")
            down_time = self.time.get(value + "_下班")
            total_seconds += down_time - up_time - sleep
        self.total_seconds[self.name] = total_seconds
        sorted_dict = dict(sorted(self.total_seconds.items(), key=lambda item: item[1], reverse=True))
        for key, value in sorted_dict.items():
            hours = value // 3600
            remaining_seconds = value % 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            print(key, f"{hours}小时", f"{minutes}分钟", f"{seconds}秒")


def excel_data():
    for index, row in df.iterrows():
        name_value = row[name]
        date_value = row[date]
        time_value = row[time]

        if name_value not in developer:
            developer[name_value] = Develop(name_value, date_value, time_value)
        else:
            developer[name_value].check_date(date_value, time_value)


# 文件路径
file_path = find_project_root() + '/develop_data.xlsx'

other = ['温旭峰', '柳诗尧', '赵嘉兴']

name = '姓名'
date = '打卡日期'
time = '打卡时间'

selected_columns = [name, date, time]

df = pd.read_excel(file_path, usecols=selected_columns)

developer = {}

excel_data()

up = time_to_seconds('12:00:00')
down = time_to_seconds('13:30:00')
sleep = time_to_seconds('01:30:00')

print("11月打卡时长")
for key, dev in developer.items():
    dev.get_hour()
