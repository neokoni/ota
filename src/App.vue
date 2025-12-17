<template>
  <mdui-layout>
    <!--顶栏部分-->
    <mdui-top-app-bar
        class="main-top-app-bar"
        scroll-target="header-scroll-behavior-elevate"
        scroll-behavior="elevate"
    >
      <mdui-button-icon @click="switchDrawer" id="menu-button" icon="menu--two-tone"></mdui-button-icon>
      <mdui-avatar src="https://res.neokoni.ink/neokoni/svg/favicon.svg"></mdui-avatar>
      <mdui-top-app-bar-title>Neokoni's OTA Center</mdui-top-app-bar-title>
      <div style="flex-grow: 1"></div>
      <div class="header-scroll-behavior-elevate" style="height: 160px;overflow: auto;">
        <div style="height: 1000px"></div>
      </div>
    </mdui-top-app-bar>

    <!--左侧抽屉部分-->
    <mdui-navigation-drawer class="main-navigation-drawer">
      <mdui-list>
        <mdui-list-item>Navigation drawer</mdui-list-item>
      </mdui-list>
    </mdui-navigation-drawer>
    <!--主内容部分-->
    <mdui-layout-main class="layout-main" style="min-height: 300px">
      <div>
        Main
      </div>
    </mdui-layout-main>
  </mdui-layout>
</template>

<style scoped></style>
<script setup lang="ts">
import 'mdui/mdui.css';
import 'mdui';

function switchDrawer() {
  const drawer = document.querySelector("mdui-navigation-drawer");
  if (drawer) {
    drawer.open = !drawer.open;
  }
}
</script>