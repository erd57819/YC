<template>
  <nav class="navbar navbar-expand-lg">
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
            <a class="nav-link logout-link" href="#" @click.prevent="logOut">로그아웃</a>
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
  accountStore.logOut();
};
</script>

<style scoped>
/* 네비게이션 바 전체에 대한 기본 스타일 */
.navbar {
  background-color: #2c3e50; /* 기존 bg-dark보다 조금 더 부드러운 색상 */
  padding: 10px 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: 'Helvetica Neue', sans-serif;
  transition: background-color 0.3s ease;
}

/* 브랜드 로고 스타일 */
.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem; /* 글자 크기 증가 */
  color: #ecf0f1; /* 밝은 회색 계열 */
  transition: color 0.3s ease;
}

.navbar-brand:hover {
  color: #3498db; /* 호버 시 색상 변경 */
}

/* 네비게이션 링크 스타일 */
.nav-link {
  color: #bdc3c7; /* 기본 링크 색상 */
  font-weight: 500;
  margin: 0 10px;
  padding: 8px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
  text-align: center;
}

/* 네비게이션 링크에 마우스를 올렸을 때 */
.nav-link:hover {
  background-color: #34495e;
  color: #ffffff;
}

/* 현재 활성화된(보고 있는 페이지) 링크 스타일 */
.router-link-exact-active {
  background-color: #3498db;
  color: #ffffff !important; /* !important를 사용해 부트스트랩 스타일 덮어쓰기 */
  font-weight: bold;
}

/* 로그아웃 링크 특별 스타일 */
.logout-link {
  color: #e74c3c !important; /* 로그아웃은 눈에 띄게 붉은 계열로 */
  font-weight: bold;
}

.logout-link:hover {
  background-color: #c0392b;
  color: #ffffff !important;
}

/* 토글 버튼 아이콘 색상 변경 (모바일 뷰) */
.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(236, 240, 241, 0.8)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

/* 토글 버튼 테두리 색상 제거 */
.navbar-toggler {
  border-color: transparent;
}
</style>