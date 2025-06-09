<template>
  <div v-if="answer" class="answer-card">
    <el-card>
      <div v-html="answer.content"></div>
      <div class="source">来源：{{ answer.source }}</div>
    </el-card>
  </div>
  <div v-else class="placeholder">
    <el-card>
      <p>欢迎使用海外藏中国文物知识问答系统</p>
      <p>示例问题：</p>
      <ul>
        <li>• 故宫博物院收藏的《千里江山图》作者是谁？</li>
        <li>• 商周时期的青铜器主要有哪些类型？</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup>
defineProps({
  answer: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.answer-card .source {
  margin-top: 15px;
  color: #666;
  font-size: 14px;
}
.placeholder ul {
  padding-left: 20px;
}
</style>