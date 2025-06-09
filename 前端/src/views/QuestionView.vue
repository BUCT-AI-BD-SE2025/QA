<script setup>
import HeaderBar from '@/components/HeaderBar.vue'
import ChatMessage from '@/components/ChatMessage.vue'
import { ref, computed } from 'vue'
import { ArrowDown, ArrowUp, ArrowRightBold } from '@element-plus/icons-vue'
import questionApi from '@/api/question'  // 新增真实API导入

// 数据定义
const chatSessions = ref([{
  id: Date.now(),
  title: '新对话',
  timestamp: Date.now(),
  messages: []
}])
const currentSessionId = ref(chatSessions.value[0].id)
const isCollapsed = ref(false)
const inputQuestion = ref('')
const isLoading = ref(false)

// 创建新会话
const createNewSession = () => {
  const newSession = {
    id: Date.now(),
    title: `对话 ${chatSessions.value.length + 1}`,
    timestamp: Date.now(),
    messages: []
  }
  chatSessions.value.unshift(newSession)
  currentSessionId.value = newSession.id
}

// 当前会话的消息列表
const currentMessages = computed(() => {
  const session = chatSessions.value.find(s => s.id === currentSessionId.value)
  return session?.messages || []
})

// 处理发送消息
const handleSearch = async () => {
  const question = inputQuestion.value.trim()
  if (!question) return
  
  const userMsg = {
    type: 'user',
    content: question,
    timestamp: new Date()
  }
  
  const session = chatSessions.value.find(s => s.id === currentSessionId.value)
  session.messages.push(userMsg)
  inputQuestion.value = ''
  isLoading.value = true
  
  try {
    // 发送真实请求
    const response = await questionApi.askLLMQuestion({
      userId: 123456, // 从store获取真实用户ID
      content: question,
      dateTime: new Date().toISOString()
    })
    
    // 添加机器人回复
    const botMsg = {
      type: 'bot',
      content: response.data.data.content,
      source: response.data.data.source || '系统',
      timestamp: new Date()
    }
    session.messages.push(botMsg)
  } catch (error) {
    // 错误处理
    console.error('请求失败:', error)
    session.messages.push({
      type: 'bot',
      content: '抱歉，系统暂时无法回答您的问题，请稍后再试',
      error: true
    })
  } finally {
    isLoading.value = false
  }
}

// 文件上传处理
const handleUploadClick = () => {
  alert('文件上传功能暂未实现')
}
</script>

<template>
  <div class="main-layout">
    <!-- 左侧历史记录侧边栏 -->
    <div class="sidebar-container" :class="{ 'expanded': !isCollapsed }">
      <!-- 侧边栏触发按钮 -->
      <div 
        class="sidebar-trigger"
        :class="{ 'collapsed': isCollapsed }"
        @click="isCollapsed = !isCollapsed"
      >
        <el-icon :size="20">
          <component :is="isCollapsed ? ArrowDown : ArrowUp" />
        </el-icon>
      </div>
      <!-- 侧边栏主体 -->
      <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
        <div class="sidebar-header">
          <h3>历史记录</h3>
          <el-button 
            type="text" 
            @click="createNewSession"
            class="new-chat-btn"
          >
            + 新对话
          </el-button>
        </div>
        <div class="history-list">
          <el-scrollbar>
            <div 
              v-for="(session, index) in chatSessions" 
              :key="session.id" 
              class="session-item"
              :class="{ active: session.id === currentSessionId }"
              @click="currentSessionId = session.id"
            >
              <div class="session-header">
                <span>{{ session.title }}</span>
              </div>
              <div class="messages-preview">
                {{ session.messages.slice(-1)[0]?.content || '无记录' }}
              </div>
            </div>
          </el-scrollbar>
        </div>
      </div>
    </div>
    <!-- 主聊天区域 -->
    <div class="chat-container" :class="{ 'full-width': isCollapsed }">
      <!-- 新增的展开按钮 -->
      <div v-if="isCollapsed" class="expand-trigger" @click="isCollapsed = !isCollapsed">
        <el-icon :size="20">
          <ArrowRightBold />
        </el-icon>
      </div>
      <header-bar />
      <!-- 欢迎语 -->
      <div v-if="!currentMessages.length" class="welcome-message">
        <h2>您好，我是文物知识助手</h2>
        <p>支持以下功能：</p>
        <ul>
          <li>• 文物属性查询（收藏地、材质、时代等）</li>
        </ul>
      </div>
      <!-- 聊天历史 -->
      <div class="message-list">
        <el-scrollbar ref="scrollbar">
          <div 
            v-for="(msg, index) in currentMessages"
            :key="index"
            class="message-item"
          >
            <chat-message :message="msg" />
          </div>
        </el-scrollbar>
      </div>
      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-wrapper">
          <el-input
            v-model="inputQuestion"
            placeholder="请输入您的问题"
            class="question-input"
            @keyup.enter="handleSearch"
          >
            <template #suffix>
              <el-tooltip content="上传文件">
                <el-button 
                  type="text" 
                  icon="el-icon-upload" 
                  @click="handleUploadClick"
                />
              </el-tooltip>
              <el-button 
                type="primary" 
                :loading="isLoading"
                @click="handleSearch"
              >
                发送
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  height: 100vh;
  background: #f5f7fa;
}
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100vh;
  transition: all 0.3s;
  margin-left: 0;
  &.full-width {
    margin-left: 0;
    flex: 1;
  }
}
// 修改消息列表样式
.message-list {
  flex: 1;
  overflow: hidden;
  padding: 20px;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 60px;
  bottom: 100px;
  width: 97%;
  .el-scrollbar {
    flex: 1;
    overflow: hidden;
    .el-scrollbar__wrap {
      overflow-x: hidden;
    }
  }
}
// 修改欢迎语样式
.welcome-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #666;
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1;
  ul {
    list-style-type: none;
    padding-left: 0;
    margin-top: 20px;
    li {
      margin-bottom: 10px;
    }
  }
}
.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #e4e7ed;
  position: absolute;
  bottom: 0;
  width: 100%;
  z-index: 2;
}
.input-wrapper {
  max-width: 800px;
  margin: 0 auto;
}
.question-input {
  border-radius: 20px;
  padding-right: 110px;
  &:deep(.el-input__inner) {
    border-radius: 20px;
    padding-right: 110px;
  }
}
/* 新增样式 */
.sidebar-container {
  position: relative;
  height: 100%;
  width: 0;
  overflow: hidden;
  transition: all 0.3s;
  &.expanded {
    width: 280px;
  }
}
.sidebar-trigger {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 60px;
  background: #fff;
  border-radius: 0 8px 8px 0;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 100;
  &:hover {
    background: #f5f7fa;
  }
  &.collapsed {
    left: 0;
  }
}
.sidebar {
  width: 280px;
  height: 100%;
  background: #fff;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  position: absolute;
  left: 0;
  top: 0;
  &.collapsed {
    transform: translateX(-100%);
  }
  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #e4e7ed;
    font-weight: bold;
  }
  .history-list {
    height: calc(100% - 60px);
    overflow-y: auto;
    padding: 10px;
  }
  .session-item {
    padding: 12px;
    margin-bottom: 8px;
    border-radius: 6px;
    transition: all 0.2s;
    cursor: pointer;
    &:hover {
      background-color: #f1f1f1;
    }
    &.active {
      background-color: #e8f4ff;
    }
  }
  .session-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
  }
  .messages-preview {
    font-size: 13px;
    color: #999;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
.message-item {
  margin-bottom: 15px;
  align-self: flex-start;
  transition: all 0.3s;
}
/* 新增展开按钮样式 */
.expand-trigger {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 60px;
  background: #fff;
  border-radius: 0 8px 8px 0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 99;
  &:hover {
    background: #f5f7fa;
  }
}
/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  background-color: #f5f5f5;
}
::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: #c1c1c1;
}
::-webkit-scrollbar-track {
  border-radius: 10px;
  background-color: #f5f5f5;
}
</style>