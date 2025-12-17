<template>
  <div class="changelog-view">
    <div class="header-section">
      <mdui-button-icon icon="arrow_back--two-tone" @click="$router.back()"></mdui-button-icon>
      <div>
        <h1>{{ deviceName }}</h1>
        <a v-if="otaUrl" :href="otaUrl" target="_blank" class="json-link">查看系统更新文件 (JSON)</a>
        <p class="subtitle">{{ systemName }} - {{ versionName }}</p>
      </div>
    </div>

    <div class="changelog-list">
      <template v-if="changelogData">
        <mdui-card 
          v-for="(release, index) in changelogData.releases" 
          :key="release.date"
          class="changelog-card" 
          :variant="index === 0 ? 'filled' : 'elevated'"
        >
          <div class="card-header">
            <h3>更新 {{ release.date }} <span v-if="release.version">({{ release.version }})</span></h3>
            <mdui-chip v-if="index === 0" variant="filter" selected>最新</mdui-chip>
          </div>
          <mdui-divider></mdui-divider>
          <div class="card-body">
            <ul>
              <li v-for="(change, idx) in release.changes" :key="idx">{{ change }}</li>
            </ul>
          </div>
        </mdui-card>
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

.state-container {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.changelog-card {
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
  font-size: 1.1rem;
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
}

.card-body li:last-child {
  margin-bottom: 0;
}
</style>
