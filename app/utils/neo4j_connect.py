from neo4j import GraphDatabase
from config.settings import NEO4J

# 全局 driver 对象（项目启动时初始化）


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, cypher) -> list:
        """
        执行查询并返回结果
        
        :param cypher: Cypher 查询语句
        :return: 查询结果列表
        """

        with self.driver.session() as session:
            result = session.run(cypher)
            return [record.data() for record in result]

# 初始化全局连接对象（只执行一次）
neo4j_connector = Neo4jConnection(
    uri=NEO4J['URI'],
    user=NEO4J['USER'],
    password=NEO4J['PASSWORD']
)
