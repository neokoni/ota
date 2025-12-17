<template>
  <div class="changelog-view">
    <div class="header-section">
      <mdui-button-icon icon="arrow_back--two-tone" @click="$router.back()"></mdui-button-icon>
      <div>
        <h1>{{ deviceName }}</h1>
        <a :href="jsonUrl" target="_blank" class="json-link">查看原始 JSON 文件</a>
        <p class="subtitle">{{ system }} - {{ version }}</p>
      </div>
    </div>

    <div class="changelog-list">
      <!-- Mock Data: Newest on top -->
      <mdui-card class="changelog-card" variant="filled">
        <div class="card-header">
          <h3>更新 2025-12-18</h3>
          <mdui-chip variant="filter" selected>最新</mdui-chip>
        </div>
        <mdui-divider></mdui-divider>
        <div class="card-body">
          <ul>
            <li>更新至 Android 16 底层</li>
            <li>修复系统稳定性问题</li>
            <li>提升电池续航</li>
            <li>添加新的自定义选项</li>
          </ul>
        </div>
      </mdui-card>

      <mdui-card class="changelog-card" variant="elevated">
        <div class="card-header">
          <h3>更新 2025-11-01</h3>
        </div>
        <mdui-divider></mdui-divider>
        <div class="card-body">
          <ul>
            <li>{{ deviceName }} 的 AviumUI 初始版本</li>
            <li>基础功能实现</li>
          </ul>
        </div>
      </mdui-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const codename = computed(() => route.params.codename as string);
const system = computed(() => route.params.system as string);
const version = computed(() => route.params.version as string);

const deviceMap: Record<string, string> = {
  'lemonades': '一加9R',
  'nabu': '小米平板5'
};

const deviceName = computed(() => deviceMap[codename.value] || codename.value);
const jsonUrl = computed(() => `/ota/${codename.value}.json`); // Placeholder URL
</script>

<style scoped>
.changelog-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.header-section h1 {
  margin: 0;
  font-size: 1.75rem;
}

.json-link {
  display: block;
  font-size: 0.875rem;
  color: rgb(var(--mdui-color-primary));
  text-decoration: none;
  margin-top: 4px;
}

.json-link:hover {
  text-decoration: underline;
}

.subtitle {
  margin: 4px 0 0 0;
  opacity: 0.7;
}

.changelog-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.changelog-card {
  padding: 0;
  width: 100%;
}

.card-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}

.card-body {
  padding: 16px 24px;
}

ul {
  margin: 0;
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
}
</style>