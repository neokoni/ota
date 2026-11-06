<template>
  <div class="system-view">
    <m3e-card variant="filled" class="hero-card">
      <div slot="content">
        <div class="hero-content">
          <m3e-icon-button aria-label="返回设备" @click="router.back()">
            <m3e-icon name="arrow_back"></m3e-icon>
          </m3e-icon-button>
          <div class="hero-heading">
            <m3e-heading variant="headline" size="small" level="1">{{ systemName }}</m3e-heading>
            <span class="subtitle">{{ deviceName }}</span>
          </div>
        </div>
        <p class="hero-hint">选择一个版本以查看更新日志。</p>
      </div>
    </m3e-card>

    <m3e-action-list variant="segmented" class="version-list" aria-label="版本列表">
      <m3e-list-action
        v-for="version in versions"
        :key="version.version"
        @click="selectVersion(version.version)"
      >
        <m3e-icon slot="leading" name="history"></m3e-icon>
        {{ version.version }}
        <span slot="supporting-text">{{ version.label }}</span>
        <m3e-icon slot="trailing" name="chevron_right"></m3e-icon>
      </m3e-list-action>
    </m3e-action-list>

    <div v-if="!versions.length" class="empty-state">
      <m3e-icon name="history"></m3e-icon>
      <p>该设备暂未配置任何版本。</p>
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
  void router.push(`/device/${codename.value}/${systemName.value}/${version}`);
}
</script>

<style scoped>
.system-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-top: 8px;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hero-heading {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.subtitle {
  color: var(--md-sys-color-on-surface-variant);
}

.hero-hint {
  margin-top: 12px;
  color: var(--md-sys-color-on-surface-variant);
}

.version-list {
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
