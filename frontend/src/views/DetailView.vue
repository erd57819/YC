<template>
  <div class="detail-view p-4" v-if="article">
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h2 class="mb-0">{{ article.title }}</h2>
        <div v-if="accountStore.user?.username === article.user_nickname">
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
          <div v-for="comment in article.comments" :key="comment.id" class="list-group-item">
            <p class="mb-1">{{ comment.content }}</p>
            <small class="text-muted">by {{ comment.user_nickname }}</small>
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
import { ref, onMounted, onUnmounted } from 'vue'; // ★ 1. onUnmounted를 import 합니다.
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

// ★ 2. 컴포넌트가 현재 화면에 존재하는지 상태를 추적하는 변수를 추가합니다.
let isMounted = false;

// 데이터 로드 함수
const loadArticle = async () => {
  const fetchedArticle = await articleStore.getArticleDetail(articleId);
  
  // ★ 4. API 응답이 왔을 때, 컴포넌트가 여전히 화면에 있는지 확인합니다.
  if (isMounted && fetchedArticle) {
    // 화면에 있을 때만 데이터를 업데이트합니다.
    article.value = fetchedArticle;
  } else if (isMounted && !fetchedArticle) {
    alert('Failed to load article details.');
    router.push({ name: 'ArticleView' });
  }
};

onMounted(() => {
  // ★ 3. 컴포넌트가 화면에 마운트(표시)되면 상태를 true로 변경합니다.
  isMounted = true;
  if (!accountStore.isLogin) {
    alert('Please log in to view article details.');
    router.push({ name: 'LogInView' });
    return;
  }
  loadArticle();
});

// ★ 5. 컴포넌트가 화면에서 사라지기 직전에 실행됩니다.
onUnmounted(() => {
  // 컴포넌트가 사라지면 상태를 false로 변경합니다.
  isMounted = false; 
});


// --- 아래 함수들은 기존과 동일합니다 ---

// 게시글 수정 페이지로 이동
const goToEdit = () => {
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