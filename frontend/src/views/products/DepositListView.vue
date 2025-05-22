<template>
  <div class="container mt-5">
    <h2>예금 상품 목록</h2>

    <div class="mb-3">
      <label for="bankFilter" class="form-label">은행 검색</label>
      <div class="input-group">
        <input
          type="text"
          id="bankFilter"
          class="form-control"
          v-model="bankSearchTerm"
          placeholder="은행명을 입력하세요 (예: 국민은행)"
          @keyup.enter="applyBankFilter"
        />
        <button class="btn btn-outline-secondary" type="button" @click="applyBankFilter">검색</button>
        <button class="btn btn-outline-danger" type="button" @click="clearBankFilter" v-if="currentFilter">필터 해제</button>
      </div>
    </div>

    <div v-if="isLoading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="filteredProducts.length > 0">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">은행명</th>
            <th scope="col">상품명</th>
            <th scope="col">가입 방법</th>
            <th scope="col">비고</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id" @click="goToDetail(product.id)" style="cursor: pointer;">
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.fin_prdt_nm }}</td>
            <td>{{ product.join_way || '정보 없음' }}</td>
            <td>{{ product.etc_note }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p class="text-center">해당 조건에 맞는 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const products = ref([]);
const isLoading = ref(true);
const router = useRouter();
const bankSearchTerm = ref(''); // 은행 검색어
const currentFilter = ref(''); // 현재 적용된 필터 은행명

const API_URL = 'http://127.0.0.1:8000/api/v1';

// 예금 상품 목록 가져오기
const fetchDepositProducts = async (bankName = null) => {
  isLoading.value = true;
  try {
    let url = `${API_URL}/products/?type=deposit`;
    if (bankName) {
      url += `&bank=${encodeURIComponent(bankName)}`;
    }
    const response = await axios.get(url);
    products.value = response.data;
    currentFilter.value = bankName; // 현재 필터 상태 업데이트
  } catch (error) {
    console.error('예금 상품 목록 로딩 실패:', error);
    products.value = []; // 에러 발생 시 빈 배열로 초기화
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchDepositProducts(); // 컴포넌트 마운트 시 전체 예금 상품 로드
});

// 은행 필터 적용
const applyBankFilter = () => {
  if (bankSearchTerm.value.trim()) {
    fetchDepositProducts(bankSearchTerm.value.trim());
  } else {
    // 검색어가 없으면 전체 목록 다시 로드 (필터 해제와 유사)
    fetchDepositProducts();
  }
};

// 은행 필터 해제
const clearBankFilter = () => {
  bankSearchTerm.value = '';
  fetchDepositProducts(); // 전체 목록 다시 로드
};

// 상세 페이지로 이동
const goToDetail = (productId) => {
  router.push({ name: 'DepositDetailView', params: { productId: productId } }); // [cite: 46]
};

// 필터링된 상품 목록 (클라이언트 측 필터링 예시 - 필요시 API 필터링으로 대체)
// 현재는 API 호출 시 필터링하므로, computed는 단순히 products를 반환
const filteredProducts = computed(() => {
  return products.value;
});

</script>

<style scoped>
/* 필요한 경우 여기에 스타일 추가 */
.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}
</style>