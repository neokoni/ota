// import './assets/main.css'
import 'mdui/mdui.css';
import 'mdui';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(router)

app.mount('#app')
