import requests

# 基础信息
account = 'jzqTCJcw'
password = '00274031-3483-B352-75F0-19B14C3B69FA'
workspace_id = 31316618
iteration_status = 'open'

api = 'https://api.tapd.cn/'

head = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 Safari/537.36',
}


# 获取迭代列表
def get_iteration():
    url = api + 'iterations'
    param = {
        'limit': 5,
        'status': iteration_status,
        'workspace_id': workspace_id,
        'order': 'startdate desc',
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取需求列表
def get_iteration_story(iteration):
    url = api + 'stories'
    param = {
        'iteration_id': iteration['id'],
        'limit': 50,
        'workspace_id': iteration['workspace_id'],
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取任务列表
def get_story_tasks(iteration, story):
    url = api + 'tasks'
    param = {
        'iteration_id': iteration['id'],
        'story_id': story['id'],
        'limit': 50,
        'workspace_id': iteration['workspace_id'],
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取需求对应测试用例
def get_story_tcase(iteration, story):
    url = api + 'stories/get_story_tcase'
    param = {
        'story_id': story['id'],
        'limit': 50,
        'workspace_id': iteration['workspace_id'],
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取测试用例
def get_tcase(iteration, tcase):
    url = api + 'tcases'
    param = {
        'workspace_id': iteration['workspace_id'],
        'id': tcase['tcase_id']
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text
