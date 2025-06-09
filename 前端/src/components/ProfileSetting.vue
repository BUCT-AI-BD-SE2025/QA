<template>
  <div class="profile-setting">
    <h3>个人资料</h3>
    <el-form label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="username" disabled />
      </el-form-item>
      <el-form-item label="头像">
        <el-upload action="/api/upload" :show-file-list="false">
          <el-button type="primary">上传头像</el-button>
        </el-upload>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
// 修改导入方式
import { useUserStore } from '@/stores/userStore'

// 获取store实例
const store = useUserStore()

// 修改获取用户名的方式
const username = ref(store.username)
</script>