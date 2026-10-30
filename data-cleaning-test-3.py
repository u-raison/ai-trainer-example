import pandas as pd
from datetime import datetime
import os

def clean_employees(file_path):
    """员工绩效表清洗"""

    # 读取 CSV
    df = pd.read_csv(file_path, encoding='utf-8')

    # 拷贝一份原始数据，用于后面对比
    df_original = df.copy()

    # 统计每列缺失值个数
    print(df.isna().sum())

    # 绩效分的中位数
    median_score = df['绩效分'].median()

    # 用中位数填充绩效分缺失值
    df['绩效分'] = df['绩效分'].fillna(median_score)

    # 剔除外包部门，保留部门为空的员工
    df_cleaned = df[(df['部门']!= '外包')| df['部门'].isna()]

    return df_original, df_cleaned


def make_report(df_original, df_cleaned):
    """生成清洗报告"""

    # 部门为空的员工姓名，多人用顿号连接，没有则为"无"
    na_names = "、".join(df_cleaned[df_cleaned['部门'].isna()]['姓名']) or '无'

    report = f"""
【员工数据清洗报告】
1. 数据源路径：{os.path.join(os.getcwd(), 'employees.csv')}
2. 原始数据：{len(df_original)}行
3. 清洗后数据：{len(df_cleaned)}行
4. 绩效分填充值（中位数）：{df_cleaned['绩效分'].median()}
5. 部门为空的员工：{na_names}
6. 绩效分范围：[{df_cleaned['绩效分'].min()}, {df_cleaned['绩效分'].max()}]
7. 报告日期：{datetime.now().strftime("%Y年%m月%d日")}
"""
    print(report)
    return report


def main():
    df_original, df_cleaned = clean_employees('employees.csv')
    make_report(df_original, df_cleaned)

    # 保存结果，不保留行索引
    df_cleaned.to_csv('cleaned_employees.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    main()