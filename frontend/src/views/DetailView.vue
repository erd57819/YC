<template>
  <div class="detail-wrapper">
    <div v-if="article" class="detail-container">
      <h3 class="page-header">게시판 상세</h3>
      
      <div class="article-main">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span>작성자: {{ article.user_nickname }}</span>
          <span class="meta-separator">|</span>
          <span>작성일: {{ formatDate(article.created_at, 'date') }}</span>
        </div>
        <hr class="divider" />
        <div class="article-content">
          <p>{{ article.content }}</p>
        </div>
      </div>
      
      <div v-if="isAuthor" class="article-actions">
        <button @click="goToEdit" class="btn btn-outline-secondary">수정</button>
        <button @click="deletePost" class="btn btn-outline-danger">삭제</button>
      </div>

      <div class="comments-section">
        <hr class="divider" />
        <h4 class="comments-title">댓글 ({{ article.comment_count }})</h4>
        
        <div class="comment-list">
          <div v-for="comment in article.comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user_nickname }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at, 'datetime') }}</span>
            </div>
            <div class="comment-body">
              <p class="comment-content">{{ comment.content }}</p>
              <button 
                v-if="accountStore.user && accountStore.user.id === comment.user"
                @click="removeComment(comment.id)" 
                class="btn-delete-comment"
              >
                삭제
              </button>
            </div>
          </div>
          <div v-if="article.comment_count === 0" class="no-comments">
            아직 댓글이 없습니다.
          </div>
        </div>
        
        <form @submit.prevent="submitComment" v-if="accountStore.isLogin" class="comment-form">
          <textarea 
            v-model.trim="newComment"
            class="form-control" 
            rows="3" 
            placeholder="댓글을 입력하세요..."
            required
          ></textarea>
          <button type="submit" class="btn btn-dark btn-submit-comment">댓글 등록</button>
        </form>
      </div>

    </div>
    
    <div v-else class="loading-wrapper">
      <p>게시글을 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()
const accountStore = useAccountStore()

const article = ref(null)
const newComment = ref('')
const articleId = route.params.id

// 데이터 새로고침 함수
const refreshArticle = async () => {
  article.value = await articleStore.getArticleDetail(articleId)
}

onMounted(() => {
  refreshArticle()
})

const isAuthor = computed(() => {
  if (!accountStore.user || !article.value) return false
  return accountStore.user.id === article.value.user
})

// 날짜 포맷 함수 (용도에 따라 'date' 또는 'datetime'으로 포맷)
const formatDate = (dateString, type) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const yyyy = date.getFullYear()
  const mm = (date.getMonth() + 1).toString().padStart(2, '0')
  const dd = date.getDate().toString().padStart(2, '0')
  
  if (type === 'date') {
    return `${yyyy}-${mm}-${dd}`
  } else {
    const hh = date.getHours().toString().padStart(2, '0')
    const mi = date.getMinutes().toString().padStart(2, '0')
    return `${yyyy}-${mm}-${dd} ${hh}:${mi}`
  }
}

const goToEdit = () => {
  router.push({ name: 'ArticleEditView', params: { id: articleId } })
}

const deletePost = async () => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    await articleStore.deleteArticle(articleId)
    router.push({ name: 'ArticleView' })
  }
}

// 댓글 작성 로직
const submitComment = async () => {
  if (!newComment.value) {
    alert('댓글 내용을 입력해주세요.')
    return
  }
  await articleStore.createComment(articleId, { content: newComment.value })
  newComment.value = '' // 입력창 초기화
  await refreshArticle() // 댓글 목록 새로고침
}

// 댓글 삭제 로직
const removeComment = async (commentId) => {
  if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    await articleStore.deleteComment(commentId)
    await refreshArticle() // 댓글 목록 새로고침
  }
}
</script>

<style scoped>
/* 기존 스타일은 유지 */
.detail-wrapper { background-color: #f8f9fa; padding: 50px 20px; display: flex; justify-content: center; min-height: calc(100vh - 56px); }
.detail-container { background-color: white; padding: 40px 50px; border-radius: 8px; width: 100%; max-width: 950px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); }
.page-header { font-size: 22px; font-weight: 600; color: #343a40; margin-bottom: 25px; }
.article-main { padding: 20px 0; }
.article-title { font-size: 34px; font-weight: 700; margin-bottom: 16px; text-align: center; color: #212529; }
.article-meta { font-size: 14px; color: #868e96; text-align: center; margin-bottom: 25px; }
.meta-separator { margin: 0 8px; }
.divider { border: 0; border-top: 1px solid #e9ecef; margin: 40px 0; }
.article-content p { font-size: 17px; line-height: 1.8; color: #343a40; white-space: pre-wrap; word-break: break-word; }
.article-actions { margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px; }

/* ▼▼▼▼▼ 댓글 섹션 스타일 (추가) ▼▼▼▼▼ */
.comments-section {
  margin-top: 30px;
}

.comments-title {
  font-size: 20px;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 20px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 댓글 아이템 사이의 간격 */
}

.comment-item {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  font-size: 15px;
}

.comment-date {
  font-size: 13px;
  color: #868e96;
}

.comment-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-content {
  margin: 0;
  color: #495057;
  font-size: 15px;
  line-height: 1.6;
}

.btn-delete-comment {
  background: none;
  border: none;
  color: #868e96;
  font-size: 13px;
  cursor: pointer;
  padding: 5px;
}
.btn-delete-comment:hover {
  color: #dc3545;
  text-decoration: underline;
}

.no-comments {
  text-align: center;
  color: #868e96;
  padding: 30px 0;
}

/* 댓글 작성 폼 */
.comment-form {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-form textarea {
  resize: none;
  font-size: 15px;
}

.btn-submit-comment {
  align-self: flex-end; /* 버튼을 오른쪽으로 정렬 */
  padding: 8px 20px;
}
</style>