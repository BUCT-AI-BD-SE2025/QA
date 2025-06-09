import { defineStore } from 'pinia'

// ✅ 确保使用命名导出
export const useUserStore = defineStore('user', {
  state: () => ({
    isLogin: false,
    username: '',
    avatar: '',
    settings: {
      theme: 'light',
      notifications: true
    }
  }),
  actions: {
    login(username) {
      this.isLogin = true
      this.username = username
      localStorage.setItem('user', JSON.stringify({
        username,
        isLogin: true
      }))
    },
    logout() {
      this.isLogin = false
      this.username = ''
      localStorage.removeItem('user')
    },
    loadFromStorage() {
      // ✅ 保持原有存储加载逻辑
      const userData = localStorage.getItem('user')
      if (userData) {
        const data = JSON.parse(userData)
        this.isLogin = data.isLogin
        this.username = data.username
      }
    }
  }
})