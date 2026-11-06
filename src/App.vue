<template>
  <div class="app-shell">
    <m3e-app-bar class="top-app-bar">
      <m3e-icon-button slot="leading" aria-label="切换导航抽屉" toggle>
        <m3e-drawer-toggle for="nav-drawer"></m3e-drawer-toggle>
        <m3e-icon name="menu"></m3e-icon>
        <m3e-icon slot="selected" name="menu_open"></m3e-icon>
      </m3e-icon-button>

      <span slot="title" class="brand" @click="navigate('/')">
        <img class="brand-logo" src="https://res.neokoni.ink/neokoni/svg/favicon.svg" alt="" />
        <span class="brand-name">NeoBuilds Changelog</span>
      </span>

      <m3e-icon-button slot="trailing" :title="themeLabel" :aria-label="themeLabel" @click="cycleThemeMode">
        <m3e-icon :name="themeIcon"></m3e-icon>
      </m3e-icon-button>
    </m3e-app-bar>

    <m3e-drawer-container
      class="drawer-container"
      :start="drawerOpen"
      start-mode="auto"
      @change="syncDrawer"
    >
      <nav slot="start" id="nav-drawer" class="navigation-drawer" aria-label="站点导航">
        <m3e-nav-rail mode="compact">
          <m3e-nav-item
            :selected="route.path === '/'"
            @click="navigate('/')"
          >
            <m3e-icon slot="icon" name="home"></m3e-icon>
            主页
          </m3e-nav-item>
          <m3e-nav-item
            :selected="isDevicesSection"
            @click="navigate('/devices')"
          >
            <m3e-icon slot="icon" name="devices"></m3e-icon>
            设备列表
          </m3e-nav-item>
        </m3e-nav-rail>
      </nav>

      <main class="layout-main">
        <div class="content-area">
          <router-view v-slot="{ Component, route: currentRoute }">
            <transition name="route" mode="out-in">
              <component :is="Component" :key="currentRoute.path" />
            </transition>
          </router-view>
        </div>

        <footer class="site-footer">
          <a
            v-for="item in siteConfig"
            :key="item.icp"
            :href="item.icpLink"
            target="_blank"
            rel="noopener noreferrer"
          >{{ item.icp }}</a>
        </footer>
      </main>
    </m3e-drawer-container>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { siteConfig } from '@/config/site';
import { cycleThemeMode, themeMode } from '@/config/theme';

const route = useRoute();
const router = useRouter();
const persistentDrawer = window.matchMedia('(min-width: 840px)');
const drawerOpen = ref(persistentDrawer.matches);

const isDevicesSection = computed(() => route.path.startsWith('/device'));

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

function navigate(path: string) {
  if (!persistentDrawer.matches) drawerOpen.value = false;
  if (route.path !== path) void router.push(path);
}

function syncDrawer(event: Event) {
  const container = event.currentTarget as HTMLElement & { start: boolean };
  drawerOpen.value = container.start;
}
</script>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}

.top-app-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  --m3e-app-bar-container-color: var(--md-sys-color-surface);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 200ms ease;
}

.brand:hover {
  background-color: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent);
}

.brand-logo {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.brand-name {
  font-weight: 500;
}

.drawer-container {
  flex: 1;
  --m3e-drawer-container-width: 104px;
  --m3e-drawer-divider-thickness: 0px;
}

.navigation-drawer {
  width: 100%;
  height: 100%;
  background-color: var(--md-sys-color-surface-container-low);
  --m3e-nav-rail-compact-width: 104px;
}

.layout-main {
  display: flex;
  flex-direction: column;
  min-height: calc(100dvh - 64px);
}

.content-area {
  flex: 1;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
  box-sizing: border-box;
}

.site-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  justify-content: center;
  padding: 24px 16px 32px;
  font-size: 0.8125rem;
  color: var(--md-sys-color-on-surface-variant);
}

.site-footer a {
  color: inherit;
  text-decoration: none;
}

.site-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .content-area {
    padding: 16px;
  }
}

.route-enter-active {
  animation: route-enter var(--md-sys-motion-spring-default-spatial, 500ms cubic-bezier(0.2, 0, 0, 1)) both;
}

.route-leave-active {
  animation: route-leave var(--md-sys-motion-spring-fast-effects, 200ms cubic-bezier(0.31, 0.94, 0.34, 1)) both;
}

@keyframes route-enter {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes route-leave {
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .route-enter-active,
  .route-leave-active {
    animation: none;
  }
}
</style>
