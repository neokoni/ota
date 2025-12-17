<template>
  <div class="device-selection-view">
    <h1 class="page-title">选择您的设备</h1>
    <div class="device-grid">
      <mdui-card 
        v-for="device in devices" 
        :key="device.codename"
        clickable 
        class="device-card" 
        @click="$router.push(`/device/${device.codename}`)"
      >
        <div class="device-info">
          <h3>{{ device.name }}</h3>
          <p>{{ device.codename }}</p>
        </div>
        <mdui-icon name="chevron_right--two-tone"></mdui-icon>
      </mdui-card>
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
  color: rgb(var(--mdui-color-on-surface));
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.device-card {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.device-info h3 {
  margin: 0 0 4px 0;
  font-size: 1.2rem;
}

.device-info p {
  margin: 0;
  opacity: 0.7;
  font-family: monospace;
}
</style>