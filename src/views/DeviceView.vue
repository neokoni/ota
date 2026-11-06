<template>
  <div class="device-view">
    <m3e-card variant="filled" class="hero-card">
      <div slot="content">
        <div class="hero-content">
          <span class="device-icon">
            <m3e-icon name="devices"></m3e-icon>
          </span>
          <div class="device-heading">
            <m3e-heading variant="headline" size="small" level="1">{{ deviceName }}</m3e-heading>
            <span class="device-codename">{{ codename }}</span>
          </div>
        </div>
        <p class="hero-hint">选择一个系统以查看可用版本。</p>
      </div>
    </m3e-card>

    <m3e-action-list variant="segmented" class="system-list" aria-label="系统列表">
      <m3e-list-action
        v-for="system in systems"
        :key="system.name"
        @click="selectSystem(system.name)"
      >
        <m3e-icon slot="leading" name="deployed_code"></m3e-icon>
        {{ system.name }}
        <span slot="supporting-text">{{ system.versions.length }} 个版本</span>
        <m3e-icon slot="trailing" name="chevron_right"></m3e-icon>
      </m3e-list-action>
    </m3e-action-list>

    <div v-if="!systems.length" class="empty-state">
      <m3e-icon name="deployed_code"></m3e-icon>
      <p>该设备暂未配置任何系统。</p>
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
  void router.push(`/device/${codename.value}/${system}`);
}
</script>

<style scoped>
.device-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-top: 8px;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.device-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  flex-shrink: 0;
  border-radius: 18px;
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  --m3e-icon-size: 30px;
}

.device-heading {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.device-codename {
  font-family: ui-monospace, 'SFMono-Regular', Menlo, monospace;
  color: var(--md-sys-color-on-surface-variant);
}

.hero-hint {
  margin-top: 12px;
  color: var(--md-sys-color-on-surface-variant);
}

.system-list {
  --m3e-segmented-list-item-container-color: var(--md-sys-color-surface-container-high);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 16px;
  color: var(--md-sys-color-on-surface-variant);
  --m3e-icon-size: 40px;
}

.empty-state p {
  margin: 0;
}
</style>
