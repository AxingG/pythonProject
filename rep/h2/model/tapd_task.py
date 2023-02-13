class Task:
    def __init__(self, task_id, owner, start_day, effort):
        self.task_id = task_id
        self.owner = owner
        self.start_day = start_day
        self.effort = effort
        self.created_at = 0,  # 当前时间戳
        self.update_at = 0,  # 更新时间戳
