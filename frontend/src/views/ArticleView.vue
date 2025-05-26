<template>
  <div class="board-wrapper">
    <div class="board-container">
      <div class="board-title-header">
        <h2>게시판</h2>
        <button 
          v-if="accountStore.isLogin" 
          @click="goToCreate" 
          class="btn btn-primary create-btn"
        >
          글쓰기
        </button>
      </div>
      
      <div class="date-filter-controls">
        <goods-vue
          v-model:startYear="startYear"
          v-model:startMonth="startMonth"
          v-model:endYear="endYear"
          v-model:endMonth="endMonth"
          :show-price-header="false" />
      </div>
      
      <div class="board-header">
        <div class="header-no">번호</div>
        <div class="header-nickname">닉네임</div>
        <div class="header-title">제목</div>
        <div class="header-date">날짜 및 시간</div>
      </div>

      <div v-if="isLoading" class="loading-message">
        <p>게시글을 불러오는 중입니다...</p>
      </div>
      <div v-else-if="filteredArticles.length > 0" class="article-list">
        <div
          v-for="(article, index) in filteredArticles" 
          :key="article.id"
          class="article-item"
          @click="goToDetail(article.id)"
        >
          <div class="item-no">{{ formatNumber(filteredArticles.length - index) }}</div>
          <div class="item-nickname">{{ article.user_nickname }}</div>
          <div class="item-title">{{ article.title }}</div>
          <div class="item-date">{{ formatDate(article.created_at) }}</div>
        </div>
      </div>
      <div v-else-if="!isLoading && attemptedFetch && store.articles.length > 0 && filteredArticles.length === 0" class="no-results-message">
        <p>선택하신 기간에 해당하는 게시글이 없습니다.</p>
      </div>
      <div v-else-if="!isLoading && store.articles.length === 0 && attemptedFetch" class="no-results-message">
        <p>게시글이 없습니다. 첫 번째 글을 작성해보세요!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// ... (ArticleView.vue의 script setup 부분은 이전 답변과 동일하게 유지) ...
import { ref, computed, onMounted, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { useAccountStore } from '@/stores/accounts';
import GoodsVue from '@/components/goods.vue';

const store = useArticleStore();
const router = useRouter();
const accountStore = useAccountStore();

const currentYear = new Date().getFullYear();
const currentMonth = new Date().getMonth() + 1;

const startYear = ref(currentYear); 
const startMonth = ref(1);
const endYear = ref(currentYear);
const endMonth = ref(currentMonth);

const filterStartDate = ref(new Date(startYear.value, startMonth.value - 1, 1));
const filterEndDate = ref(new Date(endYear.value, endMonth.value, 0, 23, 59, 59));

const isLoading = ref(false);
const attemptedFetch = ref(false);

watchEffect(() => {
  if (startYear.value && startMonth.value && endYear.value && endMonth.value) {
    const newStartDate = new Date(startYear.value, startMonth.value - 1, 1);
    const newEndDate = new Date(endYear.value, endMonth.value, 0, 23, 59, 59);

    if (newStartDate > newEndDate) {
        filterStartDate.value = newStartDate;
        filterEndDate.value = new Date(startYear.value, startMonth.value, 0, 23, 59, 59);
    } else {
        filterStartDate.value = newStartDate;
        filterEndDate.value = newEndDate;
    }
  }
});

const filteredArticles = computed(() => {
  if (!store.articles || store.articles.length === 0) {
    return [];
  }
  
  return store.articles.filter(article => {
    const articleDate = new Date(article.created_at);
    return articleDate >= filterStartDate.value && articleDate <= filterEndDate.value;
  }).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
});

onMounted(async () => {
  isLoading.value = true;
  attemptedFetch.value = true;
  try {
    await store.getArticles();
  } catch (error) {
    console.error("게시글 로딩 중 오류 발생:", error);
  } finally {
    isLoading.value = false;
  }
});

const goToDetail = (articleId) => {
  router.push({ name: 'DetailView', params: { id: articleId } });
};

const goToCreate = () => {
  router.push({ name: 'CreateView' });
};

const formatNumber = (num) => {
  return num.toString().padStart(2, '0');
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  const year = date.getFullYear().toString().slice(-2);
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');
  return `${year}.${month}.${day} ${hours}:${minutes}:${seconds}`;
};
</script>

<style scoped>
/* ArticleView.vue의 style 부분은 이전 답변과 동일하게 유지 */
.board-wrapper { background-color: #f4f6f9; padding: 40px 20px; display: flex; justify-content: center; min-height: calc(100vh - 56px); font-family: 'Pretendard', sans-serif; }
.board-container { background-color: white; padding: 30px 40px; border-radius: 12px; box-shadow: 0 6px 24px rgba(0, 0, 0, 0.07); width: 100%; max-width: 1100px; }

.board-title-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

h2 {
  font-weight: 700;
  font-size: 28px;
  margin-bottom: 0; 
}

.create-btn {
  font-size: 15px;
  padding: 8px 18px;
}

.date-filter-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.board-header { display: grid; grid-template-columns: 80px 150px 1fr 180px; padding: 0 20px 15px 20px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #6c757d; font-size: 15px; text-align: center; }
.header-title { text-align: left; }
.article-list { margin-top: 10px; }
.article-item { display: grid; grid-template-columns: 80px 150px 1fr 180px; align-items: center; padding: 18px 20px; background-color: #ffffff; border: 1px solid #f1f3f5; border-radius: 8px; margin-bottom: 12px; transition: box-shadow 0.2s ease-in-out, transform 0.2s ease-in-out; }
.article-item:hover { cursor: pointer; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
.item-no { color: #868e96; font-weight: 500; text-align: center; }
.item-nickname { text-align: center; font-weight: 500; }
.item-title { text-align: left; font-weight: 600; color: #343a40; }
.item-date { font-size: 14px; color: #868e96; text-align: center; }

.loading-message, .no-results-message {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
  font-size: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  margin-top: 1rem;
}
</style>