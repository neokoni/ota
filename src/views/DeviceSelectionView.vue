<template>
  <div class="device-selection-view">
    <h1 class="page-title">选择您的设备</h1>
    <div class="device-grid">
      <div
        v-for="device in devices"
        :key="device.codename"
        class="device-card md-card"
        @click="$router.push(`/device/${device.codename}`)"
        role="button"
        tabindex="0"
        @keydown.enter="$router.push(`/device/${device.codename}`)"
      >
        <md-ripple></md-ripple>
        <div class="device-info">
          <h3>{{ device.name }}</h3>
          <p>{{ device.codename }}</p>
        </div>
        <md-icon class="chevron-icon">chevron_right</md-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { devices } from '@/config/devices';
</script>

<style scoped>
.device-selection-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 24px;
  color: var(--md-sys-color-on-surface);
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

@media (max-width: 600px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
}

.device-card {
  position: relative;
  overflow: hidden;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  border-radius: 12px;
  background-color: var(--md-sys-color-surface-container-low);
  border: 1px solid var(--md-sys-color-outline-variant);
  transition: background-color 200ms ease;
  outline: none;
}

.device-card:hover {
  background-color: var(--md-sys-color-surface-container);
}

.device-card:focus-visible {
  outline: 3px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}

.device-info h3 {
  margin: 0 0 4px 0;
  font-size: 1.2rem;
  color: var(--md-sys-color-on-surface);
}

.device-info p {
  margin: 0;
  color: var(--md-sys-color-on-surface-variant);
  font-family: monospace;
}

.chevron-icon {
  color: var(--md-sys-color-on-surface-variant);
}
</style>