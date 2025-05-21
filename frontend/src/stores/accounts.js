// frontend/src/stores/accounts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('') // 로그인 성공 시 토큰 저장
  const router = useRouter()

  // 로그인 여부 확인
  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const signUp = function ({username, password1, password2, age}) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: {
        username, password1, password2, age
      }
    })
      .then(res => {
        console.log('회원가입 성공!')
        router.push({ name: 'LogInView' })
      })
      .catch(err => console.log(err))
  }

  const logIn = function({username, password}) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key // 로그인 성공 시 토큰 저장
        router.push({ name: 'ArticleView' }) // 로그인 성공 시 게시글 목록으로 이동
      })
      .catch(err => console.log(err))
  }

  // 로그아웃 기능
  const logOut = function () {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/logout/`,
      headers: {
        Authorization: `Token ${token.value}` // 현재 로그인 토큰을 헤더에 포함하여 전송
      }
    })
      .then(res => {
        token.value = '' // 토큰 초기화 (로그아웃 처리)
        console.log('로그아웃 성공!')
        router.push({ name: 'ArticleView' }) // 로그아웃 후 게시글 목록으로 이동
      })
      .catch(err => console.log(err))
  }

  // 외부로 노출할 상태와 함수들을 반환
  return { 
    signUp, logIn, token, isLogin, logOut
  }
}, { persist: true })