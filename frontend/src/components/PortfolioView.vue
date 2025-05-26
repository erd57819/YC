<template>
  <div>
    <h5 class="mt-4 mb-3">가입한 상품 목록</h5>
    <div v-if="subscribedProducts.length > 0">
      <ul class="list-group">
        <li v-for="product in subscribedProducts" :key="`${product.type}-${product.id}`" class="list-group-item d-flex justify-content-between align-items-center">
          <span>
            [{{ product.type === 'deposit' ? '예금' : '적금' }}] {{ product.product_info.kor_co_nm }} - {{ product.product_info.fin_prdt_nm }}
          </span>
          <button class="btn btn-sm btn-outline-danger" @click="cancelSubscription(product.type, product.id)">삭제</button>
        </li>
      </ul>

      <div class="mt-5">
        <h5 class="mb-3">가입 상품 금리 비교</h5>
        <SubscribedProductsChart :products="subscribedProducts" />
      </div>

    </div>
    <div v-else>
      <p>가입한 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAccountStore } from '@/stores/accounts';
import { useFinancialStore } from '@/stores/financials';
import SubscribedProductsChart from '@/components/SubscribedProductsChart.vue';

const accountStore = useAccountStore();
const financialStore = useFinancialStore();

const subscribedProducts = computed(() => {
  if (!accountStore.user) return [];
  const deposits = accountStore.user.subscribed_deposits?.map(d => ({ ...d, type: 'deposit', product_info: d.deposit_product })) || [];
  const savings = accountStore.user.subscribed_savings?.map(s => ({ ...s, type: 'saving', product_info: s.saving_product })) || [];
  return [...deposits, ...savings];
});

const cancelSubscription = (type, id) => {
  if (confirm('정말로 가입을 취소하시겠습니까?')) {
    financialStore.deleteSubscription(type, id);
  }
};
</script>

<style scoped>
/* 스타일은 필요에 따라 추가 */
</style>