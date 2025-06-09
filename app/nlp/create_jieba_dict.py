import pandas as pd
from natsort import natsorted
import re


if __name__ == "__main__":
    # 读取 CSV
    df = pd.read_csv(r'E:\DjangoProject\kgqa_project\question_answer\resources\title_zh2itemIds.csv')

    # 合并 itemIds，并自然排序
    def merge_and_sort(items):
        item_list = []
        for item in items:
            if pd.notna(item):
                item_list.extend([x.strip() for x in str(item).split(';') if x.strip()])
        return ';'.join(natsorted(set(item_list)))

    # 按 title_zh 分组并合并 itemIds
    df = df.groupby('title_zh', as_index=False)['itemIds'].apply(merge_and_sort)
    df = df.sort_values(by='title_zh').reset_index(drop=True)

    # 中文/英文标点符号（用于分割）
    punctuation_pattern = r'[-.,：；“”‘’《》【】/\\\[\]\s]'

    # 构建用户词典集合（去重）
    user_dict = set()

    for title in df['title_zh'].dropna().unique():
        if re.search(punctuation_pattern, title):
            # 含标点 → 按标点分割
            parts = [part.strip() for part in re.split(punctuation_pattern, title) if part.strip()]
            for part in parts:
                freq = 10000 + len(part) * 10
                user_dict.add(f"{part} {freq} nz")
        else:
            # 不含标点 → 保留整体
            freq = 10000 + len(title) * 10
            user_dict.add(f"{title} {freq} nz")

    # 保存为 jieba 用户词典
    with open(r'app\nlp\resources\custom_dict.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(user_dict)))
