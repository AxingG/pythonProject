import datetime
import time


def struct_time(date):
    struct_t = time.strptime(date, '%Y-%m-%d')
    return time.mktime(struct_t)


def struct_time_2(date):
    struct_t = time.strptime(date, '%Y-%m-%d %H:%M:%S')
    return time.mktime(struct_t)


def struct_time_3(date):
    return date.strftime('%Y-%m-%d')


def struct_time_4(date):
    return date.strftime('%Y%m')


# 获取当天零点
def get_today_zero():
    now_time = int(time.time())
    day_time = now_time - now_time % 86400 + time.timezone
    return day_time


def get_date(t_str):
    return datetime.strptime(t_str, '%Y-%m-%d')


def time_to_seconds(str_time):
    if type(str_time) is int:
        return str_time
    elif type(str_time) is str:
        hours, minutes, seconds = map(int, str_time.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    elif isinstance(str_time, datetime.time):
        hours, minutes, seconds = str_time.hour, str_time.minute, str_time.second
        return hours * 3600 + minutes * 60 + seconds
    else:
        print(str_time, type(str_time))
        return str_time
