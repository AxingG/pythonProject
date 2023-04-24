import requests

# 基础信息
account = 'jzqTCJcw'
password = '00274031-3483-B352-75F0-19B14C3B69FA'
workspace_id = 31316618
open_status = 'open'

api = 'https://api.tapd.cn/'

head = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 Safari/537.36',
}


def get_iteration(iteration_id):
    url = api + 'iterations'
    param = {
        'limit': 5,
        'id': iteration_id,
        'workspace_id': workspace_id,
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


def get_open_iteration():
    url = api + 'iterations'
    param = {
        'limit': 20,
        'status': "open",
        'order': "startdate desc",
        'workspace_id': workspace_id,
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取需求列表
def get_story(story_id):
    url = api + 'stories'
    param = {
        'id': story_id,
        'limit': 50,
        'workspace_id': workspace_id,
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


def get_tasks(owner):
    url = api + 'tasks'
    param = {
        'owner': owner,
        'status': open_status,
        'limit': 100,
        'workspace_id': workspace_id,
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text


# 获取任务列表
def get_story_tasks_by_date(date):
    url = api + 'tasks'
    param = {
        'begin': date,
        'limit': 100,
        'workspace_id': workspace_id,
    }
    response = requests.get(url, params=param, headers=head, auth=(account, password))
    return response.text
