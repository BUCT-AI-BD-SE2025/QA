import uuid
from django.db import models
from django.db.models import JSONField

# Create your models here.

class ChatLog(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    question = models.TextField()
    answer = models.TextField()
    is_rag = models.BooleanField(default=False)
    model_data = JSONField()
    # 响应时间，单位s
    response_time = models.FloatField()
    # 记录时间
    log_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_log'
        ordering = ['-log_time']
        verbose_name = '聊天记录'
        verbose_name_plural = '聊天记录'
