import pandas as pd
import openpyxl

def clean_sales():
    # 读取 GBK 编码的 CSV
    df = pd.read_csv('sales.csv', encoding='utf-8')

    # 查看每列的数据类型
    print(df.dtypes)

    # 检查缺失值总数（每列）
    print(df.isna().sum())

    # 用平均值填充销量缺失值
    df['销量'] = df['销量'].fillna(df['销量'].mean())

    # 剔除"退货"和"赠品"两类订单（两个条件同时成立才留下）
    df = df[(df['类型'] != '退货') & (df['类型'] != '赠品')]

    # 只在"客户"列为空时删除该行
    df = df.dropna(subset=['客户'])

    # 另一种写法：用 query 筛选销量大于 0 的行
    df = df.query("销量 > 0")

    # 保存为 xlsx，不保留行索引
    df.to_excel('cleaned_sales.xlsx', sheet_name='结果',
               engine='openpyxl', index=False)

    print(f"保存完成，共{len(df)}行")
    return df

if __name__ == '__main__':
    clean_sales()