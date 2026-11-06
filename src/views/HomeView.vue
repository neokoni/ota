<template>
  <div class="home-container">
    <section class="hero">
      <m3e-heading class="hero-title" variant="display" size="large" level="1">
        NeoBuilds Changelog
      </m3e-heading>

      <p class="hero-description">
        查看Neokoni的ROM的更新记录
      </p>

      <div class="hero-actions">
        <m3e-button variant="filled" @click="router.push('/devices')">
          选择设备
          <m3e-icon slot="trailing-icon" name="arrow_forward"></m3e-icon>
        </m3e-button>
        <m3e-button
          variant="tonal"
          href="https://github.com/neokoni/ota_site"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
          <m3e-icon slot="trailing-icon" name="open_in_new"></m3e-icon>
        </m3e-button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.home-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 75vh;
  text-align: center;
}

.hero {
  max-width: 720px;
}

.hero-title {
  display: block;
  margin-bottom: 16px;
  color: var(--md-sys-color-primary);
}

.hero-description {
  margin: 0 0 32px;
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--md-sys-color-on-surface-variant);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

@media (max-width: 600px) {
  .hero-description {
    font-size: 1rem;
  }
}
</style>
