<template>
  <div class="container mt-5">
    <h1>개시글 수정</h1>
    <form v-if="articleToEdit" @submit.prevent="submitUpdate">
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input type="text" class="form-control" id="title" v-model="formData.title" required>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea class="form-control" id="content" v-model="formData.content" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary me-2">수정완료</button>
      <button type="button" class="btn btn-secondary" @click="cancelEdit">취소</button>
    </form>
    <div v-else class="alert alert-info">
      Loading article data...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { useAccountStore } from '@/stores/accounts';

const route = useRoute();
const router = useRouter();
const articleStore = useArticleStore();
const accountStore = useAccountStore();

const articleId = route.params.id;
const articleToEdit = ref(null);
const formData = ref({
  title: '',
  content: ''
});

onMounted(async () => {
  if (!accountStore.isLogin) {
    alert('Please log in to edit articles.');
    router.push({ name: 'LogInView' });
    return;
  }

  const fetchedArticle = await articleStore.getArticleDetail(articleId);
  if (fetchedArticle) {
    if (accountStore.user && accountStore.user.nickname !== fetchedArticle.user_nickname) {
        alert('You are not authorized to edit this article.');
        console.log(articleId);
        router.push({ name: 'DetailView', params: { id: articleId } });
        return;
    }
    articleToEdit.value = fetchedArticle;
    formData.value.title = fetchedArticle.title;
    formData.value.content = fetchedArticle.content;
  } else {
    alert('Failed to load article for editing.');
    router.push({ name: 'ArticleView' });
  }
});

const submitUpdate = async () => {
  if (!formData.value.title.trim() || !formData.value.content.trim()) {
    alert('Title and content cannot be empty.');
    return;
  }
  const updatedArticle = await articleStore.updateArticle(articleId, formData.value);
  if (updatedArticle) {
  }
};

const cancelEdit = () => {
  router.push({ name: 'DetailView', params: { id: articleId } });
};
</script>

<style scoped>
/* 필요한 스타일 추가 */
</style>