import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts';
  const token = ref(null);
  const user = ref(null);
  const router = useRouter();

  const isLogin = computed(() => !!token.value);

  // API 요청 에러 핸들러 유틸리티 함수
  const handleApiError = (error, contextMessage) => {
    console.error(`${contextMessage}:`, error);
    if (error.response) {
      // 서버가 상태 코드로 응답한 경우
      console.error('응답 데이터:', error.response.data);
      console.error('응답 상태 코드:', error.response.status);
      alert(`${contextMessage} 실패: ${JSON.stringify(error.response.data) || '서버 오류'}`);
    } else if (error.request) {
      // 요청은 이루어졌으나 응답을 받지 못한 경우
      console.error('요청 데이터:', error.request);
      alert(`${contextMessage} 실패: 서버에서 응답이 없습니다.`);
    } else {
      // 요청을 설정하는 중에 문제가 발생한 경우
      console.error('에러 메시지:', error.message);
      alert(`${contextMessage} 중 오류 발생: ${error.message}`);
    }
  };

  const fetchUser = async () => {
    if (!token.value) return;
    try {
      const response = await axios({
        method: 'GET',
        url: `${ACCOUNT_API_URL}/user/`,
        headers: { Authorization: `Token ${token.value}` },
      });
      user.value = response.data;
    } catch (err) {
      handleApiError(err, '사용자 정보 로딩');
      // 토큰이 유효하지 않을 수 있으므로 로그아웃 처리와 유사하게 상태 초기화
      token.value = null;
      user.value = null;
    }
  };

  const signUp = async (payload) => {
    try {
      await axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/signup/`,
        data: payload,
      });
      console.log('회원가입 성공!');
      alert('회원가입에 성공했습니다. 로그인 페이지로 이동합니다.');
      router.push({ name: 'LogInView' });
    } catch (err) {
      handleApiError(err, '회원가입');
    }
  };

  const logIn = async (payload) => {
    try {
      const res = await axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/login/`,
        data: payload,
      });
      token.value = res.data.key;
      await fetchUser(); // 로그인 직후 사용자 정보 가져오기
      router.push({ name: 'MainView' }); // 로그인 후 메인 페이지로 이동
    } catch (err) {
      handleApiError(err, '로그인');
    }
  };

  const logOut = async () => {
    if (!token.value) return; // 이미 로그아웃 상태이거나 토큰이 없는 경우
    try {
      await axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/logout/`,
        headers: { Authorization: `Token ${token.value}` },
      });
      console.log('로그아웃 성공!');
    } catch (err) {
      // 로그아웃 API 호출 실패 시에도 클라이언트 측 상태는 초기화
      handleApiError(err, '로그아웃 API 호출');
    } finally {
      token.value = null;
      user.value = null;
      router.push({ name: 'MainView' }); // 로그아웃 후 게시글 목록 페이지로 이동
    }
  };

  const updateUser = async (payload) => {
    if (!token.value) {
      alert('프로필을 수정하려면 로그인이 필요합니다.');
      router.push({ name: 'LogInView' });
      return;
    }
    try {
      const response = await axios({
        method: 'PUT',
        url: `${ACCOUNT_API_URL}/user/`,
        headers: { Authorization: `Token ${token.value}` },
        data: payload,
      });
      user.value = response.data; // 스토어의 user 상태를 서버로부터 받은 최신 정보로 업데이트
      alert('프로필 정보가 성공적으로 수정되었습니다.');
    } catch (err) {
      handleApiError(err, '프로필 정보 수정');
    }
  };

  return {
    token,
    user,
    isLogin,
    signUp,
    logIn,
    logOut,
    fetchUser,
    updateUser,
  };
}, { persist: true });