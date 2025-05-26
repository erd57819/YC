<template>
  <div class="container mt-5">
    <div v-if="accountStore.user" class="card">
      <div class="card-header">
        <h2>프로필 정보</h2>
      </div>
      <div class="card-body">
        <p><strong>사용자 이름:</strong> {{ accountStore.user.username }}</p>
        <p><strong>닉네임:</strong> {{ accountStore.user.nickname }}</p>
        <p><strong>나이:</strong> {{ accountStore.user.age }}</p>
        <p><strong>연봉:</strong> {{ accountStore.user.salary }}</p>
        <p><strong>자산:</strong> {{ accountStore.user.wealth }}</p>
        <p><strong>가입일:</strong> {{ new Date(accountStore.user.created_at).toLocaleDateString() }}</p>
      </div>
    </div>
    <div v-else>
      <p>로그인 후 이용해주세요.</p>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore();
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>