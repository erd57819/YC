<script setup>
import { ref } from 'vue'
import { useArticleStore } from '@/stores/articles' // articles 스토어 임포트

const title = ref('')
const content = ref('')

const articleStore = useArticleStore() // articles 스토어 사용

const createNewArticle = function () {
  const payload = {
    title: title.value,
    content: content.value
  }
  articleStore.createArticle(payload) // createArticle 함수 호출
}
</script>

<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createNewArticle">
      <label for="title">제목:</label>
      <input type="text" id="title" v-model.trim="title"><br>
      <label for="content">내용:</label>
      <textarea id="content" v-model.trim="content"></textarea><br>
      <input type="submit" value="작성">
    </form>
  </div>
</template>

<style scoped>

</style>