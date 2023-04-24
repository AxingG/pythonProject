import collections
import time
from rep.h2.data import tapd_parse


def get_iteration_our(people, days):
    return people * days * 8


'''
  DY: 10人
  D：5人
  π：5人
'''
dev_owner = {'王奕娇;', '王媛;', '高强;', '侯维维;', '林军;', '贾宇光;', '张伟;', '高哲;', '徐培帅;', '曹永胜;',
             '高祥;', '秦浩楠;', '万雪婷;', '李正祥;', '王成斌;', '苏帅龙;', '吴华友;', '徐培帅;', '乔天良;', '马廉;',
             '张梦佳;'}


def get_tasks(num):
    dev_end = {}
    for name in dev_owner:
        task_arr = tapd_parse.get_tasks(name)
        max_end = 0
        for task in task_arr:
            begin = task['begin']
            if begin is None:
                continue
            num_begin = int(str(begin).replace('-', ''))
            if max_end < num_begin:
                max_end = num_begin
        if max_end < num:
            dev_end[name] = max_end
            print(name, max_end)


def get_open_iter():
    iter_arr = tapd_parse.get_open_iteration()
    for iter in iter_arr:
        print(iter)


get_open_iter()
