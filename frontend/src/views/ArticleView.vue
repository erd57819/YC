<template>
  <div class="article-view">
    <h1 class="mb-4">Articles</h1>
    <div v-if="store.articles.length > 0" class="row">
      <div v-for="article in store.articles" :key="article.id" class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ article.title }}</h5>
            <p class="card-text flex-grow-1">{{ truncateContent(article.content, 100) }}</p>
            <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="btn btn-primary mt-auto">View Details</RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info">
      No articles yet. Be the first to create one!
    </div>
    <RouterLink v-if="accountStore.isLogin" :to="{ name: 'CreateView' }" class="btn btn-success mt-3">
      <i class="bi bi-plus-circle-fill"></i> Create New Article
    </RouterLink>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const store = useArticleStore()
const accountStore = useAccountStore()

onMounted(() => {
  store.getArticles() //
})

const truncateContent = (content, maxLength) => {
  if (content.length <= maxLength) {
    return content;
  }
  return content.substring(0, maxLength) + '...';
}
</script>

<style scoped>
.card-title {
  font-weight: bold;
}
.card-text {
  color: #555;
}
.article-view {
  padding: 20px;
}
/* Bootstrap Icons CDN (만약 아이콘을 사용한다면 index.html에 추가하거나 npm으로 설치) */
/* @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"); */
</style>