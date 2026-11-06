<template>
  <div class="not-found-view">
    <div class="illustration">
      <img src="http://bili.apis.amethysty.dev/" alt="anime" class="anime-404" />
    </div>
    <div class="content">
      <m3e-heading variant="display" size="large" level="1" class="title">404</m3e-heading>
      <p class="description">哎呀呀, 找不到了喵。</p>
      <m3e-button variant="filled" @click="router.push('/')">
        主页
        <m3e-icon slot="trailing-icon" name="home"></m3e-icon>
      </m3e-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.not-found-view {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 60px;
  min-height: 70vh;
  padding: 24px 0;
}

.illustration {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.anime-404 {
  max-width: 30vw;
  height: auto;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.title {
  color: var(--md-sys-color-on-surface);
}

.description {
  margin: 16px 0 32px;
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--md-sys-color-on-surface-variant);
  max-width: 450px;
}

@media (max-width: 768px) {
  .not-found-view {
    flex-direction: column;
    gap: 32px;
    text-align: center;
  }

  .illustration {
    justify-content: center;
  }

  .anime-404 {
    max-width: 80vw;
  }

  .content {
    align-items: center;
    text-align: center;
  }
}
</style>
