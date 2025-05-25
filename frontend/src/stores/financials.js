import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useFinancialStore = defineStore('financial', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const depositProducts = ref([]);
  const savingProducts = ref([]);
  const depositProduct = ref(null);
  const savingProduct = ref(null);

  const fetchDepositProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/`);
      depositProducts.value = response.data;
    } catch (error) {
      console.error('Error fetching deposit products:', error);
    }
  };

  const fetchSavingProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/`);
      savingProducts.value = response.data;
    } catch (error) {
      console.error('Error fetching saving products:', error);
    }
  };

  const fetchDepositProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/deposit-products/${id}/`);
      depositProduct.value = response.data;
    } catch (error) {
      console.error('Error fetching deposit product detail:', error);
    }
  };

  const fetchSavingProductDetail = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/financials/saving-products/${id}/`);
      savingProduct.value = response.data;
    } catch (error) {
      console.error('Error fetching saving product detail:', error);
    }
  };
  
  // 데이터베이스 초기 데이터 로드 함수
  const loadInitialData = async () => {
    try {
      await axios.get(`${API_URL}/financials/save-products/`);
      console.log('초기 금융 데이터 로드 성공!');
    } catch (error) {
      console.error('초기 금융 데이터 로드 실패:', error);
    }
  };

  return {
    depositProducts,
    savingProducts,
    depositProduct,
    savingProduct,
    fetchDepositProducts,
    fetchSavingProducts,
    fetchDepositProductDetail,
    fetchSavingProductDetail,
    loadInitialData,
  };
}, { persist: true });
