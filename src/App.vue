<template>
  <div class="app-layout">
    <!-- Top App Bar -->
    <header class="top-app-bar" :class="{ scrolled: isScrolled }">
      <md-icon-button class="menu-btn" @click="drawerOpen = !drawerOpen">
        <md-icon>menu</md-icon>
      </md-icon-button>
      <div class="app-bar-branding" @click="navigate('/')">
        <img src="https://res.neokoni.ink/neokoni/svg/favicon.svg" class="app-bar-logo" alt="logo" />
        <span class="app-bar-title">Neokoni's OTA Center</span>
      </div>
      <div class="spacer"></div>
      <md-icon-button @click="toggleTheme" :title="themeLabel">
        <md-icon>{{ themeIcon }}</md-icon>
      </md-icon-button>
    </header>

    <!-- Backdrop overlay for mobile drawer -->
    <div class="drawer-backdrop" :class="{ visible: drawerOpen }" @click="drawerOpen = false"></div>

    <!-- Body row: drawer + main content side by side (push layout, same layer) -->
    <div class="body-row">
      <!-- Navigation Drawer wrapper — animates width 0→280px to push content -->
      <div class="drawer-wrapper" :class="{ open: drawerOpen }">
        <nav class="navigation-drawer">
          <md-list>
            <div class="nav-item-wrap">
              <md-list-item type="button" @click="navigate('/')">
                <md-icon slot="start">home</md-icon>
                主页
              </md-list-item>
            </div>
            <md-divider></md-divider>
            <div class="list-subheader">设备列表</div>
            <div
              v-for="device in devices"
              :key="device.codename"
              class="nav-item-wrap"
            >
              <md-list-item
                type="button"
                @click="navigate(`/device/${device.codename}`)"
              >
                <md-icon slot="start">smartphone</md-icon>
                {{ device.name }} ({{ device.codename }})
              </md-list-item>
            </div>
          </md-list>
        </nav>
      </div>

      <!-- Main Content -->
      <main class="layout-main">
        <div class="content-area">
          <router-view></router-view>
        </div>

        <footer class="site-footer">
          <a v-for="(item, index) in siteConfig" :key="index" :href="item.icpLink" target="_blank" rel="noopener noreferrer">
            {{ item.icp }}<br>
          </a>
        </footer>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { themeFromImage, themeFromSourceColor, applyTheme } from '@material/material-color-utilities';
import type { Theme } from '@material/material-color-utilities';
import { devices } from '@/config/devices';
import { siteConfig, wallpaperConfig } from '@/config/site';

const drawerOpen = ref(false);
const router = useRouter();
const isScrolled = ref(false);

// Theme Logic
type ThemeMode = 'auto' | 'light' | 'dark';
const themeMode = ref<ThemeMode>('auto');
let loadedTheme: Theme | null = null;

const themeIcon = computed(() => {
  switch (themeMode.value) {
    case 'light': return 'light_mode';
    case 'dark': return 'dark_mode';
    default: return 'brightness_auto';
  }
});

const themeLabel = computed(() => {
  switch (themeMode.value) {
    case 'light': return '当前: 浅色模式';
    case 'dark': return '当前: 深色模式';
    default: return '当前: 自动模式';
  }
});

function isDarkMode(mode: ThemeMode): boolean {
  return mode === 'dark' || (mode === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
}

function applyCurrentTheme(theme: Theme, mode: ThemeMode) {
  applyTheme(theme, { dark: isDarkMode(mode), brightnessSuffix: true });
}

function toggleTheme() {
  if (themeMode.value === 'auto') themeMode.value = 'light';
  else if (themeMode.value === 'light') themeMode.value = 'dark';
  else themeMode.value = 'auto';

  if (loadedTheme) {
    applyCurrentTheme(loadedTheme, themeMode.value);
  }
  localStorage.setItem('theme-mode', themeMode.value);
}

async function initDynamicColors() {
  if (!wallpaperConfig.api) return;

  const timeout = 5 * 1000;
  const img = new Image();
  img.crossOrigin = 'Anonymous';

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
    loadedTheme = await themeFromImage(img);
    applyCurrentTheme(loadedTheme, themeMode.value);
    console.log('Dynamic color applied from wallpaper');
  } catch (error) {
    console.warn('Dynamic color initialization failed:', error);
    // Apply MD3 baseline purple theme as fallback so surface tokens are defined
    loadedTheme = themeFromSourceColor(0xFF6750A4);
    applyCurrentTheme(loadedTheme, themeMode.value);
  }
}

function handleScroll() {
  isScrolled.value = window.scrollY > 4;
}

onMounted(() => {
  const saved = localStorage.getItem('theme-mode') as ThemeMode;
  if (saved && ['auto', 'light', 'dark'].includes(saved)) {
    themeMode.value = saved;
  }

  window.addEventListener('scroll', handleScroll);
  initDynamicColors();
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

function navigate(path: string) {
  router.push(path);
}
</script>

<style scoped>
/* App Layout */
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Top App Bar */
.top-app-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  height: 64px;
  padding: 0 24px;
  background-color: var(--md-sys-color-surface);
  transition: box-shadow 200ms ease, background-color 200ms ease;
}

.top-app-bar.scrolled {
  background-color: var(--md-sys-color-surface-container);
  box-shadow: var(--md-sys-elevation-level2, 0 3px 6px rgba(0,0,0,0.12));
}

.app-bar-branding {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background-color 200ms ease;
}

.app-bar-branding:hover {
  background-color: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent);
}

.app-bar-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.app-bar-title {
  font-size: 1.375rem;
  font-weight: 400;
  color: var(--md-sys-color-on-surface);
  letter-spacing: 0;
  font-family: var(--font-family);
}

.spacer {
  flex: 1;
}

/* Body row: drawer + main sit side-by-side, same layer */
.body-row {
  display: flex;
  flex: 1;
}

/* Drawer wrapper animates width 0 → 280px to push main content */
.drawer-wrapper {
  flex-shrink: 0;
  align-self: stretch;
  width: 0;
  overflow: hidden;
  transition: width 300ms cubic-bezier(0.2, 0, 0, 1);
}

.drawer-wrapper.open {
  width: 280px;
}

/* Navigation Drawer — in-flow, solid background */
.navigation-drawer {
  width: 280px;
  min-height: 100%;
  background-color: var(--md-sys-color-surface-container-low);
  border-radius: 0 16px 16px 0;
  overflow-y: auto;
  padding-top: 12px;
  /* Transparent md-list background so drawer colour shows uniformly */
  --md-list-container-color: transparent;
}

/* MD3 Navigation Drawer: pill-shaped (28 dp radius) item highlight, inset 12 px */
.nav-item-wrap {
  position: relative;
  margin: 2px 12px;
  border-radius: 28px;
  transition: background 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item-wrap:hover {
  background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent);
}

.navigation-drawer :deep(md-list-item) {
  border-radius: 28px;
  /* Disable built-in flat-opacity hover layer; our .nav-item-wrap provides the hover styles */
  --md-list-item-hover-state-layer-opacity: 0;
  --md-list-item-leading-space: 16px;
  --md-list-item-trailing-space: 16px;
}

.list-subheader {
  padding: 8px 16px 4px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--md-sys-color-on-surface-variant);
}

/* Give the divider some breathing room and use the outline-variant token */
.navigation-drawer :deep(md-divider) {
  margin: 8px 0;
  --md-divider-color: var(--md-sys-color-outline-variant);
}

/* Main Layout */
.layout-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.content-area {
  flex: 1;
}

/* Footer */
.site-footer {
  text-align: center;
  padding: 20px;
  margin-top: auto;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
}

.site-footer a {
  color: inherit;
  text-decoration: none;
}

.site-footer a:hover {
  text-decoration: underline;
}

/* Drawer backdrop for mobile overlay */
.drawer-backdrop {
  display: none;
}

@media (max-width: 840px) {
  .app-bar-title {
    font-size: 1.1rem;
  }

  .drawer-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 49;
    opacity: 0;
    pointer-events: none;
    transition: opacity 300ms ease;
  }

  .drawer-backdrop.visible {
    opacity: 1;
    pointer-events: auto;
  }

  /* Overlay drawer on mobile — floats above content instead of pushing it */
  .drawer-wrapper {
    position: fixed;
    top: 64px;
    left: 0;
    height: calc(100vh - 64px);
    z-index: 50;
    overflow: hidden;
  }

  .drawer-wrapper.open {
    box-shadow: 4px 0 16px rgba(0, 0, 0, 0.2);
  }

  .navigation-drawer {
    border-radius: 0 16px 16px 0;
  }
}

@media (max-width: 600px) {
  .app-bar-title {
    font-size: 1rem;
  }

  .top-app-bar {
    padding: 0 8px;
  }
}
</style>