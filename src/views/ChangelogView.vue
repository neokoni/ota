<template>
  <div class="changelog-view">
    <div class="header-section">
      <mdui-button-icon icon="arrow_back--two-tone" @click="$router.back()"></mdui-button-icon>
      <div>
        <h1>{{ deviceName }}</h1>
        <a :href="changelogUrl" target="_blank" class="json-link">查看更新日志文件</a>
        <p class="subtitle">{{ systemName }} - {{ versionName }}</p>
      </div>
    </div>

    <div class="changelog-list">
      <div v-if="loading" class="state-container">
        <mdui-circular-progress></mdui-circular-progress>
      </div>
      
      <div v-else-if="error" class="state-container">
        <p>{{ error }}</p>
      </div>

      <template v-else-if="changelogData">
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getDevice, getSystem } from '@/config/devices';

interface Release {
  date: string;
  version?: string;
  changes: string[];
}

interface ChangelogData {
  device: string;
  codename: string;
  system: string;
  releases: Release[];
}

const route = useRoute();
const codename = computed(() => route.params.codename as string);
const systemName = computed(() => route.params.system as string);
const versionName = computed(() => route.params.version as string);

const device = computed(() => getDevice(codename.value));
const deviceName = computed(() => device.value?.name || codename.value);

const system = computed(() => getSystem(codename.value, systemName.value));
const versionConfig = computed(() => system.value?.versions.find(v => v.version === versionName.value));

const changelogUrl = computed(() => versionConfig.value?.changelogJsonUrl || '#');

const changelogData = ref<ChangelogData | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const fetchChangelog = async () => {
  if (!changelogUrl.value || changelogUrl.value === '#') return;
  
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(changelogUrl.value);
    if (!response.ok) throw new Error('Failed to load changelog');
    const data = await response.json();
    // Sort releases by date descending
    if (data.releases) {
      data.releases.sort((a: Release, b: Release) => new Date(b.date).getTime() - new Date(a.date).getTime());
    }
    changelogData.value = data;
  } catch (e) {
    error.value = '无法加载更新日志';
    console.error(e);
  } finally {
    loading.value = false;
  }
};

watch(() => changelogUrl.value, fetchChangelog, { immediate: true });
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
