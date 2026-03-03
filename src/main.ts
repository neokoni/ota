import './assets/main.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import '@fontsource/noto-sans-sc/400.css';
import '@fontsource/noto-sans-sc/500.css';
import '@fontsource/noto-sans-sc/700.css';

import '@material/web/all.js';
import { themeFromSourceColor, applyTheme, argbFromHex } from '@material/material-color-utilities';

// Apply Material 3 baseline theme immediately (before wallpaper loads)
const baselineTheme = themeFromSourceColor(argbFromHex('#6750A4'));
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
applyTheme(baselineTheme, { dark: prefersDark, brightnessSuffix: true });

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(router)

app.mount('#app')
