import { createApp } from 'vue'
import './styles/main.css' // We will copy the CSS here
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
