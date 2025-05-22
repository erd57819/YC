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
              <RouterLink class="nav-link" :to="{ name: 'DepositListView' }">예적금 비교</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'BankMapView' }">은행 찾기</RouterLink>
            </li>
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
              <a class="nav-link" href="#" @click.prevent="handleLogout">로그아웃</a>
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

// 로그아웃 핸들러 함수
const handleLogout = async () => {
  try {
    await accountStore.logOut();
    // 로그아웃 후 메인 페이지 또는 로그인 페이지로 리디렉션
    router.push({ name: 'MainPageView' }); // 또는 LogInView
  } catch (error) {
    console.error('로그아웃 실패:', error);
    // 필요한 경우 사용자에게 오류 메시지 표시
  }
};

onMounted(async () => {
  if (accountStore.token && !accountStore.currentUser) {
    try {
      await accountStore.getUserProfile();
    } catch (error) {
      console.error("Failed to fetch user profile on app mount:", error);
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        // 토큰이 유효하지 않으면 로그아웃 처리 후 로그인 페이지로 이동
        await accountStore.logOut(); // logOut이 Promise를 반환하도록 수정했으므로 await 사용 가능
        router.push({ name: 'LogInView' });
      }
    }
  }
});
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