import pandas as pd
import numpy as np

def clean_scores():
    data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
        '成绩': [85, np.nan, 90, 78, 88, 92],
        '学院': ['计算机', '艺术', '数学', '物理', np.nan, '艺术']
    }
    df = pd.DataFrame(data)                      # 字典转二维表

    # 统计每列缺失值个数
    print(df.isna().sum())

    # 计算成绩列的中位数
    median_score = df['成绩'].median()

    # 用中位数填充成绩缺失值
    df['成绩'] = df['成绩'].fillna(median_score)

    # 剔除艺术学院，保留学院为空的学生
    df_cleaned = df[(df['学院']!='艺术')| df['学院'].isna()]
    print(f"\n清洗后的数据为")
    print(df_cleaned)

    print(f"清洗后共{len(df_cleaned)}行")

    # 保存，不保留行索引
    df_cleaned.to_csv('cleaned.csv', index=False, encoding='utf-8')

    return df_cleaned

if __name__ == '__main__':
    result = clean_scores()
    print(result)