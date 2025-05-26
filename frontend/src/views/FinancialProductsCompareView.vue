<template>
  <div class="container mt-5">
    <h1 class="mb-4">금융 상품 비교</h1>
    <div class="d-flex justify-content-start gap-2 mb-4">
      <RouterLink :to="{ name: 'DepositProductsView' }" class="btn btn-primary" :class="{ 'active': $route.name === 'DepositProductsView' || $route.name === 'DepositProductDetailView' }">정기예금</RouterLink>
      <RouterLink :to="{ name: 'SavingProductsView' }" class="btn btn-primary" :class="{ 'active': $route.name === 'SavingProductsView' || $route.name === 'SavingProductDetailView' }">정기적금</RouterLink>
    </div>
    
    <RouterView /> </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();

// 현재 라우트 이름을 감지하여 버튼의 active 상태를 결정
// computed(() => route.name === 'DepositProductsView' || route.name === 'DepositProductDetailView');
// computed(() => route.name === 'SavingProductsView' || route.name === 'SavingProductDetailView');

// 이 뷰에서는 특별한 로직이 없으므로 스크립트 부분은 간단합니다.
</script>

<style scoped>
/* 탭 버튼 스타일 */
.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.btn-primary.active {
  background-color: #2980b9;
  border-color: #2980b9;
  font-weight: bold;
}
</style>