import pickle


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.item_ids = set()

class EntityTrie:
    """
    构建前缀树，加快查询
    """
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, item_ids: list[str]):
        """
        插入一个实体及对应 itemIds
        """
        
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.item_ids.update(item_ids)

    def search(self, word: str) -> list[str]:
        """
        查找实体对应的 itemIds，找不到则返回空列表
        """
        
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.item_ids) if node.is_end else []

    def save_to_file(self, filepath: str):
        """
        将 Trie 树保存为 pickle 文件
        """
        
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filepath: str):
        """
        从 pickle 文件加载 Trie 树
        """
        
        with open(filepath, 'rb') as f:
            return pickle.load(f)




# if __name__ == "__main__":

#     def load_entity_itemid_map(csv_path: str) -> dict[str, list[str]]:
#         entity_map = {}
#         with open(csv_path, newline='', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 entity = row['title_zh'].strip()
#                 item_ids = [x.strip() for x in row['itemIds'].split(';')]
#                 entity_map[entity] = item_ids
#         return entity_map
    
#     data = load_entity_itemid_map(r"E:\DjangoProject\kgqa_project\question_answer\resources\title_zh2itemIds.csv")

#     # 构建 Trie
#     pkl_path = r"E:\DjangoProject\kgqa_project\question_answer\resources\entity_trie.pkl"
#     trie = EntityTrie()
#     for title, ids in data.items():
#         trie.insert(title, ids)

#     # 保存
#     trie.save_to_file(pkl_path)

#     # 加载
#     loaded_trie = EntityTrie.load_from_file(pkl_path)
#     print("加载后查'龟龙纹饰件':", trie.search("龟龙纹饰件"))
#     print("加载后查 '龙纹戈':", loaded_trie.search("龙纹戈"))
