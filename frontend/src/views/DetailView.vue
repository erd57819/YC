<template>
  <div class="detail-view" v-if="article">
    <h1 class="mb-3">{{ article.title }}</h1>
    <div class="card">
      <div class="card-body">
        <p class="card-text text-muted">Author: {{ article.user }}</p>
        <p class="card-text text-muted">Created: {{ new Date(article.created_at).toLocaleDateString() }}</p>
        <p class="card-text text-muted">Last Updated: {{ new Date(article.updated_at).toLocaleDateString() }}</p>
        <hr>
        <div class="article-content py-3">
          {{ article.content }}
        </div>
      </div>
    </div>
    <RouterLink :to="{ name: 'ArticleView' }" class="btn btn-secondary mt-4">Back to List</RouterLink>
  </div>
  <div v-else class="alert alert-warning">
    Loading article details or article not found.
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter() // router 사용
const article = ref(null)
const store = useArticleStore()
const accountStore = useAccountStore()

onMounted(async () => {
  const articleId = route.params.id
  if (!accountStore.token) { // 토큰이 없으면 로그인 페이지로
    alert('Please log in to view article details.')
    router.push({ name: 'LogInView' }) //
    return
  }
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/articles/${articleId}/`, //
      headers: {
        Authorization: `Token ${accountStore.token}` //
      }
    })
    article.value = response.data
  } catch (error) {
    console.error('Failed to fetch article:', error)
    if (error.response && error.response.status === 404) {
      alert('Article not found.')
      router.push({ name: 'ArticleView' }) //
    } else if (error.response && error.response.status === 401) {
        alert('Authentication credentials were not provided or are invalid.')
        router.push({ name: 'LogInView'})
    }
    else {
      alert('Error loading article details.')
    }
  }
})
</script>

<style scoped>
.detail-view {
  padding: 20px;
}
.article-content {
  white-space: pre-wrap; /* 줄바꿈과 공백을 유지하도록 설정 */
  line-height: 1.6;
}
.card {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>