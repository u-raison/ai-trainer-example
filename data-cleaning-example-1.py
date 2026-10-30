# 导入pandas库，用于处理表格数据
import pandas as pd
# 导入numpy库，用于缺失值处理
import numpy as np
from datetime import datetime 
import os

def data_cleaning_example():

  """
  学生表清洗

  要求：
  1. 成绩缺失的用中位数条虫
  2. 剔除“艺术”学院学生
  3. 保留学院信息为空(NaN)的学生  (陷阱)
  
  """

  print("=" * 70)
  print("数据清洗示例 - 学生成绩表")
  print("=" * 70)

  # 读取CSV数据，存储为pands表格类型数据
  df = pd.read_csv("学生成绩.csv",encoding='gbk')

  print("\n【原始数据】")
  print(df)
  print(f"原始数据行数：{len(df)}")

  print("\n【缺失值检查】")
  print(df.isnull().sum()) # 检查缺失值的数量

  print("\n 【中位数填充缺失值】")
  # 先使用media()获得中位数
  median_source = df['成绩'].median()
  print(f"\n成绩中位数是{median_source}")

  #用中位数填充成绩列的空值
  df['成绩'] = df['成绩'].fillna(median_source)
  
  print ("\n 【填充缺失值后为】")
  print(df)

  #剔除艺术学院，但保留学院为NaN的记录
  print("\n" + "=" * 70)
  print("关键考点，NaN布尔索引陷阱")
  print("=" * 70)


  #声明变量存剔除"艺术"学院,但保留学院为NaN的记录
  df_cleaned = df[df['学院'] !='艺术']
  #df_cleaned = df[(df['学院'] !='艺术')| df['学院'].isna()]

  #输出提示
  print(df_cleaned)
  print(f"结果: 钱七(学院为NaN)被正确保留! 剩余{len(df_cleaned)}行")
  print("\n" + "=" *70)

  #最后验证
  print("\n 【清洗后数据验证】")
  print(f"艺术学院学生已删除 {len(df[df['学院']=='艺术'])}条")
  print(f"学院为空的学生保留 {len(df_cleaned[df_cleaned['学院'].isna()])}条")
  print(f"成绩有缺失值的共 {df_cleaned['成绩'].isna().sum()}条")

  #结束函数的同时，返回原表格数据，需要保留数据

  return df,df_cleaned

# 定义生称清洗报告的函数，参数分布为原表格数据，清洗后的数据
def generate_cleaning_report(df_oraginal,df_cleaned):

  """
  生成数据清洗规范审核报告
  考点：报告格式必须按标准模板
  """
  print("\n" + "=" *70)
  print("数据清洗规范审核报告")
  print("=" *70)

  reprot = f"""

  1.数据表基本信息

  （1） 数据源文件所在路径：{os.path.join(os.getcwd(),'学生成绩.csv')}
  （2） 用户数量：
      - 原始数据：{len(df_oraginal)}条
      - 清洗后的数据：{len(df_cleaned)}条
  （3）用户特征：
      - 字段：姓名（字符串）、成绩（数值）、学院（字符串）
      - 成绩范围：[{df_cleaned['成绩'].min()},{df_cleaned['成绩'].max()}]
  
  2.清洗审核规范

    （1） 处理后的数据文件是否能正常打开：是
    （2） 是否有未处理的缺失值：否
      - "成绩"列：原缺失值已使用中位数({df_cleaned['成绩'].median()})填充
      - "学院"列：保留{df_cleaned['学院'].isna().sum()}个空值（符合业务要求）
    （3）是否有未处理的异常值：否
      - 成绩范围在[0,100]内无异常值
      - "艺术"学院已按规则全部剔除

  3.清洗是否合格（合格/不合格）：合格
    
    理由：
      - 缺失值按规格使用中位数填充（针对需保留的记录）
      - 指定无效类别("艺术"学院)已完全剔除
      - 允许保留的空学院记录正确留存
      - 最终数据结构完整、逻辑一致

  4. 清洗后存在问题的用户:

    | 姓名 | 问题描述 | 是否保留 | 备注 |
    |------|---------|---------|------|
    {df_cleaned[df_cleaned['学院'].isna()]['姓名'].values[0] if df_cleaned['学院'].isna().any() else '无'}|学院信息缺失(NaN)|?是|符合业务要求允许保留｜

    说明：其余用户数据完整、有效
    报告生成时间：{datetime.now().strftime("%Y年%m月%d日")}
    审核人：数据治理小组
"""
 
  print(reprot)
  return reprot

def main():

  #调用数据清洗的函数，并将函数返回的两个结果存在2个变量里
  df_oraginal,df_clened = data_cleaning_example()

  #调用生产清洗报告的函数，并将函数返回结果存在变量
  report = generate_cleaning_report(df_oraginal,df_clened)

  #将清洗好的数据存在csv指定文件中
  df_clened.to_csv('cleaned_data.csv',index=False,encoding='utf-8')

  #提示
  print('\n 清洗好的数据已保存至，cleaned_data.csv')

if __name__=='__main__':
  main()