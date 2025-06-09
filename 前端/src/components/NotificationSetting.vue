<template>
  <div class="notification-setting">
    <h3>通知设置</h3>
    <el-switch v-model="notifications" active-text="开启" inactive-text="关闭" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
</script>