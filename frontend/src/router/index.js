import { createRouter, createWebHistory } from 'vue-router';
import MainView from '@/views/MainView.vue';
import ArticleView from '@/views/ArticleView.vue';
import DetailView from '@/views/DetailView.vue';
import CreateView from '@/views/CreateView.vue';
import SignUpView from '@/views/SignUpView.vue';
import LogInView from '@/views/LogInView.vue';
import BankFinder from '@/views/BankFinder.vue';
import SearchView from '@/views/SearchView.vue';
import VideoDetailView from '@/views/VideoDetailView.vue';
import ArticleEditView from '@/views/ArticleEditView.vue';
import SilverView from '@/views/SilverView.vue';
import GoldView from '@/views/GoldView.vue';
import SavingProductDetailView from '@/views/SavingProductDetailView.vue';
import SavingProductsView from '@/views/SavingProductsView.vue';
import DepositProductDetailView from '@/views/DepositProductDetailView.vue';
import DepositProductsView from '@/views/DepositProductsView.vue';
import ProFileView from '@/components/ProFileView.vue';
import FinancialProductsCompareView from '@/views/FinancialProductsCompareView.vue';
import AIRecommendationView from '@/views/AIRecommendationView.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView
    },
    {
      path: '/articles',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/:id/edit',
      name: 'ArticleEditView',
      component: ArticleEditView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
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
      path: '/bank-finder',
      name: 'BankFinder',
      component: BankFinder
    },
    {
      path: '/search',
      name: 'SearchView',
      component: SearchView
    },
    {
      path: '/video/:id',
      name: 'video',
      component: VideoDetailView,
      props: true
    },
    {
      path: '/gold',
      name: 'GoldView',
      component: GoldView
    },
    {
      path: '/silver',
      name: 'SilverView',
      component: SilverView
    },
    { 
      path: '/financial-products-compare',
      name: 'FinancialProductsCompareView',
      component: FinancialProductsCompareView,
      children: [
        { // 기본적으로 예금 상품 탭이 먼저 보이도록 설정
          path: '', // 부모 경로와 동일
          redirect: { name: 'DepositProductsView' }
        },
        { // 예금 상품 목록 뷰
          path: 'deposits',
          name: 'DepositProductsView',
          component: DepositProductsView
        },
        // 예금 상품 상세 뷰
        {
          path: 'deposits/:id',
          name: 'DepositProductDetailView',
          component: DepositProductDetailView,
          props: true
        },
        // 적금 상품 목록 뷰
        {
          path: 'savings',
          name: 'SavingProductsView',
          component: SavingProductsView
        },
        // 적금 상품 상세 뷰
        {
          path: 'savings/:id',
          name: 'SavingProductDetailView',
          component: SavingProductDetailView,
          props: true
        },
      ]
    },
    {
      path: '/profile',
      name: 'ProFileView',
      component: ProFileView
    },
    { // AI 추천 페이지 라우트 추가
      path: '/ai-recommendations',
      name: 'AIRecommendationView',
      component: AIRecommendationView
    },
  ]
});

export default router;