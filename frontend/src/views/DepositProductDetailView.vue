<template>
  <div class="container mt-5" v-if="store.depositProduct">
    <h2>{{ store.depositProduct.fin_prdt_nm }}</h2>
    <p><strong>은행:</strong> {{ store.depositProduct.kor_co_nm }}</p>
    <p><strong>가입 방법:</strong> {{ store.depositProduct.join_way }}</p>
    <p><strong>특별 조건:</strong> {{ store.depositProduct.spcl_cnd }}</p>
    <p><strong>기타 사항:</strong> {{ store.depositProduct.etc_note }}</p>

    <h4 class="mt-4">금리 옵션</h4>
    <table class="table">
      <thead>
        <tr>
          <th>저축 기간 (개월)</th>
          <th>이자율 종류</th>
          <th>기본 금리</th>
          <th>최고 금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="option in store.depositProduct.options" :key="option.id">
          <td>{{ option.save_trm }}</td>
          <td>{{ option.intr_rate_type_nm }}</td>
          <td>{{ option.intr_rate }}%</td>
          <td>{{ option.intr_rate2 }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="container mt-5">
    <p>상품 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useFinancialStore } from '@/stores/financials';
import { useRoute } from 'vue-router';

const store = useFinancialStore();
const route = useRoute();

onMounted(() => {
  store.fetchDepositProductDetail(route.params.id);
});
</script>