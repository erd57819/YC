// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue' 
import MainPageView from '@/views/MainPageView.vue'
import BankMapView from '@/views/BankMapView.vue' 

import { useAccountStore } from '@/stores/accounts'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', 
      name: 'MainPageView',
      component: MainPageView
    },
    {
      path: '/articles', 
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
      beforeEnter: (to, from) => { 
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
      path: '/map',
      name: 'BankMapView',
      component: BankMapView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profile', 
      name: 'ProfileView',
      component: ProfileView,
      beforeEnter: (to, from) => { 
        const store = useAccountStore()
        if (!store.isLogin) {
          alert('로그인이 필요합니다.')
          return { name: 'LogInView' }
        }
      }
    },
    {
      path: '/products/deposit',
      name: 'DepositListView',
      // component: () => import('@/views/products/DepositListView.vue') 
    },
    {
      path: '/products/deposit/:productId',
      name: 'DepositDetailView',
      // component: () => import('@/views/products/DepositDetailView.vue')
    },
  ]
})

router.beforeEach(async (to, from, next) => {
  const store = useAccountStore();
  if (store.token && !store.currentUser) {
    try {
      await store.getUserProfile();
      next(); // 사용자 정보 로드 성공 시 다음으로 진행
    } catch (error) {
      console.error("Failed to fetch user profile on navigation:", error);
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        try {
            await store.logOut(); // logOut이 Promise를 반환하므로 await 사용
        } catch (logoutError) {
            console.error("Error during logout after profile fetch failure:", logoutError);
        }
        // logOut 함수가 내비게이션을 직접 처리하지 않으므로, 여기서 명시적으로 처리
        return next({ name: 'LogInView' }); 
      } else {
        // 다른 종류의 에러 (네트워크 에러 등)는 일단 통과시키거나, 에러 페이지로 안내
        next(); 
      }
    }
  } else {
    next(); // 토큰이 없거나 이미 사용자 정보가 있는 경우
  }
});

export default router