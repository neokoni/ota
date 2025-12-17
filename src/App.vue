<template>
  <mdui-layout>
    <!-- Top App Bar -->
    <mdui-top-app-bar
        class="main-top-app-bar"
        scroll-behavior="elevate"
    >
      <mdui-button-icon @click="drawerOpen = !drawerOpen" icon="menu--two-tone"></mdui-button-icon>
      <mdui-avatar src="https://res.neokoni.ink/neokoni/svg/favicon.svg"></mdui-avatar>
      <mdui-top-app-bar-title>Neokoni's OTA Center</mdui-top-app-bar-title>
      <div style="flex-grow: 1"></div>
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
    <mdui-layout-main class="layout-main" style="min-height: 100vh">
      <router-view></router-view>
    </mdui-layout-main>
  </mdui-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { devices } from '@/config/devices';

const drawerOpen = ref(false);
const router = useRouter();

function navigate(path: string) {
  router.push(path);
  // Close drawer on mobile/overlay mode
  drawerOpen.value = false;
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>