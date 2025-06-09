<template>
  <el-header class="header-bar">
    <div class="logo">
      <!-- 修改图片路径 -->
      <img src="@/assets/images/logo.png" alt="Logo" style="width: 40px; height: 40px;" />
      <span>海外藏文物问答</span>
    </div>
    <!-- 新增返回按钮 -->
    <el-button v-if="$route.path !== '/'" @click="$router.push('/')" class="back-btn">
      返回主界面
    </el-button>
    <div class="user-info">
      <el-button v-if="!isLogin" @click="goToAuth">登录</el-button>
      <el-dropdown v-else @command="handleCommand">
        <span class="el-dropdown-link">
          {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="settings">设置</el-dropdown-item>
            <el-dropdown-item command="logout">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
// 修改导入方式
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const route = useRoute()
// 修改使用方式
const store = useUserStore()
const isLogin = ref(store.isLogin)
const username = ref(store.username)

const goToAuth = () => {
  router.push('/auth')
}

const handleCommand = (command) => {
  if (command === 'logout') {
    store.logout()
    router.push('/')
  } else if (command === 'settings') {
    router.push('/settings')
  }
}
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eaeaea;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo img {
  height: 40px;
  margin-right: 10px;
}
.user-info {
  cursor: pointer;
}
.back-btn {
  margin-left: 20px;
}
</style>