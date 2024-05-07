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
        if len(tup) != 6:
            return True
        if self.hour != tup[3]:
            return True
        return False
