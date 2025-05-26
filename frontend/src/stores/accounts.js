import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref(null)
  const user = ref(null)
  const router = useRouter()

  const isLogin = computed(() => !!token.value)

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await axios({
        method: 'GET',
        url: `${ACCOUNT_API_URL}/user/`,
        headers: { Authorization: `Token ${token.value}` }
      })
      user.value = response.data
    } catch (err) {
      console.error('사용자 정보 로딩 실패:', err)
      // 토큰이 유효하지 않을 수 있으므로 로그아웃 처리
      token.value = null
      user.value = null
    }
  }

  const signUp = function (payload) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: payload
    })
      .then(() => {
        console.log('회원가입 성공!')
        router.push({ name: 'LogInView' })
      })
      .catch(err => console.error('회원가입 실패:', err.response.data))
  }

  const logIn = function(payload) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: payload
    })
      .then(async (res) => {
        token.value = res.data.key
        await fetchUser() // 로그인 직후 사용자 정보 가져오기
        router.push({ name: 'MainView' })
      })
      .catch(err => console.error('로그인 실패:', err.response.data))
  }

  const logOut = function () {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/logout/`,
      headers: { Authorization: `Token ${token.value}` }
    })
      .then(() => {
        console.log('로그아웃 성공!')
      })
      .catch(err => {
        console.error('로그아웃 실패:', err)
      })
      .finally(() => {
        token.value = null
        user.value = null
        router.push({ name: 'ArticleView' })
      })
  }

  return {
    signUp,
    logIn,
    logOut,
    token,
    isLogin,
    user,
    fetchUser 
  }
}, { persist: true })