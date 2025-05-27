// frontend/src/stores/financials.js
import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts'; // 계정 스토어 임포트

export const useFinancialStore = defineStore('financial', () => {
  const API_URL = 'http://127.0.0.1:8000'; // 백엔드 API 기본 URL
  const depositProducts = ref([]); //
  const savingProducts = ref([]); //
  const depositProduct = ref(null); //
  const savingProduct = ref(null); //
  const banks = ref([]); // 은행 목록 상태
  const dclsMonths = ref([]); // 공시월 목록 상태
  const recommendedProducts = ref([]); // AI 추천 상품 목록 상태 추가

  // 금융감독원 API 데이터 로드 (DB 저장 요청)
  const loadInitialData = async () => { //
    try {
      await axios.get(`${API_URL}/financials/save-products/`); //
      console.log('초기 금융 데이터 로드 성공!'); //
    } catch (error) {
      console.error('초기 금융 데이터 로드 실패:', error); //
    }
  };

  // 은행 정보 로드 (public/data.json)
  const fetchBankInfo = async () => { //
    try {
      const response = await axios.get('/data.json'); // public 폴더의 data.json 경로
      banks.value = response.data.bankInfo; //
    } catch (error) {
      console.error('은행 정보를 불러오는 데 실패했습니다.', error); //
    }
  };

  // 예금 상품 목록 (필터링 포함)
  const fetchDepositProducts = async (params = {}) => { //
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/`, { params }); //
      depositProducts.value = response.data; //
      const months = new Set(response.data.map(p => p.dcls_month).filter(Boolean)); //
      const currentMonths = new Set(dclsMonths.value);
      months.forEach(month => currentMonths.add(month));
      dclsMonths.value = Array.from(currentMonths).sort((a, b) => b.localeCompare(a)); //
    } catch (error) {
      console.error('예금 상품 목록을 불러오는 데 실패했습니다.', error); //
      depositProducts.value = [];
    }
  };

  // 적금 상품 목록 (필터링 포함)
  const fetchSavingProducts = async (params = {}) => { //
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/`, { params }); //
      savingProducts.value = response.data; //
      const months = new Set(response.data.map(p => p.dcls_month).filter(Boolean)); //
      const currentMonths = new Set(dclsMonths.value);
      months.forEach(month => currentMonths.add(month));
      dclsMonths.value = Array.from(currentMonths).sort((a, b) => b.localeCompare(a)); //
    } catch (error) {
      console.error('적금 상품 목록을 불러오는 데 실패했습니다.', error); //
      savingProducts.value = [];
    }
  };
  
  // 예금 상품 상세
  const fetchDepositProductDetail = async (id) => { //
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/${id}/`); //
      depositProduct.value = response.data; //
    } catch (error) {
      console.error(`예금 상품 상세(${id}) 정보를 불러오는 데 실패했습니다.`, error); //
      depositProduct.value = null; //
    }
  };

  // 적금 상품 상세
  const fetchSavingProductDetail = async (id) => { //
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/${id}/`); //
      savingProduct.value = response.data; //
    } catch (error) {
      console.error(`적금 상품 상세(${id}) 정보를 불러오는 데 실패했습니다.`, error); //
      savingProduct.value = null; //
    }
  };

  // 상품 가입 공통 에러 처리 함수
  const handleSubscriptionError = (error, productType) => { //
    console.error(`${productType} 상품 가입 실패:`, error.response?.data || error.message); //
    const errorData = error.response?.data;
    let alertMessage = `${productType} 상품 가입에 실패했습니다.`; //
    if (errorData && typeof errorData === 'object' && !Array.isArray(errorData)) {
        for (const key in errorData) {
            alertMessage += `\n- ${key}: ${errorData[key].join ? errorData[key].join(', ') : errorData[key]}`;
        }
    } else if (typeof errorData === 'string') {
        alertMessage += `\n서버 메시지: ${errorData}`;
    } else if (error.message) {
        alertMessage += `\n에러: ${error.message}`;
    }
    alert(alertMessage); //
    return Promise.reject(errorData || error.message);
  }

  // 예금 상품 가입
  const subscribeDepositProduct = async (productId, payload) => { //
    const accountStore = useAccountStore(); //
    if (!accountStore.token) { //
      alert('로그인이 필요합니다.'); //
      return Promise.reject('로그인 필요');
    }
    try {
      const response = await axios.post(`${API_URL}/financials/deposit-products/${productId}/subscribe/`, payload, { //
        headers: { Authorization: `Token ${accountStore.token}` }, //
      });
      alert('예금 상품 가입이 완료되었습니다!'); //
      return response.data;
    } catch (error) {
      return handleSubscriptionError(error, '예금'); //
    }
  };

  // 적금 상품 가입
  const subscribeSavingProduct = async (productId, payload) => { //
    const accountStore = useAccountStore(); //
    if (!accountStore.token) { //
      alert('로그인이 필요합니다.'); //
      return Promise.reject('로그인 필요');
    }
    try {
      const response = await axios.post(`${API_URL}/financials/saving-products/${productId}/subscribe/`, payload, { //
        headers: { Authorization: `Token ${accountStore.token}` }, //
      });
      alert('적금 상품 가입이 완료되었습니다!'); //
      return response.data;
    } catch (error) {
      return handleSubscriptionError(error, '적금'); //
    }
  };

  // AI 추천 상품 목록 가져오기
  const fetchAIRecommendations = async () => {
    const accountStore = useAccountStore();
    if (!accountStore.isLogin || !accountStore.token) {
      recommendedProducts.value = []; // 로그인이 되어있지 않으면, 추천 목록을 비웁니다.
      return; // 함수 실행 중단
    }
    try {
      const response = await axios.get(`${API_URL}/financials/ai-recommendations/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      recommendedProducts.value = response.data;
    } catch (error) {
      console.error('AI 추천 상품을 불러오는 데 실패했습니다.', error.response?.data || error.message);
      recommendedProducts.value = []; // 오류 발생 시 추천 목록을 비웁니다.
    }
  };

  return {
    API_URL,
    depositProducts, //
    savingProducts, //
    depositProduct, //
    savingProduct, //
    banks, //
    dclsMonths, //
    recommendedProducts,
    loadInitialData, //
    fetchBankInfo, //
    fetchDepositProducts, //
    fetchSavingProducts, //
    fetchDepositProductDetail, //
    fetchSavingProductDetail, //
    subscribeDepositProduct, //
    subscribeSavingProduct, //
    fetchAIRecommendations,
  };
}, { persist: true }); //