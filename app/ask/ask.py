from openai import OpenAI
from app.utils.model_config import ModelConfig


def ask_api(question:str, search_result:list, model_data:ModelConfig, is_rag = False) -> str:
    """
    调用llmapi返回查询结果
    param question: str 用户问题
    param search_result: list[
        {
           "subject": str,
            "predicate": str,
            "object": str
        } 
        ]
    知识图谱查询结果
    param model_data：ModelConfig模型配置
    param is_rag: bool 是否使用rag搜索知识图谱

    :return: str,bool
    """

    # 配置api网址与key
    client = OpenAI(
        api_key=model_data.api_key,
        base_url=model_data.base_url
    )

    # 构建提示
    prompt = "用户的问题和相关知识图谱中的实体与关系已提供，请基于这些信息回答。请确保答案简洁明确，不超过三句话，不要编造信息，仅根据提供的查询结果作答。\n"
    prompt += "这是用户发来的问题："+question+"\n"
    if len(search_result):
        prompt += "这是知识图谱中的实体与关系：\n"
        prompt += "".join(
            f"{result['subject']} {result['predicate']} {result['object']}" for result in search_result) + "\n"
    else:
        prompt += "知识图谱中未查询到相关实体与关系，请直接根据用户的问题与历史知识回答问题，不要编造信息。\n"

    try:
        response = client.chat.completions.create(
            model=model_data.model,
            messages=[
                {"role": "system", "content": "你是一个博物馆的智能助手，擅长用专业的历史知识回答问题"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=model_data.max_tokens,
            temperature=model_data.temperature,
        )
        output = response.choices[0].message.content.strip()

    except Exception as e:
        output = "抱歉，我无法处理您的请求。"
        return output,False

    return output,True
