import time

import requests
import datetime
from bs4 import BeautifulSoup

# url = 'https://www.tapd.cn/31316618/prong/iterations/card_view'
url = 'https://www.tapd.cn/31316618/prong/iterations/get_next_page_iterations'

param = {
    # 'q': 'fcc8cff7fdf986e7a9de74971131a8fd',
    'iteration_id': '1131316618001000387',
    'page': 1,
    'isShowParentWorkspaceName': 'true',
    'limit': 10,
    'time1673418317607': ''
}

head = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Cookie': 'tui_filter_fields=["title","current_owner","status","priority"]; isCloseIterationTips=1; 343476245_31316618_/prong/iterations/index_remember_view=1131316618001001096; 1773319067_31316618_/prong/iterations/index_remember_view=1131316618001029376; iter_card_status=; 343476245_31316618_iterations_card_view_close_status=0; tui_filter_fields=["title","current_owner","status","priority"]; 343476245_31316618_/prong/tasks/index_remember_view=1131316618001003793; 1773319067_31316618_/prong/tasks/index_remember_view=1131316618001029401; tui_filter_fields=["name","owner","iteration_id","priority","begin"]; 31316618_1131316618001000004_story_create_template=1131316618001000018; _qddaz=QD.129027452314209; iteration_view_type_cookie=card_view; corpid=wwea95305789c25271; agentid=1000011; 343476245_31316618_board_type=standard_board; 31316618bug_create_template=1131316618001000285; new_worktable=search_filter; __root_domain_v=.tapd.cn; sort_task_list_common=due;DESC; lastSE=baidu; iteration_card__1773319067_31316618=1; _t_crop=23759121; tapd_div=101_1; iteration_card__343476245_31316618=1; iteration_card_current_iteration_31316618=1131316618001000387; dsc-token=MYnWlLaR97MvIe4m; tapdsession=16734175124068e286f04cf783e9f54cf8f19a0933a4c54d9fa5e84eacab8260f558e15621; locale=zh_CN; _qdda=3-1.3ec4p5; _qddab=3-7zq5w3.lcr9kxjg; t_u=a880fb3c68c50f220c8a215d03e4a797e6c35d4bd2336b70165f58a61defe178be21feae64a869ea1a7b3799bdc8f413643c8f6789ff28db5e3c1915b892c931e494079d6f8a2d99|1; t_cloud_login=zhaojiaxing@dailyyoga.com; _t_uid=343476245; cloud_current_workspaceId=31316618; _wt=eyJ1aWQiOiIzNDM0NzYyNDUiLCJjb21wYW55X2lkIjoiMjM3NTkxMjEiLCJleHAiOjE2NzM0MTg2MTJ9.65ecfc52af2361ecc450c4503dfe74190a5c157faa07f22b51b26d02ae95ccaa'
}

response = requests.get(url, params=param, headers=head)
page_text = response.text
content = response.content

soup = BeautifulSoup(page_text, 'html.parser')

r = soup.find('div')
span = soup.find('span')

current_version_name = ''
iterationId = ''
if span.text.strip() == '当前':
    current_version_name = r.get('iteration_title')
    iterationId = r.get('iteration_id')
    print(current_version_name)
    print(iterationId)

urlVersion = 'https://www.tapd.cn/31316618/prong/iterations/ajax_get_card_view_by_iteration_id/' + iterationId

paramVersion = {
    'limit': 50,
    'page': 1,
    'types[]': 'story',
    'time': int(round(time.time() * 1000)),
}

responseVersion = requests.get(urlVersion, params=paramVersion, headers=head)
print(responseVersion.text)


