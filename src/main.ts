import './assets/main.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import '@fontsource/noto-sans-sc/400.css';
import '@fontsource/noto-sans-sc/500.css';
import '@fontsource/noto-sans-sc/700.css';

import '@m3e/web/theme';
import '@m3e/web/app-bar';
import '@m3e/web/button';
import '@m3e/web/card';
import '@m3e/web/chips';
import '@m3e/web/drawer-container';
import '@m3e/web/heading';
import '@m3e/web/icon';
import '@m3e/web/icon-button';
import '@m3e/web/list';
import '@m3e/web/nav-rail';

import '@m3e/icons/outlined/arrow_back';
import '@m3e/icons/outlined/arrow_forward';
import '@m3e/icons/outlined/brightness_auto';
import '@m3e/icons/outlined/check_circle';
import '@m3e/icons/outlined/chevron_right';
import '@m3e/icons/outlined/dark_mode';
import '@m3e/icons/outlined/deployed_code';
import '@m3e/icons/outlined/devices';
import '@m3e/icons/outlined/history';
import '@m3e/icons/outlined/home';
import '@m3e/icons/outlined/light_mode';
import '@m3e/icons/outlined/menu';
import '@m3e/icons/outlined/menu_open';
import '@m3e/icons/outlined/open_in_new';
import '@m3e/icons/outlined/rocket_launch';
import '@m3e/icons/outlined/system_update_alt';
import '@m3e/icons/outlined/update';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { initTheme } from './config/theme';

initTheme();

const app = createApp(App);
app.use(router);
app.mount('#app');
