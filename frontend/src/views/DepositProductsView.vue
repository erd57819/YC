<template>
  <div class="container mt-5">
    <h1>정기예금 상품 목록</h1>
    <div class="row mb-4">
      <div class="col-md-4">
        <label for="bankSelect" class="form-label">은행 선택:</label>
        <select class="form-select" id="bankSelect" v-model="selectedBank" @change="applyFilters">
          <option value="">-- 전체 은행 --</option>
          <option v-for="bank in financialStore.banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="monthSelect" class="form-label">공시월 선택:</label>
        <select class="form-select" id="monthSelect" v-model="selectedDclsMonth" @change="applyFilters">
          <option value="">-- 전체 공시월 --</option>
          <option v-for="month in financialStore.dclsMonths" :key="month" :value="month">{{ month }}</option>
        </select>
      </div>
      <div class="col-md-4 d-flex align-items-end">
        <button class="btn btn-primary" @click="applyFilters">검색</button>
      </div>
    </div>

    <table class="table table-hover">
      <thead>
        <tr>
          <th>공시제출월</th>
          <th>금융회사명</th>
          <th>상품명</th>
          <th>저축기간 (개월)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in financialStore.depositProducts" :key="`${product.id}-${product.save_trm}`" @click="goToDetail(product.id)">
          <td>{{ product.dcls_month }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <!-- <td>{{ product.options && product.options.length > 0 ? product.options.map(o => o.save_trm).join(', ') : 'N/A' }}</td> -->
          <td>{{ product.save_trm != null ? product.save_trm : 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useFinancialStore } from '@/stores/financials';
import { useRouter } from 'vue-router';

const financialStore = useFinancialStore();
const router = useRouter();

const selectedBank = ref('');
const selectedDclsMonth = ref('');

onMounted(() => {
  financialStore.fetchBankInfo(); // 은행 이름 정보 로드
  // 초기 예금 상품 목록을 불러와 dclsMonths를 채웁니다.
  financialStore.fetchDepositProducts(); 
});

const applyFilters = () => {
  const params = {};
  if (selectedBank.value) {
    params.kor_co_nm = selectedBank.value;
  }
  if (selectedDclsMonth.value) {
    params.dcls_month = selectedDclsMonth.value;
  }
  financialStore.fetchDepositProducts(params);
};

const goToDetail = (id) => {
  router.push({ name: 'DepositProductDetailView', params: { id } }); // 상세 페이지로 이동
};
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>