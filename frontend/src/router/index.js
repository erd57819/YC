// router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue' // 프로필 뷰 임포트
import MainPageView from '@/views/MainPageView.vue' // 메인 페이지 뷰 임포트 (추가)

import { useAccountStore } from '@/stores/accounts'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // 메인 페이지 경로 변경
      name: 'MainPageView',
      component: MainPageView
    },
    {
      path: '/articles', // 게시글 목록 경로
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView,
      beforeEnter: (to, from) => { // 네비게이션 가드 추가
        const store = useAccountStore()
        if (!store.isLogin) {
          alert('로그인이 필요합니다.')
          return { name: 'LogInView' }
        }
      }
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profile', // 프로필 페이지 라우트 추가
      name: 'ProfileView',
      component: ProfileView,
      beforeEnter: (to, from) => { // 네비게이션 가드 추가
        const store = useAccountStore()
        if (!store.isLogin) {
          alert('로그인이 필요합니다.')
          return { name: 'LogInView' }
        }
      }
    },
    // 예적금 관련 라우트 (예시)
    {
      path: '/products/deposit',
      name: 'DepositListView',
      // component: () => import('@/views/products/DepositListView.vue') // Lazy loading
      // 실제 컴포넌트 생성 후 연결
    },
    {
      path: '/products/deposit/:productId',
      name: 'DepositDetailView',
      // component: () => import('@/views/products/DepositDetailView.vue')
    },
    // 추가 기능들을 위한 라우트들...
  ]
})

// 전역 네비게이션 가드 (예시: 로그인 후 사용자 정보 가져오기)
router.beforeEach(async (to, from, next) => {
  const store = useAccountStore();
  // 앱 로드 시 또는 페이지 이동 시 토큰이 있고 사용자 정보가 없다면 가져오기
  if (store.token && !store.currentUser) {
    try {
      await store.getUserProfile();
    } catch (error) {
      console.error("Failed to fetch user profile on navigation:", error);
      // 프로필 로드 실패 시 (예: 토큰 만료) 로그아웃 처리 또는 로그인 페이지로 리다이렉트
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        store.logOut(); // store의 로그아웃 함수 사용
        return next({ name: 'LogInView' });
      }
    }
  }
  next();
});

export default router