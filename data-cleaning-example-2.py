import pandas as pd
import numpy as np

#原始数据
data = {
'姓名': ['张三','李四','王五','赵六','钱七','孙八'],
'成绩': [85, np.nan,90, 78, 88, 92],
'学院': ['计算机','艺术','数学','物理',np.nan,'艺术']
}

#将字典转换为二维表
df = pd.DataFrame(data)
print("原始数据为")
print(df)
print("\n" + '=' * 70)

#获取成绩的中位数
median_score = df['成绩'].median()

#filna()填充成绩列为空的后再赋值给成绩列
df['成绩'] = df['成绩'].fillna(median_score)
#print(df)

#剔除艺术学院，同时保留学院为空的学生的数据并存在新变量中;不能简单用dropna(subset=['学院'])删除空学院，而是要保留这些记录
#df_cleaned=df.dropna(subset=['学院'])
df_cleaned = df[(df['学院'] !='艺术')| df['学院'].isna()]

print("\n清洗后数据如下：")
print(df_cleaned)

df_cleaned.to_csv('cleaned_data2.csv',index=False,encoding='utf8')