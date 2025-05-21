<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/articles'
import { RouterLink } from 'vue-router' // RouterLink 임포트

const articleStore = useArticleStore()

// 컴포넌트가 마운트될 때 게시글 목록을 가져옵니다.
onMounted(() => {
  articleStore.getArticles()
})
</script>

<template>
  <div>
    <h1>게시글 목록</h1>
    <div v-if="articleStore.articles.length > 0">
      <div v-for="article in articleStore.articles" :key="article.id">
        <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }">
          <h3>{{ article.title }}</h3>
          <p>{{ article.content }}</p>
        </RouterLink>
        <hr>
      </div>
    </div>
    <div v-else>
      <p>아직 작성된 게시글이 없습니다.</p>
    </div>
  </div>
</template>

<style scoped>
/* 필요한 스타일 추가 */
</style>