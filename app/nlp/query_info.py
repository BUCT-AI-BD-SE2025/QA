# 数据库查询

from app.nlp.entity_trie import EntityTrie, TrieNode
from app.nlp.question_parser import QuestionParser
from app.utils.neo4j_connect import neo4j_connector

# 载入已保存的 Trie
trie_pkl_path = r"app\nlp\resources\entity_trie.pkl"
trie = EntityTrie.load_from_file(trie_pkl_path)
parser = QuestionParser()
connector = neo4j_connector

def get_to_label(relation: str) -> str:
    """
    获取要查询的节点标签
    """
    
    relation_to_node_label= {
    "材质": "material",
    "类别": "category",
    "文化": "culture",
    "制作地点": "place",
    "对象类型": "type",
    "捐赠来源": "donor",
    "材料术语": "glossary",
    "尺寸": "measurement",
    "制作时间": "date",
    "时期": "period",
    "创作者": "artist",
    "描述": "description",
    "题跋": "inscription",
    "博物馆": "museum",
    "图片": "images"
    }
    
    return relation_to_node_label.get(relation, "")

def build_cypher(itemId_list: list[str], relation: str) -> list[str]:
    """
    对多个itemId构建同一关系cypher查询语句  
    """
    
    to_label = get_to_label(relation)
    itemIds_str = ",".join(f"'{itemId}'" for itemId in itemId_list)
    cypher = f"MATCH (e:item)-[r:`{relation}`]->(o:{to_label}) " \
            f"WHERE e.itemId IN [{itemIds_str}] " \
            f"RETURN e.itemId AS subject, o.value AS object"
    return cypher

def query_result(question: str) -> list[dict]:
    """
    查询实体信息
    """
    
    result_info = []
    
    parser_result = parser.parse(question)
    entities = parser_result['entities']
    relations = parser_result['relations']
    
    if not entities:
        print("未匹配到实体")
        return []
    
    if not relations:
        print("未匹配到关系")
        return []
    
    itemId2entity = {}
    for entity in entities:
        itemIds = trie.search(entity)
        
        if not itemIds:
            print("未找到实体id: " + entity)
            continue
        
        itemId = itemIds[0] # 只取了一个itemId
        itemId2entity[itemId] = entity
        
    if not itemId2entity:
        print("未找到任何一个实体")
        return []
        
    # 记录哪些实体-关系组合查到了结果
    found_pairs = set()

    itemId_list = list(itemId2entity.keys())
    for relation in relations:
        cypher = build_cypher(itemId_list, relation)
        query_results = connector.query(cypher)
        
        if query_results:
            for qr in query_results:
                itemId = qr['subject']
                found_pairs.add((itemId, relation))
                qr['subject'] = itemId2entity[itemId]
                qr['predicate'] = relation
                result_info.append(qr)

        # 检查哪些组合没有查到
        for itemId in itemId_list:
            if (itemId, relation) not in found_pairs:
                print(f"未查到[ {itemId2entity[itemId]} ]的[ {relation} ]")
    print(result_info)
    return result_info
    

                
                
            
    

# 示例
# if __name__ == "__main__":
#     questions = [
#         "松浦佐世媛饰演大伴狭手彦之妻是哪个年代的？",
#         "《二道士.男女与狮》和伊斯兰托盘是用什么做的？",
#         "龙纹戈出土地在哪以及作者是谁？",
#         "仿赵孟頫山水与《东京二十景》-大根河岸晨景的作者是谁，出土地在哪里，创作时间在什么时候？",
#     ]
    
#     for q in questions:
#         query_info(q)
#         print()
