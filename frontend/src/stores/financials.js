import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';

export const useFinancialStore = defineStore('financial', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const depositProducts = ref([]);
  const savingProducts = ref([]);
  const depositProduct = ref(null);
  const savingProduct = ref(null);
  const banks = ref([]);
  const dclsMonths = ref([]);

  const loadInitialData = async () => {
    try {
      await axios.get(`${API_URL}/financials/save-products/`);
      console.log('초기 금융 데이터 로드 성공!');
    } catch (error) {
      console.error('초기 금융 데이터 로드 실패:', error);
    }
  };

  const fetchBankInfo = async () => {
    try {
      const response = await axios.get('/data.json');
      banks.value = response.data.bankInfo;
    } catch (error) {
      console.error('은행 정보를 불러오는 데 실패했습니다.', error);
    }
  };

  const fetchDepositProducts = async (params = {}) => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/`, { params });
      depositProducts.value = response.data;
      const months = new Set();
      depositProducts.value.forEach(product => {
        if (product.dcls_month) {
          months.add(product.dcls_month);
        }
      });
      dclsMonths.value = Array.from(months).sort((a, b) => b.localeCompare(a));
    } catch (error) {
      console.error('예금 상품 목록을 불러오는 데 실패했습니다.', error);
    }
  };

  const fetchSavingProducts = async (params = {}) => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/`, { params });
      savingProducts.value = response.data;
      const months = new Set();
      savingProducts.value.forEach(product => {
        if (product.dcls_month) {
          months.add(product.dcls_month);
        }
      });
      dclsMonths.value = Array.from(months).sort((a, b) => b.localeCompare(a));
    } catch (error) {
      console.error('적금 상품 목록을 불러오는 데 실패했습니다.', error);
    }
  };

  const fetchDepositProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/${id}/`);
      depositProduct.value = response.data;
    } catch (error) {
      console.error('예금 상품 상세 정보를 불러오는 데 실패했습니다.', error);
      depositProduct.value = null;
    }
  };

  const fetchSavingProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/${id}/`);
      savingProduct.value = response.data;
    } catch (error) {
      console.error('적금 상품 상세 정보를 불러오는 데 실패했습니다.', error);
      savingProduct.value = null;
    }
  };

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
      accountStore.fetchUser(); // 가입 후 사용자 정보 갱신
    } catch (error) {
      console.error('예금 상품 가입 실패:', error.response?.data || error.message);
      alert(`예금 상품 가입 실패: ${error.response?.data?.detail || error.message}`);
    }
  };

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
      accountStore.fetchUser(); // 가입 후 사용자 정보 갱신
    } catch (error) {
      console.error('적금 상품 가입 실패:', error.response?.data || error.message);
      alert(`적금 상품 가입 실패: ${error.response?.data?.detail || error.message}`);
    }
  };

  // 상품 가입 취소(삭제) 함수
  const deleteSubscription = async (type, subscriptionId) => {
    const accountStore = useAccountStore();
    if (!accountStore.token) {
      alert('로그인이 필요합니다.');
      return;
    }

    // type이 'deposit' 또는 'saving'인지 확인합니다.
    // UserDeposit, UserSaving 모델의 pk를 subscriptionId로 받습니다.
    const typeName = type === 'deposit' ? '예금' : '적금';
    const url = `${API_URL}/financials/subscriptions/${type}s/${subscriptionId}/`; // URL 경로 수정 ('deposit' -> 'deposits')

    try {
      await axios.delete(url, {
        headers: { Authorization: `Token ${accountStore.token}` },
      });
      alert(`${typeName} 상품 가입을 취소했습니다.`);
      // 데이터 갱신을 위해 사용자 정보를 다시 불러옵니다.
      accountStore.fetchUser(); 
    } catch (error) {
      console.error(`${typeName} 상품 취소 실패:`, error.response?.data || error.message);
      alert(`${typeName} 상품 취소에 실패했습니다: ${error.response?.data?.detail || error.message}`);
    }
  };

  return {
    API_URL, // API_URL도 반환 객체에 포함하는 것이 좋습니다 (이미 있다면 중복 X)
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
    deleteSubscription, // 이 함수가 반환 객체에 포함되어 있는지 확인!
  };
}, { persist: true });