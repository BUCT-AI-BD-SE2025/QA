<template>
  <el-form @submit.prevent="submitLogin">
    <el-form-item label="用户名">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password" type="password" show-password />
    </el-form-item>
    <el-button type="primary" native-type="submit" block>登录</el-button>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'
// 修改导入方式
import { useUserStore } from '@/stores/userStore'

const form = ref({
  username: '',
  password: ''
})

// 获取store实例
const store = useUserStore()

const submitLogin = () => {
  // 修改调用方式
  store.login(form.value.username)
}
</script>