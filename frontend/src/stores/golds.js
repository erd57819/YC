// frontend/src/stores/golds.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useGoldStore = defineStore('golds', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const goldData = ref(null)
  const silverData = ref(null)

  // 금 시세 데이터 가져오기
  const fetchGoldData = async () => {
    try {
      const response = await axios.get(`${API_URL}/golds/`)
      goldData.value = response.data
    } catch (error) {
      console.error('금 시세 데이터를 불러오는 데 실패했습니다.', error)
    }
  }

  // 은 시세 데이터 가져오기
  const fetchSilverData = async () => {
    try {
      const response = await axios.get(`${API_URL}/golds/silver/`)
      silverData.value = response.data
    } catch (error) {
      console.error('은 시세 데이터를 불러오는 데 실패했습니다.', error)
    }
  }

  return {
    goldData,
    silverData,
    fetchGoldData,
    fetchSilverData
  }
})