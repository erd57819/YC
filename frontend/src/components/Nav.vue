<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{ name: 'MainView' }">YC Community</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">Articles</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'BankFinder' }">은행찾기</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'SearchView' }">관심사 찾기</RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item" v-if="!accountStore.isLogin">
            <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원 가입</RouterLink>
          </li>
          <li class="nav-item" v-if="!accountStore.isLogin">
            <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
          </li>
          <li class="nav-item" v-if="accountStore.isLogin">
            <a class="nav-link" href="#" @click.prevent="logOut">로그아웃</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore();

const logOut = () => {
  accountStore.logOut(); //
  // accounts 스토어의 logOut 메소드 내에서 라우팅 처리가 되어 있으므로,
  // Nav.vue에서는 별도의 라우팅을 하지 않아도 됩니다.
};
</script>

<style scoped>

</style>