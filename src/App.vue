<template>
  <mdui-layout>
    <!-- Top App Bar -->
    <mdui-top-app-bar
        class="main-top-app-bar"
        scroll-behavior="elevate"
    >
      <mdui-button-icon @click="drawerOpen = !drawerOpen" icon="menu--two-tone"></mdui-button-icon>
      <div class="app-bar-branding" @click="navigate('/')">
        <mdui-avatar src="https://res.neokoni.ink/neokoni/svg/favicon.svg"></mdui-avatar>
        <mdui-top-app-bar-title class="app-title">Neokoni's OTA Center</mdui-top-app-bar-title>
      </div>
      <div style="flex-grow: 1"></div>
      <mdui-button-icon :icon="themeIcon" @click="toggleTheme"></mdui-button-icon>
    </mdui-top-app-bar>

    <!-- Navigation Drawer -->
    <mdui-navigation-drawer 
      class="main-navigation-drawer"
      :open="drawerOpen"
      @open="drawerOpen = true"
      @close="drawerOpen = false"
      close-on-overlay-click
    >
      <mdui-list>
        <mdui-list-item rounded @click="navigate('/')" icon="home--two-tone">主页</mdui-list-item>
        <mdui-divider></mdui-divider>
        <mdui-list-subheader>设备列表</mdui-list-subheader>
        <mdui-list-item 
          v-for="device in devices" 
          :key="device.codename"
          rounded 
          @click="navigate(`/device/${device.codename}`)" 
          icon="smartphone--two-tone"
        >
          {{ device.name }} ({{ device.codename }})
        </mdui-list-item>
      </mdui-list>
    </mdui-navigation-drawer>

    <!-- Main Content -->
    <mdui-layout-main class="layout-main" style="min-height: 100vh; display: flex; flex-direction: column;">
      <div style="flex: 1;">
        <router-view></router-view>
      </div>
      
      <footer class="site-footer">
        <a v-for="(item, index) in siteConfig" :key="index" :href="item.icpLink" target="_blank" rel="noopener noreferrer">
          {{ item.icp }}<br>
        </a>
      </footer>
    </mdui-layout-main>
  </mdui-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { setTheme, getColorFromImage, setColorScheme } from 'mdui';
import { devices } from '@/config/devices';
import { siteConfig, wallpaperConfig } from '@/config/site';

const drawerOpen = ref(false);
const router = useRouter();

// Theme Logic
type ThemeMode = 'auto' | 'light' | 'dark';
const themeMode = ref<ThemeMode>('auto');

const themeIcon = computed(() => {
  switch (themeMode.value) {
    case 'light': return 'light_mode--two-tone';
    case 'dark': return 'dark_mode--two-tone';
    default: return 'brightness_auto--two-tone';
  }
});

function toggleTheme() {
  if (themeMode.value === 'auto') themeMode.value = 'light';
  else if (themeMode.value === 'light') themeMode.value = 'dark';
  else themeMode.value = 'auto';
  
  setTheme(themeMode.value);
  localStorage.setItem('theme-mode', themeMode.value);
}

async function initDynamicColors() {
  if (!wallpaperConfig.api) return;

  const timeout = 3000; // 3 seconds timeout
  const img = new Image();
  img.crossOrigin = "Anonymous";

  const loadPromise = new Promise<HTMLImageElement>((resolve, reject) => {
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('Failed to load image'));
    img.src = wallpaperConfig.api;
  });

  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), timeout);
  });

  try {
    await Promise.race([loadPromise, timeoutPromise]);
    const color = await getColorFromImage(img);
    setColorScheme(color);
    console.log('Dynamic color applied:', color);
  } catch (error) {
    console.warn('Dynamic color initialization failed:', error);
    // Fallback or do nothing (default colors)
  }
}

onMounted(() => {
  const saved = localStorage.getItem('theme-mode') as ThemeMode;
  if (saved && ['auto', 'light', 'dark'].includes(saved)) {
    themeMode.value = saved;
    setTheme(saved);
  } else {
    setTheme('auto');
  }
  
  initDynamicColors();
});

function navigate(path: string) {
  router.push(path);
  // Close drawer on mobile/overlay mode
  drawerOpen.value = false;
}
</script>

<style scoped>
/* Add any component-specific styles here */
.site-footer {
  text-align: center;
  padding: 20px;
  margin-top: auto;
  color: rgb(var(--mdui-color-on-surface-variant));
  font-size: 0.875rem;
}

.site-footer a {
  color: inherit;
  text-decoration: none;
}

.site-footer a:hover {
  text-decoration: underline;
}

.app-bar-branding {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-left: 12px;
}

.app-bar-branding mdui-avatar {
  margin-right: 12px;
}

@media (max-width: 600px) {
  .app-title {
    font-size: 1.1rem;
  }
}
</style>