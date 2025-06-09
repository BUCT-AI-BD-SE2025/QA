<template>
  <div class="appearance-setting">
    <h3>外观设置</h3>
    <el-form label-width="80px">
      <el-form-item label="主题">
        <el-select v-model="theme" placeholder="请选择主题">
          <el-option label="浅色" value="light" />
          <el-option label="深色" value="dark" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
</script>