# 问题解析器（意图识别、实体抽取）
import re
import json
import jieba
import jieba.posseg as pseg

jieba.load_userdict(r"app\nlp\resources\jieba_dict.txt")
intent_keywords_path = r"app\nlp\resources\intent_keywords.json"


class QuestionParser:
    """
    解析用户输入的问题
    """

    def __init__(self):
        with open(intent_keywords_path, "r", encoding="utf-8") as f:
            self.relation_keywords = json.load(f)

    def preprocesse_question(self, question: str) -> str:
        """
        清洗问题
        """

        # 去除的其他字符（中文、部分标点符号除外）
        question = re.sub(
            r'[^\u4e00-\u9fa5，。？、：！“”‘’《》,.?!;/\-]', '', question)

        # 检查是否为空
        if not question:
            raise ValueError("清洗后的问题为空")

        # 检查长度
        min_length = 2
        max_length = 100
        question_length = len(question)
        if question_length < min_length:
            raise ValueError("清洗后的问题长度小于最小值")
        elif question_length > max_length:
            raise ValueError("清洗后的问题长度大于最大值")

        # 检查是否包含中文字符
        if not re.search(r'[\u4e00-\u9fff]', question):
            raise ValueError("清洗后的问题未包含中文字符")

        return question

    def parse(self, question: str = "") -> dict:
        """
        解析问题，返回结构化信息。

        :return list[dict] :
        返回实体+关系的字典列表，例如：\n
        [
            { 'entity': '龟龙纹饰件',\n
            'relaton': '创作者' },\n
            { 'entity': '龟龙纹饰件',\n
            'relaton': '制作地点' }
        ]
        """

        question = self.preprocesse_question(question)
        cut_result = self.cut_question(question)
        entities = [word for word, flag in cut_result if flag == 'nz']
        relations = self.get_relations(cut_result)

        # print("实体: " + ", ".join(entities))
        # print("关系: " + ", ".join(relations))

        return {'entities': entities, 'relations': relations}

    def cut_question(self, question: str) -> list[dict]:
        """
        切分问题
        """

        pairs_list = pseg.lcut(question)
        # print("初步分解的词项:", pairs_list)

        # 保留指定词性
        allowed_flags = ('nz', 'nx', 'x')
        filtered = [(w, f) for w, f in pairs_list if f in allowed_flags]

        # 特殊符号处理
        result = []
        i = 0
        while i < len(filtered):
            word, flag = filtered[i]

            # 《 与后一个词连接
            if word == '《' and i + 1 < len(filtered):
                next_word, next_flag = filtered[i + 1]
                result.append((word + next_word, next_flag))
                i += 2
                continue

            # 》 与前一个词连接
            elif word == '》' and result:
                prev_word, prev_flag = result.pop()
                result.append((prev_word + word, prev_flag))
                i += 1
                continue

            # ：. 与前后词连接
            elif word in ('：', '.', '-', '/') and result and i + 1 < len(filtered):
                prev_word, prev_flag = result.pop()
                next_word, next_flag = filtered[i + 1]
                result.append((prev_word + word + next_word, prev_flag))
                i += 2
                continue

            # nx、nz才词性加入
            elif flag != 'x':
                result.append((word, flag))
                i += 1
                continue

            else:
                i += 1

        return result

    def get_relations(self, cut_result: list) -> list:
        """
        从分词结果匹配标准关系名
        """

        intent_list = [word for word, flag in cut_result if flag == 'nx']

        relations = set()
        for relation, keywords in self.relation_keywords.items():
            for kw in keywords:
                if kw in intent_list:
                    relations.add(relation)
        return list(relations)


# 示例使用
# if __name__ == "__main__":

#     parser = QuestionParser()

#     questions = [
#         "仿赵孟頫山水与《东京二十景》-大根河岸晨景的作者是谁，出土地在哪里，创作时间在什么时候？",
#         "松浦佐世媛饰演大伴狭手彦之妻是哪个年代的？",
#         "《二道士.男女与狮》和伊斯兰托盘是用什么做的？",
#         "龟龙纹饰件出土地在哪以及作者是谁？"
#     ]

#     for q in questions:
#         print(f"Q: {q}")
#         print("Parsed:", parser.parse(q))
#         print()
