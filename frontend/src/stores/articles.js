// frontend/src/stores/articles.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // ... (getArticles, getArticleDetail, createArticle, deleteArticle, createComment 함수는 그대로 둡니다) ...

  const getArticles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/`);
      articles.value = response.data;
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  const getArticleDetail = async (articleId) => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/${articleId}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching article detail:', error);
      return null;
    }
  };

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

  // ▼▼▼▼▼ [추가] 댓글 삭제 함수 ▼▼▼▼▼
  const deleteComment = async (commentId) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) {
      console.error('로그인이 필요합니다.');
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/v1/articles/comments/${commentId}/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      // 댓글 삭제 후, 해당 게시글 상세 정보를 다시 불러오거나
      // 프론트엔드 상태에서 댓글을 제거하는 로직을 추가하면 좋습니다.
      console.log('댓글 삭제 성공!');
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };
    const updateArticle = async (articleId, payload) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) {
      console.error('로그인이 필요합니다.');
      // 필요시 로그인 페이지로 리다이렉트
      // router.push({ name: 'LogInView' }); 
      return null; // 또는 에러 throw
    }

    try {
      const response = await axios.put(
        `${API_URL}/api/v1/articles/${articleId}/`, // 백엔드 수정 API 엔드포인트
        payload,
        {
          headers: { Authorization: `Token ${accountStore.token}` },
        }
      );
      // 수정 성공 후, 상태 업데이트 (예: articles 목록에서 해당 게시글 업데이트 또는 상세 정보 다시 로드)
      // 여기서는 DetailView로 이동하여 다시 로드하도록 함
      router.push({ name: 'DetailView', params: { id: articleId } }); 
      return response.data;
    } catch (error) {
      console.error('Error updating article:', error.response?.data || error.message);
      // 사용자에게 에러 알림
      alert(`게시글 수정에 실패했습니다: ${error.response?.data?.detail || error.message}`);
      return null;
    }
  };


  return { 
    articles, 
    API_URL, 
    getArticles, 
    getArticleDetail, 
    createArticle, 
    deleteArticle, 
    createComment,
    deleteComment,
    updateArticle 
  }
}, { persist: true })