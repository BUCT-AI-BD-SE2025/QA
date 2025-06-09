import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import QuestionView from '../views/QuestionView.vue'
import AuthView from '../views/AuthView.vue'
import SettingsView from '../views/SettingsView.vue'
// ✅ 添加 Pinia 相关导入
import { useUserStore } from '@/stores/userStore'

// ✅ 创建 Pinia 实例
const pinia = createPinia()

const routes = [
  {
    path: '/',
    name: 'Home',
    component: QuestionView
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ 修改后的路由守卫
router.beforeEach((to, from, next) => {
  // ✅ 通过 Pinia 实例获取 store
  const userStore = useUserStore(pinia)
  
  // ✅ 加载本地存储数据
  userStore.loadFromStorage()
  
  if (to.meta.requiresAuth && !userStore.isLogin) {
    next('/auth')
  } else {
    next()
  }
})

export default router