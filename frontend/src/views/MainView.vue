<template>
  <div class="main-container">
    <div v-if="!accountStore.isLogin" class="logged-out-view">
      <img src="@/assets/bonobono.png" alt="보노보노 캐릭터" class="character-image-large" />
      <h2 class="main-message">YC BANK</h2>
      <p class="sub-message">무엇을 도와드릴까요?</p>
    </div>

    <div v-else class="logged-in-view">
      <img src="@/assets/bonobono.png" alt="보노보노 캐릭터" class="character-image-large" />
      <h2 class="main-message" v-if="accountStore.user">
        {{ accountStore.user.nickname || accountStore.user.username }}님, YC BANK에 오신 것을 환영합니다!
      </h2>
      <p class="sub-message">다양한 금융 상품을 둘러보세요.</p>
      <p class="mt-3">
        <RouterLink :to="{ name: 'DepositProductsView' }" class="btn btn-info me-2">예금 상품 보기</RouterLink>
        <RouterLink :to="{ name: 'SavingProductsView' }" class="btn btn-info">적금 상품 보기</RouterLink>
      </p>
      <p class="mt-2" v-if="accountStore.isLogin">
        <RouterLink :to="{ name: 'AIRecommendationView' }" class="btn btn-outline-primary">AI 상품 추천 받아보기</RouterLink>
      </p>
    </div>
    
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';
import { RouterLink } from 'vue-router';
// import bonobonoImage from '@/assets/bonobono.png'; // 필요시

const accountStore = useAccountStore();

// MainView는 이제 AI 추천을 직접 다루지 않으므로, financialStore 관련 로직은 제거합니다.
</script>

<style scoped>
/* 스타일은 이전 답변과 유사하게 유지하되, AI 추천 관련 스타일은 AIRecommendationView.vue로 이동 */
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px); /* 예시: 헤더/푸터 높이 제외 */
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
}

.character-image-large {
  width: 500px;
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
}

.logged-out-view .main-message,
.logged-in-view .main-message {
  font-size: 2.2em;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.logged-out-view .sub-message,
.logged-in-view .sub-message {
  font-size: 1.1em;
  color: #555;
}

.logged-in-view {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>