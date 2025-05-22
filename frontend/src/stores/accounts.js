// frontend/src/stores/accounts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('')
  const router = useRouter()
  const currentUser = ref(null) // 현재 로그인된 사용자 정보

  const isLogin = computed(() => !!token.value) // 간결하게 수정

  const signUp = function (payload) { // {username, password, password2, email, age}
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

  const logIn = function(payload) { // {username, password}
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: payload
    })
      .then(res => {
        token.value = res.data.key
        // 로그인 성공 후 사용자 정보 가져오기
        getUserProfile() 
        router.push({ name: 'ArticleView' })
      })
      .catch(err => {
        console.error('로그인 실패:', err.response ? err.response.data : err.message)
        alert(JSON.stringify(err.response?.data || '로그인 중 오류가 발생했습니다.'));
      })
  }

  const logOut = function () {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => { // res 사용 안 함
        token.value = ''
        currentUser.value = null // 사용자 정보 초기화
        console.log('로그아웃 성공!')
        router.push({ name: 'ArticleView' })
      })
      .catch(err => {
        console.error('로그아웃 실패:', err.response ? err.response.data : err.message)
        // 토큰 만료 등의 경우 클라이언트 측에서도 로그아웃 처리 강행
        token.value = ''
        currentUser.value = null
        router.push({ name: 'LogInView' }) // 로그인 페이지로 이동
      })
  }

  // 사용자 프로필 정보 가져오기
  const getUserProfile = function () {
    if (!token.value) return Promise.reject('No token found'); // 토큰 없으면 실행 안 함

    return axios({
      method: 'GET',
      url: `${ACCOUNT_API_URL}/user/`, // dj-rest-auth의 기본 사용자 정보 URL
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
        // 인증 실패 시 로그아웃 처리
        logOut();
      }
    })
  }

  // 사용자 프로필 정보 업데이트
  const updateUserProfile = function (payload) {
    if (!token.value) return Promise.reject('No token found');

    return axios({
      method: 'PUT', // 또는 PATCH
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: payload // { email, age, first_name, last_name, subscribed_products 등 }
    })
    .then(res => {
      currentUser.value = res.data
      console.log('사용자 정보 업데이트 성공:', currentUser.value)
      alert('프로필이 성공적으로 업데이트되었습니다.');
      // 필요시 router.push(...)
    })
    .catch(err => {
      console.error('사용자 정보 업데이트 실패:', err.response ? err.response.data : err.message)
      alert(JSON.stringify(err.response?.data || '프로필 업데이트 중 오류가 발생했습니다.'));
      throw err; // 에러를 다시 throw하여 컴포넌트에서 처리할 수 있도록 함
    })
  }


  return { 
    signUp, logIn, logOut, token, isLogin, ACCOUNT_API_URL, 
    currentUser, getUserProfile, updateUserProfile
  }
}, { persist: { storage: localStorage, paths: ['token', 'currentUser'] } }) // currentUser도 로컬 스토리지에 저장