import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router' // Import the router

const pinia = createPinia()

createApp(App)
  .use(router) // Use the router
  .use(pinia) // Use Pinia
  .mount('#app')
