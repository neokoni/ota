<script setup lang="ts">
</script>

<template>
  <div class="home">
    <mdui-card style="padding: 20px; margin: 20px;">
      <h1>Welcome to OTA Center</h1>
      <p>This is the home page.</p>
      <mdui-button @click="$router.push('/about')">Go to About</mdui-button>
    </mdui-card>
  </div>
</template>
