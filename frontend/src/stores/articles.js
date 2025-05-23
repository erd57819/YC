// frontend/src/stores/articles.js (수정된 최종본)

import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // 게시글 목록 가져오기
  const getArticles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/`);
      articles.value = response.data;
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  // 단일 게시글 정보 가져오기
  const getArticleDetail = async (articleId) => {
    try {
      // ★★★ 오타를 수정한 부분 ★★★
      const response = await axios.get(`${API_URL}/api/v1/articles/${articleId}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching article detail:', error);
      return null;
    }
  };

  // 게시글 생성하기
  const createArticle = async (payload) => {
    const accountStore = useAccountStore();
    try {
      const response = await axios.post(`${API_URL}/api/v1/articles/`, payload, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      console.log('게시글 작성 성공!', response.data);
      router.push({ name: 'ArticleView' });
    } catch (error) {
      console.error('Error creating article:', error);
    }
  };

  // 게시글 삭제하기
  const deleteArticle = async (articleId) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) return;

    try {
      await axios.delete(`${API_URL}/api/v1/articles/${articleId}/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      const index = articles.value.findIndex(article => article.id === articleId);
      if (index > -1) {
        articles.value.splice(index, 1);
      }
    } catch (error) {
      console.error('Error deleting article:', error);
    }
  };

  // 댓글 생성하기
  const createComment = async (articleId, payload) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) return;

    try {
      await axios.post(`${API_URL}/api/v1/articles/${articleId}/comments/`, payload, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
    } catch (error) {
      console.error('Error creating comment:', error);
    }
  };

  return { 
    articles, 
    API_URL, 
    getArticles, 
    getArticleDetail, 
    createArticle, 
    deleteArticle, 
    createComment 
  }
}, { persist: true })