<template>
  <div class="container mt-5">
    <h1>정기적금 상품 목록</h1>
    <table class="table table-hover">
      <thead>
        <tr>
          <th>은행</th>
          <th>상품명</th>
          <th>가입 방법</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in store.savingProducts" :key="product.id" @click="goToDetail(product.id)">
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ product.join_way }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useFinancialStore } from '@/stores/financials';
import { useRouter } from 'vue-router';

const store = useFinancialStore();
const router = useRouter();

onMounted(() => {
  store.fetchSavingProducts();
});

const goToDetail = (id) => {
  router.push({ name: 'SavingProductDetailView', params: { id } });
};
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>
