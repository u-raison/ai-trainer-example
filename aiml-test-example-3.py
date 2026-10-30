import aiml

# 创建聊天机器人对象
alice = aiml.Kernel()

# 让机器人学习知识库
alice.learn('ai-service-test.aiml')

# alice : 机器人的名字
# 考试内容:将特定问答写入知识库

# 无限循环
while True:
    # 人机交互
    print(alice.respond(input('Alice请您提问...>>')))