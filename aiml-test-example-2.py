import aiml
import os

def create_aiml_file():

    """
    创建AIML知识库文件
    考点: AIML的XML格式和基本语法
    """

    # 定义变量存多行文本内容,这个内容是AIML文件(考试标准格式)

    aiml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <aiml version="1.0">
    <!--医院导诊问答-->

    <category>
    <pattern>口腔科在哪里</pattern>
    <template>北区三楼</template>
    </category>

    <category>
    <pattern>急诊科在哪里</pattern>
    <template>南区一楼</template>
    </category>

    <category>
    <pattern>挂号处怎么走</pattern>
    <template>门诊大厅东侧</template>
    </category>

    <category>
    <pattern>药房在哪里</pattern>
    <template>西区二楼</template>
    </category>

    <category>
    <pattern>放射科在哪</pattern>
    <template>东区地下一层</template>
    </category>

    <category>
    <pattern>儿科在哪里</pattern>
    <template>北区二楼</template>
    </category>

    <!--问候语-->
    <category>
    <pattern>您好</pattern>
    <template>您好!我是医院智能导诊客服,请问需要咨询哪个科室的位置?</template>
    </category>

    <!-- 默认回复(通配符*) -->
    <category>
    <pattern>*</pattern>
    <template>抱歉,我不太明白您的问题。请问您想了解哪个科室的位置?我可以告诉您: 口腔科、急诊科、挂号处、药房、放射科、儿科等位置信息</template>
    </category>
    
    </aiml>
    """

    # 打开hospital-2.aiml文件
    with open("hospital-2.aiml", 'w', encoding= 'UTF-8') as f:
        
        # 写入问答内容
        f.write(aiml_content)

    print("AIML知识库文件已创建: hospital-2.aiml")


def create_kernel():

    """
    创建并初始化AIML内核
    考点:
    1. Kernel()的使用
    2. bootstrap()加载AIML文件
    3. 脑文件(.brn)缓存机制
    """

    # 输出提示
    print("\n" + "="*70)
    print("初始化AIML智能客服系统")
    print("="*70)

    # 创建AIML内核
    kernel = aiml.Kernel()
    
    # 检查是否有编译缓存(考点: 加快启动速度)
    # 定义一个变量,存脑文件名
    brain_file = "bot_brain-2.brn"

    # 判断脑文件是否存在
    if os.path.exists(brain_file):
        print(f"检测到缓存文件: {brain_file}")
        print("正在加载缓存...")
        
        #加载文件,brainFile表示加载是脑文件
        kernel.bootstrap(brainFile = brain_file)
        print("缓存加载完成(快速启动)")
    
    else:
        
        print("首次运行,正在加载AIML知识库...")

        # 判断AIML文件是否存在
        if not os.path.exists("hospital-2.aiml"):
        
        #如果aiml文件不存在,调用前面的函数创建hospital.aiml文件
            create_aiml_file()

        # 加载文件,learnFile表示加载的是aiml文件,commands加载aiml命令
        kernel.bootstrap(learnFiles='hospital-2.aiml',commands="LOAD AIML BRAIN")

        # 保存为脑文件(考点: 提高下次启动速度)    
        kernel.saveBrain(brain_file)
        print(f"知识库加载完成,已保存缓存: {brain_file}")
        print("="*70)
    
    #返回aiml内核对象
    return kernel

def chat_interface(kernel):

    """
    交互式聊天界面
    考点: kernel.respond()的使用
    """

    #输出提示
    print("\n医院智能导诊客服已启动!")
    print("="*70)
    print("提示:")
    print(" - 您可以询问科室位置,如: '口腔科在哪里'")
    print(" - 输入 '退出'、'quit' 或 'exit' 结束对话")
    print("="*70)

    # 循环
    while True:
        # 获取用户输入并存在变量
        user_input = input("\n 你：").strip()
        # 检查用户输入的是否是退出命令
        if user_input.lower() in ['退出','quit','exit','q']:
            print("\n客服: 感谢使用医院智能导诊服务,祝您身体健康!")
            break
    
    # 判断输入的内容是否为空
        if not user_input:
            #结束这次循环,执行下一次
            continue
        
        # 获取AI回复(考点: respond()方法)
        response = kernel.respond(user_input)
        # 输出回复
        print(f"\n客服:{response}",)

#定义批量测试问答的函数,kernel参数是aiml内核对象
def demo_batch_queries(kernel):
    """
    批量测试问答
    考点: 验证AIML规则是否正确
    """

    #输出提示
    print("\n" + "="*70)
    print("批量测试模式")
    print("="*70)

    test_case = [
    "您好",
    "口腔科在哪里",
    "急诊科在哪里",
    "挂号处怎么走",
    "药房在哪里",
    "放射科在哪",
    "儿科在哪里",
    "不知道说什么"
    ]

    # 循环遍历测试用例(用户的问题)

    for query in test_case:
        
        # 将问题传入到kernel.responde，kernel.responde根据问题查询并返回回答内容
        response = kernel.respond(query)
        print(f"\n 问的是：{query}")
        print(f"\n 回答的是：{response}")
        print("\n" + "="*70)

def main():

    """主函数"""

    print("="*70)
    print("智能客服系统 - AIML实现")
    print("="*70)

    # 步骤1: 创建AIML文件(如果不存在)
    # 判断hospital.aiml文件是否存
    if not os.path.exists("hospital-2.aiml"):
        #调用创建hospital.aiml文件的函数
        create_aiml_file()

    # 步骤2: 初始化AIML内核
    # 调用获得知识库脑文件对象函数
    kernel = create_kernel()

    # 步骤3：旋转运行模式
    print("\n请选择运行模式:")
    print("1. 交互式对话")
    print("2. 批量测试")

    choise = input("\n请输入选项 (1/2, 默认1): ").strip()
    if choise == '2':

        demo_batch_queries(kernel)
    else:
        chat_interface(kernel)

    print("\n" + "="*70)
    print("程序结束")
    print("="*70)


if __name__ == "__main__":
    main()