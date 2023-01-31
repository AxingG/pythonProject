import os

import openai

# model 要使用的模型的 ID，访问 OpenAI Docs Models 页面可以查看全部可用的模型
# prompt 生成结果的提示文本，即你想要得到的内容描述
# max_tokens 生成结果时的最大tokens数，不能超过模型的上下文长度，可以把结果内容复制到OpenAI Tokenizer来了解tokens的计数方式
# temperature: 控制结果的随机性，如果希望结果更有创意可以尝试 0.9，或者希望有固定结果可以尝试 0.0
# top_p: 一个可用于代替 temperature 的参数，对应机器学习中 nucleus sampling，如果设置 0.1 意味着只考虑构成前 10% 概率质量的 tokens
# frequency_penalty: -2.0 ~ 2.0 之间的数字，正值会根据新 tokens 在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性
# presence_penalty: -2.0 ~ 2.0 之间的数字，正值会根据到目前为止是否出现在文本中来惩罚新 tokens，从而增加模型谈论新主题的可能性
# stop: 最大长度为 4 的字符串列表，一旦生成的 tokens 包含其中的内容，将停止生成并返回结果


openai.api_key = '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'

while 0 < 1:
    print('\n请输入：')
    a = input()
    a.isspace()
    if len(a) == 0 or a is None:
        break
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=a,
        max_tokens=1024,
        temperature=0.8,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    message = response.choices[0].text
    print(message)

print('结束')
