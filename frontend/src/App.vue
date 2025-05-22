<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="{ name: 'ArticleView' }">YC Community</RouterLink>
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
            <li class="nav-item" v-if="accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'CreateView' }">Create Article</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">Sign Up</RouterLink>
            </li>
            <li class="nav-item" v-if="!accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'LogInView' }">Log In</RouterLink>
            </li>
            <li class="nav-item" v-if="accountStore.isLogin">
              <a class="nav-link" href="#" @click.prevent="logOut">Log Out</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const logOut = () => {
  accountStore.logOut()
}
</script>

<style>
/* 필요한 경우 여기에 추가 스타일을 작성할 수 있습니다. */
body {
  background-color: #f8f9fa; /* Optional: Light background for the body */
}
/* .container 스타일은 주석 처리하거나 필요에 맞게 조정하세요. */
/*
.container {
  background-color: #ffffff; 
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
*/
</style>