import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts'; // accounts 스토어 임포트 추가

export const useFinancialStore = defineStore('financial', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const depositProducts = ref([]);
  const savingProducts = ref([]);
  const depositProduct = ref(null);
  const savingProduct = ref(null);
  const banks = ref([]); // 은행 목록 상태 추가
  const dclsMonths = ref([]); // 공시월 목록 상태 추가

  // 금융감독원 API에서 상품 데이터를 가져와 DB에 저장하는 함수 (백엔드 호출)
  const loadInitialData = async () => {
    try {
      await axios.get(`${API_URL}/financials/save-products/`);
      console.log('초기 금융 데이터 로드 성공!');
    } catch (error) {
      console.error('초기 금융 데이터 로드 실패:', error);
    }
  };

  // public/data.json에서 은행 정보를 가져오는 함수
  const fetchBankInfo = async () => {
    try {
      const response = await axios.get('/data.json'); // public 폴더의 data.json 경로
      banks.value = response.data.bankInfo;
    } catch (error) {
      console.error('은행 정보를 불러오는 데 실패했습니다.', error);
    }
  };

  // 예금 상품 목록을 가져오는 함수 (필터링 적용 가능)
  const fetchDepositProducts = async (params = {}) => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/`, { params });
      depositProducts.value = response.data;
      // 응답 데이터에서 고유한 공시월을 추출하여 dclsMonths 업데이트
      const months = new Set();
      depositProducts.value.forEach(product => {
        if (product.dcls_month) {
          months.add(product.dcls_month);
        }
      });
      dclsMonths.value = Array.from(months).sort((a, b) => b.localeCompare(a)); // 최신 월이 먼저 오도록 정렬
    } catch (error) {
      console.error('예금 상품 목록을 불러오는 데 실패했습니다.', error);
    }
  };

  // 적금 상품 목록을 가져오는 함수 (필터링 적용 가능)
  const fetchSavingProducts = async (params = {}) => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/`, { params });
      savingProducts.value = response.data;
      // 응답 데이터에서 고유한 공시월을 추출하여 dclsMonths 업데이트
      const months = new Set();
      savingProducts.value.forEach(product => {
        if (product.dcls_month) {
          months.add(product.dcls_month);
        }
      });
      dclsMonths.value = Array.from(months).sort((a, b) => b.localeCompare(a)); // 최신 월이 먼저 오도록 정렬
    } catch (error) {
      console.error('적금 상품 목록을 불러오는 데 실패했습니다.', error);
    }
  };

  // 특정 예금 상품 상세 정보를 가져오는 함수
  const fetchDepositProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/${id}/`);
      depositProduct.value = response.data;
    } catch (error) {
      console.error('예금 상품 상세 정보를 불러오는 데 실패했습니다.', error);
      depositProduct.value = null; // 오류 발생 시 상세 정보 초기화
    }
  };

  // 특정 적금 상품 상세 정보를 가져오는 함수
  const fetchSavingProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/${id}/`);
      savingProduct.value = response.data;
    } catch (error) {
      console.error('적금 상품 상세 정보를 불러오는 데 실패했습니다.', error);
      savingProduct.value = null; // 오류 발생 시 상세 정보 초기화
    }
  };

  // 예금 상품 가입 함수
  const subscribeDepositProduct = async (productId, payload) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) {
      alert('로그인이 필요합니다.');
      return;
    }
    try {
      await axios.post(`${API_URL}/financials/deposit-products/${productId}/subscribe/`, payload, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      alert('예금 상품 가입이 완료되었습니다!');
    } catch (error) {
      console.error('예금 상품 가입 실패:', error.response?.data || error.message);
      alert(`예금 상품 가입 실패: ${error.response?.data?.detail || error.message}`);
    }
  };

  // 적금 상품 가입 함수
  const subscribeSavingProduct = async (productId, payload) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) {
      alert('로그인이 필요합니다.');
      return;
    }
    try {
      await axios.post(`${API_URL}/financials/saving-products/${productId}/subscribe/`, payload, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      alert('적금 상품 가입이 완료되었습니다!');
    } catch (error) {
      console.error('적금 상품 가입 실패:', error.response?.data || error.message);
      alert(`적금 상품 가입 실패: ${error.response?.data?.detail || error.message}`);
    }
  };

  return {
    depositProducts,
    savingProducts,
    depositProduct,
    savingProduct,
    banks,
    dclsMonths,
    fetchDepositProducts,
    fetchSavingProducts,
    fetchDepositProductDetail,
    fetchSavingProductDetail,
    loadInitialData,
    fetchBankInfo,
    subscribeDepositProduct,
    subscribeSavingProduct,
  };
}, { persist: true });