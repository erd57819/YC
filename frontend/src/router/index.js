import { createRouter, createWebHistory } from 'vue-router';
import MainView from '@/views/MainView.vue'; //
import ArticleView from '@/views/ArticleView.vue'; //
import DetailView from '@/views/DetailView.vue'; //
import CreateView from '@/views/CreateView.vue'; //
import SignUpView from '@/views/SignUpView.vue'; //
import LogInView from '@/views/LogInView.vue'; //
import BankFinder from '@/views/BankFinder.vue'; 
import SearchView from '@/views/SearchView.vue'; //
import VideoDetailView from '@/views/VideoDetailView.vue';
import ArticleEditView from '@/views/ArticleEditView.vue'; // Import the VideoDetailView component
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
    { path: '/video/:id',
      name: 'video',
      component: VideoDetailView,
      props: true },

  ]
});

export default router;