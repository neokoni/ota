<script setup lang="ts">
</script>

<template>
  <div class="home-container">
    <div class="hero-section">
      <h1 class="hero-title">Neokoni's OTA Center</h1>
      <p class="hero-description">
        Self hosted OTA info site for
        Neokoni's ROM builds.
      </p>
      <div class="hero-actions">
        <md-filled-button trailing-icon @click="$router.push('/devices')">
          选择设备
          <md-icon slot="icon">arrow_forward</md-icon>
        </md-filled-button>
        <md-text-button trailing-icon href="https://github.com/neokoni/ota_site" target="_blank">
          GitHub
          <md-icon slot="icon">open_in_new</md-icon>
        </md-text-button>
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
  color: var(--md-sys-color-primary);
}

.hero-description {
  font-size: 1.2rem;
  color: var(--md-sys-color-on-surface-variant);
  margin-bottom: 2rem;
  line-height: 1.6;
}

@media (max-width: 840px) {
  .hero-title {
    font-size: 2rem;
  }
}

@media (max-width: 600px) {
  .hero-title {
    font-size: 1.75rem;
  }

  .hero-description {
    font-size: 1rem;
  }
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
