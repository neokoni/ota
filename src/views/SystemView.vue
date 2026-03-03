<template>
  <div class="system-view">
    <div class="md-card system-card">
      <div class="card-content">
        <div class="header">
          <md-icon-button @click="$router.back()">
            <md-icon>arrow_back</md-icon>
          </md-icon-button>
          <h1>{{ systemName }} for {{ deviceName }}</h1>
        </div>
        <p>选择一个版本以查看更新日志。</p>

        <div class="version-list">
          <div
            v-for="version in versions"
            :key="version.version"
            class="md-card version-item"
            role="button"
            tabindex="0"
            @click="selectVersion(version.version)"
            @keydown.enter="selectVersion(version.version)"
          >
            <md-ripple></md-ripple>
            <div class="version-info">
              <h3>{{ version.version }}</h3>
              <p>{{ version.label }}</p>
            </div>
            <md-icon class="chevron-icon">chevron_right</md-icon>
          </div>
        </div>
      </div>
    </div>
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
  box-sizing: border-box;
  background-color: var(--md-sys-color-surface-container-low);
  border-radius: 16px;
  border: 1px solid var(--md-sys-color-outline-variant);
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
  color: var(--md-sys-color-on-surface);
}

.system-card > .card-content > p {
  color: var(--md-sys-color-on-surface-variant);
  margin: 0 0 16px 0;
}

.version-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.version-item {
  position: relative;
  overflow: hidden;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  border-radius: 12px;
  background-color: var(--md-sys-color-surface-container-highest);
  border: 1px solid var(--md-sys-color-outline-variant);
  transition: background-color 200ms ease;
  outline: none;
}

.version-item:hover {
  background-color: var(--md-sys-color-surface-variant);
}

.version-item:focus-visible {
  outline: 3px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}

.version-info h3 {
  margin: 0 0 4px 0;
  color: var(--md-sys-color-on-surface);
}

.version-info p {
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
}

.chevron-icon {
  color: var(--md-sys-color-on-surface-variant);
}

@media (max-width: 600px) {
  .system-view {
    padding: 12px;
  }

  .system-card {
    padding: 16px;
  }
}
</style>