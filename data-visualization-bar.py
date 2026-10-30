import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
#plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


#创建字典类型数据
data = {
    '水果':['苹果','香蕉','樱桃','葡萄'],
    '数量':[10,15,7,10]
}

# 将字典数据转为二维表
df = pd.DataFrame(data)

#df.plot方法可视化，设置图类型为条形图bar，X轴显示水果数据，Y轴显示数量数据，title表示徒刑标题
df.plot(kind='bar',x='水果',y='数量',title='水果数量分布')
#显示图表
plt.show()