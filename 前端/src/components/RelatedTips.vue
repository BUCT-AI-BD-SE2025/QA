<template>
  <div class="related-tips">
    <h4>历史记录</h4>
    <el-scrollbar max-height="300px">
      <div v-if="history.length">
        <el-tag 
          v-for="(item, index) in history" 
          :key="index" 
          size="small" 
          style="margin: 5px 0"
          @click="reSearch(item)"
          class="history-tag"
        >
          {{ item }}
        </el-tag>
      </div>
      <p v-else class="no-history">暂无搜索记录</p>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  history: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['re-search'])

const reSearch = (question) => {
  emit('re-search', question)
}
</script>

<style scoped>
.related-tips h4 {
  margin-bottom: 10px;
}
.history-tag:hover {
  cursor: pointer;
  background-color: #ecf5ff;
}
.no-history {
  color: #999;
  font-size: 13px;
}
</style>