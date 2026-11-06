<template>
  <div class="changelog-view">
    <m3e-card variant="filled" class="hero-card">
      <div slot="content">
        <div class="hero-content">
          <m3e-icon-button aria-label="返回版本列表" @click="router.back()">
            <m3e-icon name="arrow_back"></m3e-icon>
          </m3e-icon-button>
          <div class="hero-heading">
            <m3e-heading variant="headline" size="small" level="1">{{ deviceName }}</m3e-heading>
            <span class="subtitle">{{ systemName }} · {{ versionName }}</span>
          </div>
        </div>
        <div v-if="otaUrl" class="hero-actions">
          <m3e-button
            variant="tonal"
            :href="otaUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            查看系统更新文件 (JSON)
            <m3e-icon slot="trailing-icon" name="system_update_alt"></m3e-icon>
          </m3e-button>
        </div>
      </div>
    </m3e-card>

    <div v-if="changelogData" class="changelog-list">
      <m3e-card
        v-for="(release, index) in changelogData.releases"
        :key="release.date"
        :variant="index === 0 ? 'filled' : 'outlined'"
        class="release-card"
      >
        <div slot="header" class="release-header">
          <m3e-heading variant="title" size="medium">{{ release.date }}</m3e-heading>
          <m3e-chip v-if="index === 0" variant="elevated">
            <m3e-icon slot="icon" name="check_circle"></m3e-icon>
            最新
          </m3e-chip>
        </div>
        <ul slot="content" class="release-list">
          <li v-for="(change, idx) in release.changes" :key="idx" v-html="change"></li>
        </ul>
      </m3e-card>
    </div>

    <div v-else class="empty-state">
      <m3e-icon name="history"></m3e-icon>
      <p>未找到更新日志</p>
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
const versionName = computed(() => route.params.version as string);

const device = computed(() => getDevice(codename.value));
const deviceName = computed(() => device.value?.name || codename.value);

const system = computed(() => getSystem(codename.value, systemName.value));
const versionConfig = computed(() => system.value?.versions.find(v => v.version === versionName.value));
const otaUrl = computed(() => versionConfig.value?.otaUrl);

const changelogData = computed(() => {
  if (!versionConfig.value) return null;
  // Sort releases by date descending
  const releases = [...(versionConfig.value.releases || [])];
  releases.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  return { releases };
});
</script>

<style scoped>
.changelog-view {
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

.hero-actions {
  margin-top: 16px;
}

.changelog-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.release-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.release-list {
  margin: 0;
  padding-left: 20px;
  line-height: 1.6;
}

.release-list li {
  margin-bottom: 8px;
}

.release-list li:last-child {
  margin-bottom: 0;
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
