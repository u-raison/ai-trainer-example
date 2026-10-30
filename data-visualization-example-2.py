import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import inspect

plt.rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv("fruit.csv")

print(df)

def plot_bar_chart():
    
    print("=" * 60)
    print("数据：")
    print(df)
    print("\n方法1：df.plot()绘制")

    df.plot(
        kind='bar',
        x='水果',
        y='数量',
        title='水果数量分布',
        color='skyblue',
        legend=False
    )
    
    # plt.xlabel = '水果类型'
    # plt.ylabel = '数量'

    plt.xticks (rotation=0)
   
    plt.tight_layout()
   
    plt.savefig(fname='水果条形图.png',dpi=100,bbox_inches='tight')
    print("条形图已保存")
   
    #plt.show()

    print("=" * 60)
    print("\n 方法2 plt.bar()绘制")

    plt.bar(df['水果'],df['数量'],color='lightcoral',width=0.6)

    plt.title('水果数量分布图',fontsize=14)

    plt.xlabel('水果类型')
    plt.ylabel('数量')

    plt.grid(axis='y',alpha=0.3)

    plt.tight_layout()

    plt.show()

def plot_pie_chart():

    print("=" * 60)
    print("\n方法2：绘制饼图")

    data = {
    '水果': ['苹果', '香蕉', '樱桃', '葡萄'],
    '数量': [10, 15, 7, 10]
    }

    df = pd.DataFrame(data)

    print("数据：")
    print(df)

    print("\n绘制饼图")

    plt.figure(figsize=(8,8))

    plt.pie(
        df['数量'],
        labels = df['水果'],
        autopct = '%1.1f%%',
        startangle = 90,
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
        explode = [0.1,0,0,0]
    )

    plt.title('水果数量占比',fontsize=16)

    plt.axis('equal')

    plt.tight_layout()

    plt.savefig(fname='水果饼图.png',dpi = 100, bbox_inches = 'tight')

    print( "饼图已保存" )

    plt.show()

    #help(plt.savefig)
    # print([n for n in dir('plt') if ])
    #print(inspect.signature(plt.savefig(fname='1')))

def plot_line_chart():

    print("=" * 60)
    print("3. 折线图绘制")
    print("=" * 60)

    data = {

        '日期':['2025-01-01','2025-02-01','2025-03-01','2025-04-01'],
        '销售额':[200,220,210,280]
    }

    df = pd.DataFrame(data)

    df['日期'] = pd.to_datetime(df['日期'])

    print("数据:")
    print(df)

    print("\n方法1：df.plot()绘制")

    df.plot(
        kind='line',
        x='日期',
        y='销售额',
        title='月度销售额趋势',
        marker='o',
        color='green',
        legend=False
    )

    plt.xlabel ('日期')
    plt.ylabel ('销售额（元）')

    plt.grid(True,alpha=0.3)

    plt.tight_layout()

    plt.savefig(fname='折线图',dpi=100,bbox_inches='tight')

    print("折线图已保存")

    #plt.show()

    print("方法2： 使用plt.plot")

    plt.figure(figsize=(10,5))

    #help(plt.figure)

    plt.plot(
        df['日期'],
        df['销售额'],
        marker = 'o',
        markersize = 8,
        linestyle ='-', #线条类型
        linewidth = 2, #线条宽度
        color = 'blue',
        label = '销售额'  # 添加数据标签
        )

    for i,value in enumerate(df['销售额']):
        
        plt.text(
            df['日期'][i],
            value +5 ,
            str(value),
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.title('月销售额趋势',fontsize=14)

    plt.xlabel('日期')
    plt.ylabel('销售额（元）')

    plt.legend=False
    plt.grid(True,alpha=0.3)

    plt.xticks(rotation=15)
    #help(plt.xticks)
    
    plt.tight_layout()

    #plt.show()

    # lines = plt.title([1,2,3])
    # plt.setp(lines)

    #help(plt.plot)
    #print([n for n in dir('plt.plot') if not n.startswith('_')])
    

def comprehensive_example():

    print("=" * 60)
    print('4. 综合示例 - 多子图布局')
    print("=" * 60)

    data = {
    '科目': ['语文', '数学', '英语', '物理'],
    '成绩': [85, 92, 78, 88]
        }

    df = pd.DataFrame(data)

    fig,axes = plt.subplots(2,2,figsize=(12,10))

    fig.suptitle('学生成绩分析报告',fontsize=16,fontweight='bold')

    #help(fig.suptitle)
    #plt.setp( fig.suptitle('学生成绩分析报告',fontsize=16))

    #第一个条形图
    axes[0,0].bar(df['科目'],df['成绩'],color='blue')
    axes[0,0].set_title('各科成绩对比')
    axes[0,0].set_ylabel('成绩')
    axes[0,0].grid(axis='y',alpha=0.3)

    #第二个饼图
    axes[0,1].pie(df['成绩'],labels=df['科目'],autopct='%1.1f%%',startangle=90)
    axes[0,1].set_title('成绩占比')

    #第三个折线图
    axes[1,0].plot(df['科目'],df['成绩'],marker='o',linewidth=2,color='green')
    axes[1,0].set_title('成绩趋势')
    axes[1,0].set_ylabel('成绩')
    axes[1,0].grid(True,alpha=0.3)

    #第四个水平条形图
    axes[1,1].barh(df['科目'],df['成绩'],color='coral')
    axes[1,1].set_title('成绩排名')
    axes[1,1].set_xlabel('成绩')
    axes[1,1].grid(axis='x',alpha=0.3)

    plt.tight_layout()

    plt.savefig('成绩综合分析图.png',dpi =150, bbox_inches='tight')

    plt.show()


def main():

    print("数据可视化考点示例程序")
    print("=" * 60)

    plot_bar_chart()
    plot_pit_chart()
    plot_line_chart()

    #绘制综合图
    comprehensive_example()

    print("\n" + "="*60)
    print("所有图表绘制完成!")
    print("="*60) 

if __name__ == '__main__':
    main()





