import { createApp } from 'vue'
import { createPinia } from 'pinia' // ✅ 确保已导入
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import '@/assets/css/global.css'
import '@/assets/css/text.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


// ✅ 创建 Pinia 实例
const pinia = createPinia()
const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
// ✅ 按正确顺序注册插件
app.use(pinia)   // 先注册 Pinia
app.use(router)  // 再注册路由
app.use(ElementPlus)

app.mount('#app')