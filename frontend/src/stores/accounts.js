// frontend/src/stores/accounts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('')
  const router = useRouter()
  const currentUser = ref(null) 

  const isLogin = computed(() => !!token.value)

  const signUp = function (payload) {
    console.log('Signing up with payload:', payload)
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: payload
    })
      .then(res => {
        console.log('회원가입 성공!', res.data)
        router.push({ name: 'LogInView' })
      })
      .catch(err => {
        console.error('회원가입 실패:', err.response ? err.response.data : err.message)
        alert(JSON.stringify(err.response?.data || '회원가입 중 오류가 발생했습니다.'));
      })
  }

  const logIn = function(payload) {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: payload
    })
      .then(res => {
        token.value = res.data.key
        getUserProfile() 
        router.push({ name: 'ArticleView' })
      })
      .catch(err => {
        console.error('로그인 실패:', err.response ? err.response.data : err.message)
        alert(JSON.stringify(err.response?.data || '로그인 중 오류가 발생했습니다.'));
      })
  }

  const logOut = function () {
    return new Promise((resolve, reject) => { // Promise 반환
      axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/logout/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
        .then(() => {
          token.value = ''
          currentUser.value = null
          console.log('로그아웃 성공! (상태 초기화)')
          // router.push({ name: 'ArticleView' }) // 여기서 내비게이션 제거
          resolve() // 성공 시 resolve
        })
        .catch(err => {
          console.error('로그아웃 실패:', err.response ? err.response.data : err.message)
          // 토큰 만료 등의 경우 클라이언트 측에서도 로그아웃 처리 강행
          token.value = ''
          currentUser.value = null
          // router.push({ name: 'LogInView' }) // 여기서 내비게이션 제거
          reject(err) // 실패 시 reject
        })
    })
  }

  const getUserProfile = function () {
    if (!token.value) return Promise.reject('No token found');

    return axios({
      method: 'GET',
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      currentUser.value = res.data
      console.log('사용자 정보 GET 성공:', currentUser.value)
    })
    .catch(err => {
      console.error('사용자 정보 GET 실패:', err.response ? err.response.data : err.message)
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        // 인증 실패 시 로그아웃 처리 (내비게이션은 호출부에서)
        // logOut(); // logOut 호출 후 내비게이션은 router/index.js 에서 담당
        return Promise.reject(err); // 에러를 다시 throw하여 router에서 처리
      }
      return Promise.reject(err); // 그 외 에러도 throw
    })
  }

  const updateUserProfile = function (payload) {
    if (!token.value) return Promise.reject('No token found');

    return axios({
      method: 'PUT',
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: payload
    })
    .then(res => {
      currentUser.value = res.data
      console.log('사용자 정보 업데이트 성공:', currentUser.value)
      alert('프로필이 성공적으로 업데이트되었습니다.');
    })
    .catch(err => {
      console.error('사용자 정보 업데이트 실패:', err.response ? err.response.data : err.message)
      alert(JSON.stringify(err.response?.data || '프로필 업데이트 중 오류가 발생했습니다.'));
      throw err; 
    })
  }


  return { 
    signUp, logIn, logOut, token, isLogin, ACCOUNT_API_URL, 
    currentUser, getUserProfile, updateUserProfile
  }
}, { persist: { storage: localStorage, paths: ['token', 'currentUser'] } })