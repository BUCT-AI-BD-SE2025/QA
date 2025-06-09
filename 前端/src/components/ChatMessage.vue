<template>
  <div :class="['chat-message', message.type]" style="animation: slide-in 0.3s ease-out;">
    <div class="avatar">
      <!-- ✅ 使用定义好的头像变量 -->
      <img :src="message.type === 'user' ? userAvatar : botAvatar" alt="Avatar" />
    </div>
    <div class="content">
      <!-- ✅ 添加空值检查 -->
      <div v-if="message.type === 'bot' && message.source" class="source">来源：{{ message.source }}</div>
      <div v-html="message.content"></div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

// ✅ 新增默认头像导入
import defaultBotAvatar from '@/assets/images/bot-avatar.png' // 需要创建这个图片文件
import defaultUserAvatar from '@/assets/images/user-avatar.png' // 需要创建这个图片文件

defineProps({
  message: {
    type: Object,
    required: true
  }
})

// ✅ 定义头像常量
const botAvatar = defaultBotAvatar
const userAvatar = defaultUserAvatar
</script>

<style scoped>
@keyframes slide-in {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.chat-message {
  display: flex;
  margin-bottom: 20px;
  align-items: start;
}
.chat-message.user .content {
  background-color: #d1ecf1;
  margin-left: auto;
}
.chat-message.bot .content {
  background-color: #f8f9fa;
  margin-right: auto;
}
.avatar {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}
.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.content {
  max-width: 70%;
  padding: 12px 15px;
  border-radius: 15px;
  font-size: 14px;
  line-height: 1.5;
}
.source {
  color: #888;
  font-size: 12px;
  margin-bottom: 5px;
}
</style>