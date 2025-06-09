import json
from time import time
from django.http import JsonResponse
from app.ask.ask import ask_api
from django.views.decorators.csrf import csrf_exempt
from app.nlp.query_info import query_result
from app.utils.model_config import model_config1
from app.utils.chat_log_utils import log_chatlog


# 视图函数
@csrf_exempt
def answer(request):

   
    if request.method == 'POST':
        try:
            start_time = time()
            data = json.loads(request.body)
            
            question = data.get('content')
            if not question:
                return JsonResponse({'message': 'error', 'content':'问题不能为空'}, status=400)
            # 调用 Neo4j 查询
            search_reslut = query_result(question)
            #从settings.py中获取模型配置
            model_data = model_config1
            #调用api润色查询结果
            output,status = ask_api(question, search_reslut,model_data)
            end_time = time()
            # 可选：保存入 PostgreSQL（如启用了）
            log_chatlog(data.get('userId'), status, question, output, model_data.bulid_model_data(), end_time - start_time, data.get("dateTime"),is_rag=False)
            
            return JsonResponse({
                'message':'success',
                'data': {
                    'source': '系统',
                    'content': output
                },
                }, 
                status=200)

        except Exception as e:
            return JsonResponse({'message': 'error','content': str(e)}, status=500)

    return JsonResponse({'message': 'error', 'content':'请求类型错误'}, status = 405)


