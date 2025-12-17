<template>
  <div class="device-view">
    <mdui-card class="device-card" variant="filled">
      <div class="card-content">
        <h1>{{ deviceName }} ({{ codename }})</h1>
        <p>选择一个系统以查看可用版本。</p>
        
        <div class="system-list">
          <mdui-card 
            v-for="system in systems"
            :key="system.name"
            clickable 
            class="system-item" 
            variant="elevated" 
            @click="selectSystem(system.name)"
          >
            <div class="system-info">
              <h3>{{ system.name }}</h3>
              <p>基于 Android</p>
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
}

.system-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.system-item {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.system-info h3 {
  margin: 0 0 4px 0;
}

.system-info p {
  margin: 0;
  opacity: 0.7;
}
</style>