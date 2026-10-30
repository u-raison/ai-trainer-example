import pandas as pd
import matplotlib.pyplot as plt

#设置字体，避免乱码
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


#创建字典类型数据
data = {
    '水果':['苹果','香蕉','樱桃','葡萄'],
    '数量':[10,15,7,10]
}

#将字典转换为二维表
df = pd.DataFrame(data)

#绘制饼图
plt.pie(df['数量'],labels=df['水果'],autopct='%1.1f%%')
plt.title('水果数量占比')
plt.show()