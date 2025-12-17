<template>
  <div class="system-view">
    <mdui-card class="system-card" variant="filled">
      <div class="card-content">
        <div class="header">
          <mdui-button-icon icon="arrow_back--two-tone" @click="$router.back()"></mdui-button-icon>
          <h1>{{ systemName }} for {{ deviceName }}</h1>
        </div>
        <p>选择一个版本以查看更新日志。</p>
        
        <div class="version-list">
          <mdui-card 
            v-for="version in versions"
            :key="version.version"
            clickable 
            class="version-item" 
            variant="elevated" 
            @click="selectVersion(version.version)"
          >
            <div class="version-info">
              <h3>{{ version.version }}</h3>
              <p>{{ version.label }}</p>
            </div>
            <mdui-icon name="chevron_right--two-tone"></mdui-icon>
          </mdui-card>
        </div>
      </div>
    </mdui-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getDevice, getSystem } from '@/config/devices';

const route = useRoute();
const router = useRouter();
const codename = computed(() => route.params.codename as string);
const systemName = computed(() => route.params.system as string);

const device = computed(() => getDevice(codename.value));
const deviceName = computed(() => device.value?.name || codename.value);

const system = computed(() => getSystem(codename.value, systemName.value));
const versions = computed(() => system.value?.versions || []);

function selectVersion(version: string) {
  router.push(`/device/${codename.value}/${systemName.value}/${version}`);
}
</script>

<style scoped>
.system-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.system-card {
  padding: 24px;
  width: 100%;
}

.header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.version-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.version-item {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.version-info h3 {
  margin: 0 0 4px 0;
}

.version-info p {
  margin: 0;
  opacity: 0.7;
}
</style>