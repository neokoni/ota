<template>
  <div class="device-selection-view">
    <header class="page-header">
      <m3e-heading variant="headline" size="medium" level="1">选择您的设备</m3e-heading>
      <p>选择设备代号以查看可用的系统版本。</p>
    </header>

    <div class="device-grid">
      <m3e-card
        v-for="device in devices"
        :key="device.codename"
        variant="filled"
        actionable
        role="button"
        tabindex="0"
        class="device-card"
        @click="openDevice(device.codename)"
        @keydown.enter.prevent="openDevice(device.codename)"
        @keydown.space.prevent="openDevice(device.codename)"
      >
        <div slot="content" class="device-content">
          <span class="device-icon">
            <m3e-icon name="devices"></m3e-icon>
          </span>
          <div class="device-meta">
            <m3e-heading variant="title" size="medium">{{ device.name }}</m3e-heading>
            <span class="device-codename">{{ device.codename }}</span>
          </div>
          <m3e-icon class="chevron" name="chevron_right"></m3e-icon>
        </div>
      </m3e-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { devices } from '@/config/devices';

const router = useRouter();

function openDevice(codename: string) {
  void router.push(`/device/${codename}`);
}
</script>

<style scoped>
.device-selection-view {
  padding-top: 8px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header p {
  margin: 8px 0 0;
  color: var(--md-sys-color-on-surface-variant);
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.device-card {
  cursor: pointer;
}

.device-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.device-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 16px;
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  --m3e-icon-size: 26px;
}

.device-meta {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  gap: 4px;
}

.device-codename {
  font-family: ui-monospace, 'SFMono-Regular', Menlo, monospace;
  color: var(--md-sys-color-on-surface-variant);
}

.chevron {
  color: var(--md-sys-color-on-surface-variant);
}

@media (max-width: 600px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
}
</style>
