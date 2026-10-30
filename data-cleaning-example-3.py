import pandas as pd
import numpy as np

#定义数据清洗函数
def data_cleaning_example():
    print("=" *70)
    print("数据清洗示例")

    data = {
        '姓名': ['张三','李四','王五','赵六','钱七','孙八'],
        '成绩': [85, np.nan, 90, 78, 88, 92], # 修复：多余的逗号和括号
        '学院': ['计算机','艺术','数学','物理', np.nan,'艺术']
    }

    df = pd.DataFrame(data)

    #拷贝一份原始数据存在变量df_original中
    df_original = df.copy()

    print("\n原始数据")
    print(df)
    print(f"\n原始数据一共有{len(df)}行")

    print("\n【缺失值检查】")
    print(f"{df.isna().sum()}")

    #获得成绩的中位数,使用中位数替换成绩的缺失值
    median_score = df['成绩'].median()
    print(f"\n成绩的中位数是{median_score}")
    df['成绩'] = df['成绩'].fillna(median_score)
    print("\n 【填充成绩缺失值后】")
    print(df)

    print("\n" + "=" *70)
    print("关键考点：NaN布尔索引陷阱")
    print("=" *70)

    #使用dropna删除学院列为空的行
    df_cleaned = df.dropna(subset=['学院'])

    print("\n 【清洗后数据验证】")
    print(f"艺术学院学生数量：{len(df_cleaned[df_cleaned['学院']=='艺术'])}条")
    print(f"学院为空的学生已剔除 {len(df_original[df_original['学院'].isna()])}条")
    print(f"成绩列有缺失值：{len(df_cleaned[df_cleaned['成绩'].isna()])}条")

    #结束函数同时返回原数据，清洗后的数据
    return df_original,df_cleaned 

#定义生产清洗报告的函数，参数分别为：原始数据、清洗后的数据
def generate_cleaning_report(df_original,df_cleaned):
    report = f"""
    【数据清洗报告】

    1.原始数据行：{len(df_original)}
    2.清洗后的数据行：{len(df_cleaned)}
    3.缺失值填充：成绩列填充中位数{df_cleaned['成绩'].median()}
    4.学院为空的行：{len(df_original[df_original['学院'].isna()])}条
"""

    print("=" *70)
    print("数据清洗规范审核报告")
    print("=" *70)

    #输出报告信息
    print(report)
    return report

def main():

    #调用数据清洗函数，并将函数的返回结果存入两个变量
    df_original,df_cleaned = data_cleaning_example()

    #调用报告生成函数，并将返回结果存入report
    report = generate_cleaning_report(df_original,df_cleaned)

    #将清洗后的数据存在CSV文件中
    df_cleaned.to_csv('cleaned_data3.csv',index=False,encoding='utf-8')

    print("\n 清洗后数据已保存至：cleaned_data3.csv")


#python程序入口

if __name__=='__main__':
    main()
