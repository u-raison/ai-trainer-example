import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

#创建字典类型数据
data = {
    '日期': ['2025-01-01','2025-02-01','2025-03-01','2025-04-01'],
    '销售额': [200, 220, 240, 260]
    }

#数据转为二维表
df = pd.DataFrame(data)

#将日期转为datetime日期类型
df['日期'] = pd.to_datetime(df['日期'])

#绘制折线图，将日期这列作为X轴，将销售额作为Y轴
plt.plot(df['日期'],df['销售额'])

#设置折线图标题
plt.title('月度销售额趋势')

#设置折线图的X轴标签
plt.xlabel('日期')

#设置折线图Y轴标签
plt.ylabel('销售额')

#显示图形
plt.show()
