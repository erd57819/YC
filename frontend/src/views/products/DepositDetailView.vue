<template>
  <div class="container mt-5">
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="product">
      <h2>{{ product.fin_prdt_nm }} <small class="text-muted">({{ product.kor_co_nm }})</small></h2>
      <hr />

      <div class="card mb-4">
        <div class="card-header">
          상품 기본 정보
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><strong>금융 상품 코드:</strong> {{ product.fin_prdt_cd }}</li>
          <li class="list-group-item"><strong>가입 방법:</strong> {{ product.join_way || '정보 없음' }}</li>
          <li class="list-group-item"><strong>만기 후 이자율:</strong> {{ product.mtrt_int || '정보 없음' }}</li>
          <li class="list-group-item"><strong>우대 조건:</strong> {{ product.spcl_cnd || '정보 없음' }}</li>
          <li class="list-group-item"><strong>가입 대상:</strong> {{ product.join_member || '정보 없음' }}</li>
          <li class="list-group-item"><strong>기타 유의사항:</strong> {{ product.etc_note || '정보 없음' }}</li>
          <li class="list-group-item" v-if="product.max_limit"><strong>최고 한도:</strong> {{ product.max_limit.toLocaleString() }} 원</li>
        </ul>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          금리 정보 (가입 기간별) [cite: 50]
        </div>
        <div class="table-responsive">
          <table class="table mb-0">
            <thead>
              <tr>
                <th>저축 기간 (개월)</th>
                <th>저축 금리 유형</th>
                <th>기본 금리 (%)</th>
                <th>최고 우대 금리 (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!product.options || product.options.length === 0">
                <td colspan="4" class="text-center">금리 정보가 없습니다.</td>
              </tr>
              <tr v-for="option in product.options" :key="option.id">
                <td>{{ option.save_trm }}</td>
                <td>{{ option.intr_rate_type_nm }} ({{ option.intr_rate_type }})</td>
                <td>{{ option.intr_rate !== null ? option.intr_rate : '-' }}</td>
                <td>{{ option.intr_rate2 !== null ? option.intr_rate2 : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div class="text-center" v-if="accountStore.isLogin"> [cite: 51]
        <button 
          class="btn btn-primary btn-lg" 
          @click="subscribeToProduct"
          :disabled="isSubscribing || isAlreadySubscribed"
        >
          <span v-if="isSubscribing" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          {{ subscriptionButtonText }}
        </button>
        <p v-if="subscriptionMessage" class="mt-2" :class="{'text-success': !subscriptionError, 'text-danger': subscriptionError}">
          {{ subscriptionMessage }}
        </p>
      </div>
      <div v-else class="alert alert-info text-center">
        상품에 가입하려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
      </div>

    </div>
    <div v-else class="alert alert-danger text-center">
      상품 정보를 불러오는 데 실패했거나 해당 상품이 존재하지 않습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts'; //

const route = useRoute();
const router = useRouter();
const accountStore = useAccountStore();

const product = ref(null);
const isLoading = ref(true);
const isSubscribing = ref(false);
const subscriptionMessage = ref('');
const subscriptionError = ref(false);

const API_URL = 'http://127.0.0.1:8000/api/v1';
const productId = route.params.productId;

// 상품 상세 정보 가져오기
onMounted(async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${API_URL}/products/${productId}/`);
    product.value = response.data;
  } catch (error) {
    console.error('상품 상세 정보 로딩 실패:', error);
    product.value = null;
  } finally {
    isLoading.value = false;
  }
});

const isAlreadySubscribed = computed(() => {
  if (!product.value || !accountStore.currentUser || !accountStore.currentUser.subscribed_products) {
    return false;
  }
  const subscribedIds = accountStore.currentUser.subscribed_products.split(',').map(s => s.trim());
  return subscribedIds.includes(product.value.fin_prdt_cd);
});

const subscriptionButtonText = computed(() => {
  if (isAlreadySubscribed.value) return '이미 가입한 상품입니다';
  if (isSubscribing.value) return '처리 중...';
  return '가입하기';
});

// 상품 가입 함수 [cite: 51]
const subscribeToProduct = async () => {
  if (!accountStore.isLogin || !product.value || isAlreadySubscribed.value) {
    subscriptionMessage.value = '로그인이 필요하거나 이미 가입한 상품입니다.';
    subscriptionError.value = true;
    return;
  }

  isSubscribing.value = true;
  subscriptionMessage.value = '';
  subscriptionError.value = false;

  try {
    await axios.post(
      `${API_URL}/products/${product.value.fin_prdt_cd}/subscribe/`, 
      {}, // POST 요청 본문 (필요시 추가 데이터)
      { headers: { Authorization: `Token ${accountStore.token}` } }
    );
    subscriptionMessage.value = '상품에 성공적으로 가입했습니다!';
    subscriptionError.value = false;
    // 성공 시 사용자 정보 갱신 (선택적: Pinia 스토어에서 사용자 정보를 다시 불러올 수 있음)
    await accountStore.getUserProfile(); // 가입 후 최신 정보로 업데이트
  } catch (error) {
    console.error('상품 가입 실패:', error.response?.data || error.message);
    subscriptionMessage.value = error.response?.data?.message || error.response?.data?.error || '가입 처리 중 오류가 발생했습니다.';
    subscriptionError.value = true;
  } finally {
    isSubscribing.value = false;
  }
};
</script>

<style scoped>
.list-group-item strong {
  margin-right: 8px;
}
small.text-muted {
  font-size: 0.9rem;
}
</style>