<template>
  <div class="ai-recommendation-container my-5">
    <div class="text-center mb-5">
      <img src="@/assets/bonobono.png" alt="AI 추천 캐릭터" class="character-image-page" />
      <h1 class="display-5 fw-bold mt-3">AI 맞춤 상품 추천</h1>
      <p class="lead text-muted">
        {{ accountStore.user?.nickname || '회원' }}님의 금융 프로필과 시장 상황을 고려하여,
        YC BANK AI가 최적의 상품을 추천해 드립니다.
      </p>
    </div>

    <div v-if="!accountStore.isLogin" class="alert alert-warning text-center">
      <p class="mb-0">AI 상품 추천을 받으시려면 <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>이 필요합니다.</p>
    </div>

    <div v-else>
      <div v-if="isLoadingRecommendations" class="loading-message text-center">
        <p>AI가 {{ accountStore.user?.nickname || '회원' }}님을 위한 맞춤 상품을 분석 중입니다...</p>
        <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="financialStore.recommendedProducts && financialStore.recommendedProducts.length > 0" class="recommendation-list-page">
        <div v-for="(product, index) in financialStore.recommendedProducts" :key="product.id || index" class="card recommendation-card shadow-sm mb-4">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">추천 {{ index + 1 }}</h5>
          </div>
          <div class="card-body">
            <h4 class="card-title product-name-page">
              ({{ getProductType(product.product_type) }}) {{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}
            </h4>
            <p class="card-text product-rate-page" v-if="product.max_rate != null">
              <strong>최고 연 {{ product.max_rate.toFixed(2) }}%</strong>
            </p>
            <p class="card-text recommendation-reason-page" v-if="product.recommendation_reason">
              <strong>AI 추천 이유:</strong> {{ product.recommendation_reason }}
            </p>
            <button @click="goToDetail(product)" class="btn btn-success mt-3">상품 상세 및 가입</button>
          </div>
        </div>
      </div>

      <div v-else class="no-recommendation-message-page text-center alert alert-info">
        <p>죄송합니다, 현재 {{ accountStore.user?.nickname || '회원' }}님께 추천드릴 수 있는 맞춤 상품이 없습니다.</p>
        <p v-if="!accountStore.user?.wealth">
          보다 정확한 추천을 위해 <RouterLink :to="{ name: 'ProFileView' }">프로필</RouterLink>에서 자산 정보를 업데이트 해주시면 도움이 됩니다.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import { useAccountStore } from '@/stores/accounts';
import { useFinancialStore } from '@/stores/financials';
import { useRouter, RouterLink } from 'vue-router';
// import bonobonoImage from '@/assets/bonobono.png'; // 필요시

const accountStore = useAccountStore();
const financialStore = useFinancialStore();
const router = useRouter();
const isLoadingRecommendations = ref(false);

const getAIRecommendations = async () => {
  if (accountStore.isLogin && accountStore.user) {
    isLoadingRecommendations.value = true;
    await financialStore.fetchAIRecommendations(); // 스토어의 액션 호출
    isLoadingRecommendations.value = false;
  } else {
    financialStore.recommendedProducts = [];
  }
};

onMounted(() => {
  // 페이지가 로드될 때 사용자 정보가 있으면 즉시 추천 가져오기
  if (accountStore.isLogin && accountStore.user) {
    getAIRecommendations();
  }
});

// 로그인 상태 또는 사용자 정보 변경 시 다시 추천 가져오기
watch([() => accountStore.isLogin, () => accountStore.user], ([newIsLogin, newUser], [oldIsLogin, oldUser]) => {
  if (newIsLogin && newUser) {
    // 로그인 상태로 변경되었거나, 사용자 정보가 변경된 경우 (예: 자산 업데이트)
    if (newIsLogin !== oldIsLogin || JSON.stringify(newUser) !== JSON.stringify(oldUser)) {
      getAIRecommendations();
    }
  } else if (!newIsLogin) {
    financialStore.recommendedProducts = []; // 로그아웃 시 초기화
  }
}, { deep: true, immediate: true }); // immediate: true로 초기 로드 시에도 감시자 실행

const getProductType = (type) => {
  if (type === 'deposit') return '정기예금';
  if (type === 'saving') return '정기적금';
  return type || '상품';
};

const goToDetail = (product) => {
  if (!product || product.id == null) {
    console.error("잘못된 상품 정보:", product);
    alert("상품 정보를 가져오는 데 문제가 발생했습니다.");
    return;
  }
  const targetView = product.product_type === 'deposit' ? 'DepositProductDetailView' : 
                     product.product_type === 'saving' ? 'SavingProductDetailView' : null;

  if (targetView) {
    router.push({ name: targetView, params: { id: product.id } });
  } else {
    console.warn('알 수 없는 상품 타입 또는 ID:', product);
    alert("해당 상품의 상세 정보를 찾을 수 없습니다.");
  }
};
</script>

<style scoped>
.ai-recommendation-container {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.character-image-page {
  width: 150px; /* 페이지 내 캐릭터 이미지 크기 */
  height: auto;
  margin-bottom: 1rem;
}

.recommendation-card {
  border: none; /* 기본 테두리 제거하고 box-shadow로 강조 */
  transition: transform 0.2s ease-in-out;
}
.recommendation-card:hover {
  transform: translateY(-5px);
}

.card-header h5 {
  font-weight: 500;
}

.product-name-page {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.product-rate-page {
  font-size: 1.1rem;
  color: #e74c3c;
  font-weight: bold;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.recommendation-reason-page {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  margin-top: 1rem;
}
.recommendation-reason-page strong {
  color: #34495e;
}

.loading-message,
.no-recommendation-message-page {
  padding: 40px 20px;
  color: #555;
}
.loading-message .spinner-border {
  width: 3rem;
  height: 3rem;
}
.no-recommendation-message-page a {
  color: #0d6efd;
}
</style>