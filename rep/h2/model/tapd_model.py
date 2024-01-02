import time
from rep.h2.util.timer import time_to_seconds, struct_time_3, struct_time_4


class Iteration:
    iteration_id = str
    name = str
    start = int
    end = str

    def __init__(self, iteration_id):
        self.iteration_id = iteration_id
        self.created_at = int(time.time())
        self.update_at = int(time.time())

    def checkInfo(self, tup):
        print(tup)
        if len(tup) != 7:
            return True
        if self.name != tup[2]:
            return True
        if self.start != tup[3]:
            return True
        if self.end != tup[4]:
            return True
        return False


class Story:
    story_id = str
    iteration_id = str
    name = str
    effort = float
    product_line = str
    product_type = str

    def __init__(self, story_id):
        self.story_id = story_id
        self.created_at = int(time.time())
        self.update_at = int(time.time())

    def checkInfo(self, tup):
        print(tup)
        if len(tup) != 9:
            return True
        if self.iteration_id != tup[2]:
            return True
        if self.name != tup[3]:
            return True
        if self.effort != tup[4]:
            return True
        if self.product_line != tup[5]:
            return True
        if self.product_type != tup[6]:
            return True
        return False


class Task:
    begin = int
    due = int
    owner = str
    effort = float
    product_line = str
    product_type = str
    story_id = str
    iteration_id = str

    def __init__(self, task_id):
        self.task_id = task_id
        self.created_at = int(time.time())
        self.update_at = int(time.time())

    def checkInfo(self, tup):
        print(tup)
        if len(tup) != 12:
            return True
        if self.owner != tup[2]:
            return True
        if self.effort != tup[3]:
            return True
        if self.product_line != tup[6]:
            return True
        if self.story_id != tup[7]:
            return True
        if self.iteration_id != tup[8]:
            return True
        if self.product_type != tup[9]:
            return True
        if self.begin != tup[10]:
            return True
        if self.due != tup[11]:
            return True
        return False


class Owner:
    owner = str
    add_effort = float
    leave_effort = float
    time_at = int
    create_at = int
    update_at = int
    department = int

    def __init__(self):
        self.create_at = int(time.time())
        self.update_at = int(time.time())


class Developer:
    name = str
    # 当月一共打卡多久
    hour = float
    # 哪个月 201312
    time = int
    # 每月日期列表，里面放打过卡的日期
    data = []
    # 打卡时间列表，里面放 打过卡日期 对应的打卡数据
    sign_time = {}

    def __init__(self, init_name, init_date, init_time):
        self.time = struct_time_4(init_date)
        self.name = init_name
        self.sign_time = {}
        date_str = struct_time_3(init_date)
        self.date = [date_str]
        self._add_time(date_str, init_time)

    def check_date(self, new_date, new_time):
        date_str = struct_time_3(new_date)
        if date_str not in self.date:
            self.date.append(date_str)
        self._add_time(date_str, new_time)

    def _add_time(self, new_date, new_time):
        check_second = time_to_seconds("14:00:00")
        new_second = time_to_seconds(new_time)
        if new_second > check_second:
            # 下班打卡
            time_key = new_date + "_下班"
        else:
            # 上班打卡
            time_key = new_date + "_上班"

        if time_key not in self.sign_time:
            # 没有key
            self.sign_time[time_key] = new_second
        else:
            ori_second = time_to_seconds(self.sign_time[time_key])
            if '上班' in time_key:
                # 上班，谁小用谁
                self.sign_time[time_key] = min(ori_second, new_second)
            else:
                # 下班，谁大用谁
                self.sign_time[time_key] = max(ori_second, new_second)

    def get_hour(self):
        total_seconds = 0
        for value in self.date:
            half_day = False
            if value + "_上班" not in self.sign_time:
                self.sign_time[value + "_上班"] = time_to_seconds('13:30:00')
                half_day = True
            elif value + "_下班" not in self.sign_time:
                self.sign_time[value + "_下班"] = time_to_seconds('12:00:00')
                half_day = True
            up_time = self.sign_time.get(value + "_上班")
            down_time = self.sign_time.get(value + "_下班")
            if half_day:
                total_seconds += down_time - up_time
            else:
                total_seconds += down_time - up_time - time_to_seconds('01:30:00')
        # self.name 和 total_seconds 是名字和hour
        self.hour = round(total_seconds / 3600, 2)


class Sign:
    owner = str
    time_at = int
    hour = float
    create_at = int
    update_at = int

    def __init__(self):
        self.create_at = int(time.time())
        self.update_at = int(time.time())

    def checkInfo(self, tup):
        print(tup)
        if len(tup) != 6:
            return True
        if self.hour != tup[3]:
            return True
        return False
