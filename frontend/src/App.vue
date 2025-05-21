<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/accounts' // accounts 스토어 임포트

const accountStore = useAccountStore()

</script>

<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticleView' }">Articles</RouterLink> |
      <RouterLink :to="{ name: 'CreateView' }">Create</RouterLink> |
      
      <template v-if="accountStore.isLogin">
        <a @click="accountStore.logOut" href="#">Logout</a>
      </template>
      <template v-else>
        <RouterLink :to="{ name: 'SignUpView' }">SignUp</RouterLink> |
        <RouterLink :to="{ name: 'LogInView' }">LogIn</RouterLink>
      </template>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
/* 기존 스타일 유지 또는 추가 */
</style>