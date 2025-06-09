<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <div class="auth-header">
        <h2>登录 / 注册</h2>
        <el-button @click="$router.push('/')">返回</el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <login-form @success="handleLoginSuccess" />
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <register-form @success="handleRegisterSuccess" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import LoginForm from '@/components/LoginForm.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('login')

const handleLoginSuccess = () => {
  router.push('/')
}

const handleRegisterSuccess = () => {
  activeTab.value = 'login'
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.auth-card {
  width: 400px;
  padding: 20px;
}

.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>