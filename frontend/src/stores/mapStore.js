// frontend/src/stores/mapStore.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMapStore = defineStore('map', () => {
  const MAP_API_URL = 'http://127.0.0.1:8000/api/v1/maps'
  const kakaoApiKey = ref(null)
  const isSdkLoaded = ref(false)

  const fetchKakaoApiKey = async () => {
    try {
      const response = await axios.get(`${MAP_API_URL}/kakao-key/`)
      kakaoApiKey.value = response.data.kakao_api_key
      return kakaoApiKey.value
    } catch (error) {
      console.error('Failed to fetch Kakao API key:', error)
      return null
    }
  }

  const loadKakaoSdk = async () => {
    if (window.kakao && window.kakao.maps) {
      isSdkLoaded.value = true
      return Promise.resolve()
    }
    
    const key = kakaoApiKey.value || await fetchKakaoApiKey()
    if (!key) {
      console.error("Kakao API Key is not available. SDK cannot be loaded.")
      return Promise.reject("API Key unavailable")
    }

    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&libraries=services,clusterer,drawing&autoload=false`
      document.head.appendChild(script)
      script.onload = () => {
        window.kakao.maps.load(() => {
          console.log('Kakao Maps SDK loaded successfully.')
          isSdkLoaded.value = true
          resolve()
        })
      }
      script.onerror = () => {
        console.error('Failed to load Kakao Maps SDK.')
        reject()
      }
    })
  }

  return { kakaoApiKey, fetchKakaoApiKey, loadKakaoSdk, isSdkLoaded }
})