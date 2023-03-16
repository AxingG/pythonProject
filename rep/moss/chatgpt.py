import json
import os

import openai

# a 是问题
# model 要使用的模型的 ID，访问 OpenAI Docs Models 页面可以查看全部可用的模型
# messages 是请求的文本内容，是一个列表，每个元素以字典类型
# role system 可以设置机器人人设
# role assistant 表示是机器人回复内容
# role user 表示是用户提问内容
# content q 问题内容

openai.api_key = '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'


class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": "一个有20年市场渠道经验的运营总监"}]
        self.filename = "./user_message.json"

    def ask_gpt(self):
        # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
        rsq = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsq.get("choices")[0]["message"]["content"]

    def writeToJson(self):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, 'w') as f:
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            # 追加
            msgs.update({self.user: self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)
        except Exception as e:
            print(f"错误代码：{e}")


def main():
    user = input("清输入用户名称：")
    chat = ChatGPT(user)

    while 1:
        # 限制对话次数 由于 gpt-3.5-turbo 单次请求最大 token 数为：4096
        if len(chat.messages) >= 11:
            print("**************************")
            print("*********强制重置**********")
            print("**************************")
            chat.writeToJson()
            user = input("请输入用户名称：")
            chat = ChatGPT(user)

        # 提问
        q = input(f"【{chat.user}】")

        # 逻辑判断
        if q == "0":
            print("*********退出程序**********")
            chat.writeToJson()
            break
        elif q == "1":
            print("**************************")
            print("*********重置对话**********")
            print("**************************")
            # 写入之前的信息
            chat.writeToJson()
            user = input("清楚入用户名称：")
            chat = ChatGPT(user)
            continue

        # 提问-回答-记录
        chat.messages.append({"role": "user", "content": q})
        answer = chat.ask_gpt()
        print(f"【ChatGPT】：{answer}")
        chat.messages.append({"role": "assistant", "content": answer})


if __name__ == '__main__':
    main()
