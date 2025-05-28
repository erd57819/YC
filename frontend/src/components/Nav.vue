<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{ name: 'MainView' }">YC BANK </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">게시판</RouterLink>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              예적금 상품 비교
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><RouterLink class="dropdown-item" :to="{ name: 'DepositProductsView' }">예금 상품</RouterLink></li>
              <li><RouterLink class="dropdown-item" :to="{ name: 'SavingProductsView' }">적금 상품</RouterLink></li>
            </ul>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'BankFinder' }">은행찾기</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'SearchView' }">관심사 찾기</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'GoldView' }">현물 시세</RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav navbar-nav-right">
          <li class="nav-item" v-if="!accountStore.isLogin">
            <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원 가입</RouterLink>
          </li>
          <li class="nav-item" v-if="!accountStore.isLogin">
            <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
          </li>
          <li class="nav-item" v-if="accountStore.isLogin">
            <a class="nav-link welcome-message" href="#">
              <strong>{{ accountStore.user?.nickname }}</strong>님 환영합니다!
            </a>
          </li>
          <li class="nav-item" v-if="accountStore.isLogin">
            <RouterLink class="nav-link" :to="{ name: 'ProFileView' }">프로필</RouterLink>
          </li>
          <li class="nav-item" v-if="accountStore.isLogin">
            <a class="nav-link logout-link" href="#" @click.prevent="logOut">로그아웃</a>
          </li>
          <!-- <li class="nav-item" v-if="accountStore.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'AIRecommendationView' }">AI 상품 추천</RouterLink>
          </li> -->
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
  accountStore.logOut();
};
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  font-family: 'Helvetica Neue', sans-serif;
  transition: background-color 0.3s ease;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem; 
  color: #2c3e50;
  transition: color 0.3s ease;
}

.navbar-brand:hover {
  color: #3498db; 
}

.nav-link {
  color: #34495e; 
  font-weight: 600; /* [변경점] 500 -> 600으로 변경하여 글자를 더 진하게 */
  margin: 0 10px;
  padding: 8px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
  text-align: center;
}

.nav-link:hover {
  background-color: #f8f9fa;
  color: #3498db;
}

.router-link-exact-active {
  background-color: #3498db;
  color: #ffffff !important; 
  font-weight: bold;
}

/* [추가] 오른쪽 메뉴의 크기를 줄이기 위한 새로운 스타일 규칙 */
.navbar-nav-right .nav-link {
  font-size: 0.9rem;  /* 폰트 크기를 약간 작게 */
  padding: 6px 12px;  /* 패딩(여백)을 줄여서 전체적인 크기 축소 */
}

.logout-link {
  color: #e74c3c !important; 
  font-weight: bold;
}

.logout-link:hover {
  background-color: #c0392b;
  color: #ffffff !important;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(44, 62, 80, 0.8)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

.navbar-toggler {
  border-color: transparent;
}
</style>