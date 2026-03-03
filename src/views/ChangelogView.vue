<template>
  <div class="changelog-view">
    <div class="header-section">
      <md-icon-button @click="$router.back()">
        <md-icon>arrow_back</md-icon>
      </md-icon-button>
      <div>
        <h1>{{ deviceName }}</h1>
        <a v-if="otaUrl" :href="otaUrl" target="_blank" class="json-link">查看系统更新文件 (JSON)</a>
        <p class="subtitle">{{ systemName }} - {{ versionName }}</p>
      </div>
    </div>

    <div class="changelog-list">
      <template v-if="changelogData">
        <div
          v-for="(release, index) in changelogData.releases"
          :key="release.date"
          class="changelog-card"
          :class="index === 0 ? 'changelog-card--filled' : 'changelog-card--elevated'"
        >
          <div class="card-header">
            <h3>{{ release.date }}</h3>
            <md-filter-chip v-if="index === 0" label="最新" selected></md-filter-chip>
          </div>
          <md-divider></md-divider>
          <div class="card-body">
            <ul>
              <li v-for="(change, idx) in release.changes" :key="idx" v-html="change"></li>
            </ul>
          </div>
        </div>
      </template>
      <div v-else class="state-container">
        <p>未找到更新日志</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { getDevice, getSystem } from '@/config/devices';

const route = useRoute();
const codename = computed(() => route.params.codename as string);
const systemName = computed(() => route.params.system as string);
const versionName = computed(() => route.params.version as string);

const device = computed(() => getDevice(codename.value));
const deviceName = computed(() => device.value?.name || codename.value);

const system = computed(() => getSystem(codename.value, systemName.value));
const versionConfig = computed(() => system.value?.versions.find(v => v.version === versionName.value));
const otaUrl = computed(() => versionConfig.value?.otaUrl);

const changelogData = computed(() => {
  if (!versionConfig.value) return null;
  // Sort releases by date descending
  const releases = [...(versionConfig.value.releases || [])];
  releases.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  return { releases };
});
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
  color: var(--md-sys-color-on-surface);
}

.json-link {
  display: block;
  font-size: 0.875rem;
  color: var(--md-sys-color-primary);
  text-decoration: none;
  margin-top: 4px;
}

.json-link:hover {
  text-decoration: underline;
}

.subtitle {
  margin: 4px 0 0 0;
  color: var(--md-sys-color-on-surface-variant);
}

.changelog-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.state-container {
  display: flex;
  justify-content: center;
  padding: 40px;
  color: var(--md-sys-color-on-surface-variant);
}

.changelog-card {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
}

.changelog-card--filled {
  background-color: var(--md-sys-color-primary-container);
  border: 1px solid transparent;
}

.changelog-card--elevated {
  background-color: var(--md-sys-color-surface-container-low);
  border: 1px solid var(--md-sys-color-outline-variant);
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.card-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--md-sys-color-on-surface);
}

.changelog-card--filled .card-header h3 {
  color: var(--md-sys-color-on-primary-container);
}

.card-body {
  padding: 16px 24px;
}

.card-body ul {
  margin: 0;
  padding-left: 20px;
}

.card-body li {
  margin-bottom: 8px;
  line-height: 1.5;
  color: var(--md-sys-color-on-surface);
}

.changelog-card--filled .card-body li {
  color: var(--md-sys-color-on-primary-container);
}

.card-body li:last-child {
  margin-bottom: 0;
}
</style>
