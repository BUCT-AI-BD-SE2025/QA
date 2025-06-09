<template>
  <div class="settings-page">
    <el-card class="settings-card">
      <div class="settings-header">
        <h3>设置</h3>
        <el-button @click="$router.push('/')">返回主界面</el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="个人资料" name="profile">
          <profile-setting />
        </el-tab-pane>
        <el-tab-pane label="外观设置" name="appearance">
          <appearance-setting />
        </el-tab-pane>
        <el-tab-pane label="通知设置" name="notifications">
          <notification-setting />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('profile')
</script>

<style scoped>
.settings-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.settings-card {
  padding: 20px;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>