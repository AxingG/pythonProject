import time


class Task:
    def __init__(self, task_id, owner, effort, product_line, product_type,
                 story_id, iteration_id):
        self.task_id = task_id
        self.owner = owner
        self.effort = effort
        self.product_line = product_line
        self.product_type = product_type

        # 当前时间戳
        self.created_at = int(time.time())
        # 更新时间戳
        self.update_at = int(time.time())
