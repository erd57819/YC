// frontend/src/stores/articles.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts' // accounts 스토어 임포트
import { useRouter } from 'vue-router'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  const getArticles = function () {
    const accountStore = useAccountStore() // accounts 스토어 사용

    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${accountStore.token}` // 토큰을 Authorization 헤더에 추가
      }
    })
      .then(res => {
        articles.value = res.data
      })
      .catch(err => console.log(err))
  }

  const createArticle = function (payload) {
    const { title, content } = payload
    const accountStore = useAccountStore()

    axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/`,
      data: {
        title, content
      },
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        console.log('게시글 작성 성공!', res.data)
        router.push({ name: 'ArticleView' })
      })
      .catch(err => console.log(err))
  }

  return { articles, API_URL, getArticles, createArticle }
}, { persist: true })