<template>
  <div class="profile-container my-5">
    <div v-if="accountStore.user" class="profile-layout">
      <div class="sidebar">
        <h3>{{ accountStore.user.username }}님</h3>
        <p class="text-muted">프로필 관리</p>
        <hr>
        <ul class="nav flex-column">
          <li class="nav-item">
            <a class="nav-link" 
               :class="{ active: activeView === 'info' }" 
               href="#" 
               @click.prevent="activeView = 'info'">
              기본 정보 수정
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" 
               :class="{ active: activeView === 'portfolio' }" 
               href="#" 
               @click.prevent="activeView = 'portfolio'">
              포트폴리오 수정
            </a>
          </li>
        </ul>
      </div>

      <div class="content">
        <component :is="currentViewComponent" />
      </div>
    </div>
    <div v-else class="text-center">
      <p>로그인 후 이용해주세요.</p>
      <RouterLink :to="{ name: 'LogInView' }">로그인 페이지로 이동</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineAsyncComponent } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore();
const activeView = ref('portfolio');

// 경로 수정: components -> views
const UserInfoEdit = defineAsyncComponent(() => import('@/views/UserInfoEdit.vue'));
const PortfolioView = defineAsyncComponent(() => import('@/views/PortfolioView.vue'));

onMounted(() => {
  accountStore.fetchUser();
});

const currentViewComponent = computed(() => {
  if (activeView.value === 'info') {
    return UserInfoEdit;
  } else {
    return PortfolioView;
  }
});
</script>

<style scoped>
/* 스타일은 이전과 동일 */
.profile-container {
  max-width: 960px;
  margin: auto;
}
.profile-layout {
  display: flex;
}
.sidebar {
  flex: 0 0 220px;
  border-right: 1px solid #dee2e6;
  padding: 20px;
}
.sidebar .nav-link {
  color: #333;
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 0.25rem;
}
.sidebar .nav-link.active {
  color: #0d6efd;
  background-color: #e9ecef;
  font-weight: bold;
}
.sidebar .nav-link:not(.active):hover {
  background-color: #f8f9fa;
}
.content {
  flex-grow: 1;
  padding-left: 30px;
}
</style>