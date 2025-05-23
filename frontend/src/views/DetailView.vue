<template>
  <div class="detail-view p-4" v-if="article">
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h2 class="mb-0">{{ article.title }}</h2>
        <div v-if="accountStore.user && accountStore.user.nickname === article.user_nickname">
          <button @click="goToEdit" class="btn btn-outline-secondary btn-sm me-2">Edit</button>
          <button @click="deleteArticle" class="btn btn-outline-danger btn-sm">Delete</button>
        </div>
      </div>
      <div class="card-body">
        <div class="text-muted mb-3">
          <span><strong>Author:</strong> {{ article.user_nickname }}</span> |
          <span><strong>Created:</strong> {{ new Date(article.created_at).toLocaleString() }}</span>
        </div>
        <hr>
        <div class="article-content py-3">
          {{ article.content }}
        </div>
      </div>
    </div>

    <div class="comments-section">
      <h4 class="mb-3">Comments ({{ article.comment_count }})</h4>
      <div v-if="article.comments && article.comments.length > 0">
        <div class="list-group">
          <div v-for="comment in article.comments" :key="comment.id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <p class="mb-1">{{ comment.content }}</p>
              <small class="text-muted">by {{ comment.user_nickname }}</small>
            </div>
            <button 
              v-if="accountStore.user && accountStore.user.nickname === comment.user_nickname"
              @click="handleDeleteComment(comment.id)" 
              class="btn btn-outline-danger btn-sm"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <div v-else class="alert alert-light">
        No comments yet. Be the first to comment!
      </div>
    </div>

    <div class="comment-form mt-4 card">
      <div class="card-body">
        <form @submit.prevent="submitComment">
          <div class="mb-3">
            <label for="commentContent" class="form-label">Leave a Comment</label>
            <textarea class="form-control" id="commentContent" v-model="newComment" rows="3" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Submit Comment</button>
        </form>
      </div>
    </div>

    <RouterLink :to="{ name: 'ArticleView' }" class="btn btn-secondary mt-4">Back to List</RouterLink>
  </div>

  <div v-else class="alert alert-info">
    Loading article details...
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; // onUnmounted 및 isMounted 관련 로직은 간소화 가능하여 제거
import { useRoute, useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { useAccountStore } from '@/stores/accounts';

const route = useRoute();
const router = useRouter();
const articleStore = useArticleStore();
const accountStore = useAccountStore();

const article = ref(null);
const newComment = ref('');
const articleId = route.params.id;

// 데이터 로드 함수
const loadArticle = async () => {
  const fetchedArticle = await articleStore.getArticleDetail(articleId);
  article.value = fetchedArticle;
  if (!fetchedArticle) {
    alert('Failed to load article details.');
    router.push({ name: 'ArticleView' });
  }
};

onMounted(() => {
  if (!accountStore.isLogin) {
    alert('Please log in to view article details.');
    router.push({ name: 'LogInView' });
    return;
  }
  // 스토어에 사용자 정보가 없을 경우 (예: 페이지 새로고침) 다시 가져옵니다.
  if (!accountStore.user) {
    accountStore.fetchUser();
  }
  loadArticle();
});

// 게시글 수정 페이지로 이동
const goToEdit = () => {
  // 수정 기능에 대한 라우터 이름이 'ArticleEditView'라고 가정합니다.
  // 실제 라우터 설정에 맞게 수정이 필요할 수 있습니다.
  router.push({ name: 'ArticleEditView', params: { id: articleId } });
};

// 게시글 삭제 함수
const deleteArticle = async () => {
  if (confirm('Are you sure you want to delete this article?')) {
    await articleStore.deleteArticle(articleId);
    router.push({ name: 'ArticleView' });
  }
};

// 댓글 작성 함수
const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('Comment content cannot be empty.');
    return;
  }
  await articleStore.createComment(articleId, { content: newComment.value });
  newComment.value = ''; // 입력창 초기화
  await loadArticle(); // 댓글 목록 새로고침
};

// [추가] 댓글 삭제 처리 함수
const handleDeleteComment = async (commentId) => {
  if (confirm('Are you sure you want to delete this comment?')) {
    await articleStore.deleteComment(commentId);
    await loadArticle(); // 댓글 목록 새로고침
  }
};
</script>

<style scoped>
.detail-view {
  max-width: 800px;
  margin: auto;
}
.article-content {
  white-space: pre-wrap;
  line-height: 1.6;
}
.comments-section {
  margin-top: 2rem;
}
</style>