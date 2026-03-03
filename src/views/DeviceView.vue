<template>
  <div class="device-view">
    <div class="md-card device-card">
      <div class="card-content">
        <h1>{{ deviceName }} ({{ codename }})</h1>
        <p>选择一个系统以查看可用版本。</p>

        <div class="system-list">
          <div
            v-for="system in systems"
            :key="system.name"
            class="md-card system-item"
            role="button"
            tabindex="0"
            @click="selectSystem(system.name)"
            @keydown.enter="selectSystem(system.name)"
          >
            <md-ripple></md-ripple>
            <div class="system-info">
              <h3>{{ system.name }}</h3>
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
import { getDevice } from '@/config/devices';

const route = useRoute();
const router = useRouter();
const codename = computed(() => route.params.codename as string);

const device = computed(() => getDevice(codename.value));
const deviceName = computed(() => device.value?.name || '未知设备');
const systems = computed(() => device.value?.systems || []);

function selectSystem(system: string) {
  router.push(`/device/${codename.value}/${system}`);
}
</script>

<style scoped>
.device-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.device-card {
  padding: 24px;
  width: 100%;
  background-color: var(--md-sys-color-surface-container-low);
  border-radius: 16px;
  border: 1px solid var(--md-sys-color-outline-variant);
}

.device-card h1 {
  color: var(--md-sys-color-on-surface);
  margin: 0 0 8px 0;
}

.device-card > .card-content > p {
  color: var(--md-sys-color-on-surface-variant);
  margin: 0 0 16px 0;
}

.system-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.system-item {
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
  transition: background-color 200ms ease, box-shadow 200ms ease;
  outline: none;
}

.system-item:hover {
  background-color: var(--md-sys-color-surface-variant);
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.system-item:focus-visible {
  outline: 3px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}

.system-info h3 {
  margin: 0;
  color: var(--md-sys-color-on-surface);
}

.chevron-icon {
  color: var(--md-sys-color-on-surface-variant);
}
</style>