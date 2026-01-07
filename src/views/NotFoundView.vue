<template>
  <div class="not-found-view">
    <div class="container">
      <div class="illustration">
        <img src="http://bili.apis.amethysty.dev/" alt="anime" class="anime-404" />
      </div>
      <div class="content">
        <h1 class="title">404</h1>
        <p class="description">
          哎呀呀, 找不到了喵。
        </p>
        <mdui-button variant="filled" @click="$router.push('/')">主页</mdui-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.anime-404 {
  max-width: 30vw;
  height: auto;
}

.container {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 60px;
  max-width: 1000px;
  width: 100%;
}

.illustration {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.content {
  flex: 1;
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.title {
  font-size: 8rem;
  font-weight: 700;
  margin: 0;
  line-height: 1;
  color: rgb(var(--mdui-color-on-surface));
}

.description {
  margin: 24px 0 32px;
  font-size: 1.1rem;
  line-height: 1.6;
  color: rgb(var(--mdui-color-on-surface-variant));
  max-width: 450px;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    text-align: center;
    gap: 32px;
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

  .title {
    font-size: 6rem;
  }
}
</style>
