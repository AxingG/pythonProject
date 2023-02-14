from datetime import datetime
import time


# 时间结构化
def struct_time(date):
    struct_t = time.strptime(date, '%Y-%m-%d')
    return time.mktime(struct_t)


def struct_time_2(date):
    struct_t = time.strptime(date, '%Y-%m-%d %H:%M:%S')
    return time.mktime(struct_t)


# 获取当天零点
def get_today_zero():
    now_time = int(time.time())
    day_time = now_time - now_time % 86400 + time.timezone
    return day_time


def get_date(t_str):
    return datetime.strptime(t_str, '%Y-%m-%d')
