<script setup lang="ts">
</script>

<template>
  <div class="home-container">
    <div class="hero-section">
      <h1 class="hero-title">Neokoni's OTA Center</h1>
      <p class="hero-description">
        您的一站式设备更新与变更日志中心。
        简单、快速、可靠。
      </p>
      <div class="hero-actions">
        <mdui-button variant="filled" end-icon="arrow_forward--two-tone" @click="$router.push('/devices')">选择设备</mdui-button>
        <mdui-button variant="text" end-icon="open_in_new--two-tone" href="https://github.com/neokoni/ota_site" target="_blank">GitHub</mdui-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  padding: 20px;
}

.hero-section {
  max-width: 800px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: rgb(var(--mdui-color-primary));
}

.hero-description {
  font-size: 1.2rem;
  color: rgb(var(--mdui-color-on-surface-variant));
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>
