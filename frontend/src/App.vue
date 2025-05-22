<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="{ name: 'MainPageView' }">
          <img src="@/assets/bank_logo.png" alt="FinLife" style="height: 30px; margin-right: 10px;"> FinLife
        </RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'MainPageView' }">메인</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">게시판</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'DepositListView' }">예적금 비교</RouterLink> </li>
            <li class="nav-item" v-if="accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'CreateView' }">글쓰기</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            </li>
            <li class="nav-item" v-if="!accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
            </li>
            <li class="nav-item" v-if="accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'ProfileView' }">
                {{ accountStore.currentUser?.username }}님 프로필
              </RouterLink>
            </li>
            <li class="nav-item" v-if="accountStore.isLogin">
              <a class="nav-link" href="#" @click.prevent="accountStore.logOut">로그아웃</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main class="container mt-4">
    <RouterView />
  </main>

  <footer class="bg-light text-center text-lg-start mt-auto py-3">
    <div class="text-center">
      © 2025 FinLife. All rights reserved.
    </div>
  </footer>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { onMounted } from 'vue';

const accountStore = useAccountStore()
const router = useRouter()

// 앱이 마운트될 때 토큰이 있고 사용자 정보가 없다면 가져오기
// (라우터 가드에서도 처리하지만, 초기 로드 시 한 번 더 확인 가능)
onMounted(async () => {
  if (accountStore.token && !accountStore.currentUser) {
    try {
      await accountStore.getUserProfile();
    } catch (error) {
      console.error("Failed to fetch user profile on app mount:", error);
      // 여기서도 에러 발생 시 로그인 페이지로 리다이렉트 또는 로그아웃 처리 가능
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        accountStore.logOut();
        router.push({ name: 'LogInView' });
      }
    }
  }
});

// 로고 이미지 예시 (실제 이미지를 assets 폴더에 추가해야 함)
// import bankLogo from '@/assets/bank_logo.png' // 스크립트에서 사용 시
</script>

<style scoped>
body, #app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex: 1;
}
.navbar-brand img { /* 로고 스타일 예시 */
  vertical-align: middle;
}
</style>