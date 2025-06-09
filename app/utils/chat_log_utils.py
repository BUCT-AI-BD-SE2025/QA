from app.models import ChatLog


def log_chatlog(user_id, status, question, answer, model_data, response_time, log_time, is_rag=False):
    """
    用于将聊天记录存入数据库
    :return: boolean
    """
    log = ChatLog.objects.create(
        user_id=user_id,
        status=status,
        question=question,
        answer=answer,
        model_data=model_data,
        response_time=response_time,
        log_time=log_time,
        is_rag=is_rag

    )
