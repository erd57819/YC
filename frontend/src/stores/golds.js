// frontend/src/stores/golds.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useGoldStore = defineStore('golds', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const goldData = ref([])
  const silverData = ref([])

  // 금 시세 데이터 가져오기 (기간 필터링)
  const fetchGoldData = async (startDate = null, endDate = null) => {
    try {
      const params = (startDate && endDate) ? { start_date: startDate, end_date: endDate } : {}
      const response = await axios.get(`${API_URL}/golds/`, { params })
      goldData.value = response.data
    } catch (error) {
      console.error('금 시세 데이터를 불러오는 데 실패했습니다.', error)
      goldData.value = []
    }
  }

  // 은 시세 데이터 가져오기 (기간 필터링)
  const fetchSilverData = async (startDate = null, endDate = null) => {
    try {
      const params = (startDate && endDate) ? { start_date: startDate, end_date: endDate } : {}
      const response = await axios.get(`${API_URL}/golds/silver/`, { params })
      silverData.value = response.data
    } catch (error) {
      console.error('은 시세 데이터를 불러오는 데 실패했습니다.', error)
      silverData.value = []
    }
  }

  return {
    goldData,
    silverData,
    fetchGoldData,
    fetchSilverData
  }
})