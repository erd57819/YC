<template>
  <div class="detail-view p-4" v-if="article">
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h2 class="mb-0">{{ article.title }}</h2>
        <div v-if="accountStore.user && accountStore.user.nickname === article.user_nickname">
          <button @click="goToEdit" class="btn btn-outline-secondary btn-sm me-2">Edit</button>
          <button @click="handleDeleteArticle" class="btn btn-outline-danger btn-sm">Delete</button>
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
        <form @submit.prevent="handleSubmitComment">
          <div class="mb-3">
            <label for="commentContent" class="form-label">Leave a Comment</label>
            <textarea class="form-control" id="commentContent" v-model="newCommentContent" rows="3" required></textarea>
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { useAccountStore } from '@/stores/accounts';

const route = useRoute();
const router = useRouter();
const articleStore = useArticleStore();
const accountStore = useAccountStore();

const article = ref(null);
const newCommentContent = ref(''); // 변수명 변경: newComment -> newCommentContent (가독성)
const articleId = route.params.id;

// 데이터 로드 함수 (게시글)
const loadArticleDetail = async () => {
  const fetchedArticle = await articleStore.getArticleDetail(articleId);
  if (fetchedArticle) {
    article.value = fetchedArticle;
  } else {
    alert('Failed to load article details.');
    router.push({ name: 'ArticleView' });
  }
};

// 컴포넌트 마운트 시 실행될 초기화 로직
onMounted(async () => {
  if (!accountStore.isLogin) {
    alert('Please log in to view article details.');
    router.push({ name: 'LogInView' });
    return;
  }

  // 스토어에 사용자 정보가 없을 경우 (예: 페이지 새로고침) 다시 가져옵니다.
  // fetchUser는 비동기이므로 await를 사용하여 완료를 기다립니다.
  if (!accountStore.user) {
    await accountStore.fetchUser();
  }
  
  // 게시글 상세 정보 로드
  await loadArticleDetail();
});

// 게시글 수정 페이지로 이동 함수
const goToEdit = () => {
  // 'ArticleEditView'는 실제 라우터에 정의된 이름이어야 합니다.
  router.push({ name: 'ArticleEditView', params: { id: articleId } });
};

// 게시글 삭제 처리 함수 (함수명 일관성: deleteArticle -> handleDeleteArticle)
const handleDeleteArticle = async () => {
  if (confirm('Are you sure you want to delete this article?')) {
    await articleStore.deleteArticle(articleId);
    router.push({ name: 'ArticleView' });
  }
};

// 댓글 작성 처리 함수 (함수명 일관성: submitComment -> handleSubmitComment)
const handleSubmitComment = async () => {
  if (!newCommentContent.value.trim()) {
    alert('Comment content cannot be empty.');
    return;
  }
  await articleStore.createComment(articleId, { content: newCommentContent.value });
  newCommentContent.value = ''; // 입력창 초기화
  await loadArticleDetail(); // 댓글 목록 포함, 게시글 전체 정보 새로고침
};

// 댓글 삭제 처리 함수
const handleDeleteComment = async (commentId) => {
  if (confirm('Are you sure you want to delete this comment?')) {
    await articleStore.deleteComment(commentId);
    await loadArticleDetail(); // 댓글 목록 포함, 게시글 전체 정보 새로고침
  }
};
</script>

<style scoped>
.detail-view {
  max-width: 800px;
  margin: auto;
}
.article-content {
  white-space: pre-wrap; /* 줄바꿈 및 공백 유지 */
  line-height: 1.6;
}
.comments-section {
  margin-top: 2rem;
}
</style>