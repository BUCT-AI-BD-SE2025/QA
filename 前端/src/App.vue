<template>
  <router-view />
</template>

<style>
/* ✅ 新增全局样式 */
#app {
  font-family: Arial, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止全局滚动 */
}

/* 新增：确保 html 和 body 占满整个视口 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden; /* 隐藏浏览器原生滚动条 */
}
</style>