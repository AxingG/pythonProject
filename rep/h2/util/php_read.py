import os
import re


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


def php_read(file_path):
    if not os.path.exists(file_path):
        print('文件不存在！')
        return

    print("读取文件：" + file_path)

    with open(file_path, 'r') as file:
        content = file.read()
    # 匹配类名和函数名
    class_pattern = r'class\s+(\w+)Controller\s+extends\s+\w+\s*{'
    function_pattern = r'(?:public|private|protected)\s+function\s+(\w+)(?:Action)?\(.*?\)\s*{'

    # 提取类名
    class_matches = re.findall(class_pattern, content)
    # 提取函数名
    function_matches = re.findall(function_pattern, content)

    for class_name in class_matches:
        for function_name in function_matches:
            function_name = function_name[:-6]  # 去除函数名中的最后一个 "Action"
            print(f"/{class_name}/{function_name}")


php_read(find_project_root() + '/Activity.php')
