<template>
  <el-input 
    v-model="question"
    :placeholder="'请输入您的问题（例如：清明上河图的作者是谁？）'"
    aria-label="问题输入框"
    @keyup.enter="onSearch"
  >
    <template #append>
      <el-button @click="onSearch">提问</el-button>
    </template>
  </el-input>
</template>

<script setup>
import { ref } from 'vue'

const question = ref('')
const emit = defineEmits(['search'])

const onSearch = () => {
  if (question.value.trim()) {
    emit('search', question.value.trim())
  }
}
</script>