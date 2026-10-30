#导入aiml，处理知识库
import aiml
# #导入python自带os模块，处理文件或文件夹
import os

# 定义创建知识库的函数
def create_kernel():

    # 创建内核,并装进知识:有脑文件就直接加载,没有就读 AIML 并保存脑文件
    # kernel(内核)是机器人的"大脑引擎",是 aiml.Kernel() 创建出来的对象。它负责: 保存所有学到的问答规则(pattern 和 template)
    # 收到用户输入后,去规则里找匹配的 pattern; 找到后,按 template 生成回答; 记住会话信息(比如用户的名字)
    kernel = aiml.Kernel()

    # 判断是否存在脑文件
    if os.path.exists('bot_brain.brn'):
        
        # 如果存在则直接加载脑文件brainFile; kernel.bootstrap(brainFile=...) 从脑文件恢复,不解析amil文件
        kernel.bootstrap(brainFile = 'bot_brain.brn')
    
    else:

        # 加载知识库learnFiles，启动时向机器人说：LOAD AIML BRAIN
        kernel.bootstrap(learnFiles ='hospital.aiml',commands ='LOAD AIML BRAIN')

        # kernel.saveBrain() 把学到的内容存成脑文件
        kernel.saveBrain('bot_brain.brn')

    return kernel


def main():

    # 调用创建内核函数
    kernel = create_kernel()

    print("医院智能客服已启动！输入 '退出' 结束对话。")

    while True:

        # 接收用户输入的字符串，使用strip()方法去除空格
        user_input = input("你：").strip()

        # 判断输入是不是退出指令
        if user_input in ['退出',"quit","exit"]:

            print("再见！")

            break
        
        # kernel.respond(用户输入) 匹配规则,返回回答。没匹配到时返回空字符串
        response = kernel.respond(user_input)

        print("客服：",response)


if __name__ == "__main__":

    main()