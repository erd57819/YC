<template>
  <div class="board-wrapper">
    <div class="board-container">
      <div class="board-title-header">
        <h2>게시판</h2>
        <button 
          v-if="accountStore.isLogin" 
          @click="goToCreate" 
          class="btn btn-primary"
        >
          글쓰기
        </button>
      </div>
      
      <div class="date-filter-box">
        <span>2024-08-27 ~ 2024-05-01</span>
        <span class="dropdown-arrow">▼</span>
      </div>

      <div class="board-header">
        <div class="header-no">번호</div>
        <div class="header-nickname">닉네임</div>
        <div class="header-title">제목</div>
        <div class="header-date">날짜 및 시간</div>
      </div>

      <div class="article-list">
        <div
          v-for="(article, index) in store.articles"
          :key="article.id"
          class="article-item"
          @click="goToDetail(article.id)"
        >
          <div class="item-no">{{ formatNumber(store.articles.length - index) }}</div>
          <div class="item-nickname">{{ article.user_nickname }}</div>
          <div class="item-title">{{ article.title }}</div>
          <div class="item-date">{{ formatDate(article.created_at) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
// ▼▼▼▼▼ [추가] 로그인 상태를 확인하기 위해 account 스토어를 가져옵니다. ▼▼▼▼▼
import { useAccountStore } from '@/stores/accounts'

const store = useArticleStore()
const router = useRouter()
// ▼▼▼▼▼ [추가] account 스토어 인스턴스 생성 ▼▼▼▼▼
const accountStore = useAccountStore()

onMounted(() => {
  store.getArticles()
})

const goToDetail = (articleId) => {
  router.push({ name: 'DetailView', params: { id: articleId } })
}

// ▼▼▼▼▼ [추가] 글쓰기 페이지로 이동하는 함수 ▼▼▼▼▼
const goToCreate = () => {
  router.push({ name: 'CreateView' })
}

const formatNumber = (num) => {
  return num.toString().padStart(2, '0')
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear().toString().slice(-2)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const seconds = date.getSeconds().toString().padStart(2, '0')
  return `${year}.${month}.${day} ${hours}:${minutes}:${seconds}`
}
</script>

<style scoped>
/* 기존 스타일은 그대로 유지 */
.board-wrapper { background-color: #f4f6f9; padding: 40px 20px; display: flex; justify-content: center; min-height: calc(100vh - 56px); font-family: 'Pretendard', sans-serif; }
.board-container { background-color: white; padding: 30px 40px; border-radius: 12px; box-shadow: 0 6px 24px rgba(0, 0, 0, 0.07); width: 100%; max-width: 1100px; }

/* ▼▼▼▼▼ [추가] 제목과 버튼을 정렬하기 위한 스타일 ▼▼▼▼▼ */
.board-title-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

h2 {
  font-weight: 700;
  font-size: 28px;
  margin-bottom: 0; /* board-title-header 에서 margin을 관리하므로 0으로 변경 */
}
/* ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ */

.date-filter-box { border: 1px solid #dee2e6; padding: 8px 12px; border-radius: 6px; display: inline-block; margin-bottom: 30px; font-size: 14px; color: #495057; }
.dropdown-arrow { margin-left: 10px; color: #868e96; }
.board-header { display: grid; grid-template-columns: 80px 150px 1fr 180px; padding: 0 20px 15px 20px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #6c757d; font-size: 15px; text-align: center; }
.header-title { text-align: left; }
.article-list { margin-top: 10px; }
.article-item { display: grid; grid-template-columns: 80px 150px 1fr 180px; align-items: center; padding: 18px 20px; background-color: #ffffff; border: 1px solid #f1f3f5; border-radius: 8px; margin-bottom: 12px; transition: box-shadow 0.2s ease-in-out, transform 0.2s ease-in-out; }
.article-item:hover { cursor: pointer; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.item-no { color: #868e96; font-weight: 500; text-align: center; }
.item-nickname { text-align: center; font-weight: 500; }
.item-title { text-align: left; font-weight: 600; color: #343a40; }
.item-date { font-size: 14px; color: #868e96; text-align: center; }
</style>