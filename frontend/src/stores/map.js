// frontend/src/stores/map.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useMapStore = defineStore('map', () => {
  const KAKAO_MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;
  const isMapSDKLoaded = ref(false);
  const sdkLoadPromise = ref(null);

  if (!KAKAO_MAP_API_KEY) {
    console.warn('VITE_KAKAO_MAP_API_KEY is not defined in .env file. Map features will be unavailable.');
  } else {
    console.log('Loaded API Key in mapStore:', KAKAO_MAP_API_KEY);
  }

  function _loadSdkLogic() { 
    if (sdkLoadPromise.value && !isMapSDKLoaded.value) {
      return sdkLoadPromise.value;
    }
    if (isMapSDKLoaded.value) {
      return Promise.resolve(window.kakao);
    }

    sdkLoadPromise.value = new Promise((resolve, reject) => {
      if (!KAKAO_MAP_API_KEY) {
        const errorMsg = '카카오맵 API 키가 설정되지 않았습니다. 애플리케이션 설정을 확인해주세요.';
        console.error(errorMsg);
        return reject(new Error('Kakao API Key is missing'));
      }

      if (window.kakao && window.kakao.maps) {

        if (typeof window.kakao.maps.load === 'function' && !isMapSDKLoaded.value) {
          window.kakao.maps.load(() => {
            console.log('Kakao Maps SDK initialized (already loaded script).');
            isMapSDKLoaded.value = true;
            resolve(window.kakao);
          });
        } else if (isMapSDKLoaded.value) {
          resolve(window.kakao);
        } else {
           window.kakao.maps.load(() => {
            console.log('Kakao Maps SDK initialized (attempting load on existing script).');
            isMapSDKLoaded.value = true;
            resolve(window.kakao);
          });
        }
        return;
      }
      
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_API_KEY}&libraries=services&autoload=false`;
      script.onload = () => {
        if (window.kakao && window.kakao.maps && typeof window.kakao.maps.load === 'function') {
          window.kakao.maps.load(() => {
            console.log('Kakao Maps SDK loaded and initialized via store.');
            isMapSDKLoaded.value = true;
            resolve(window.kakao);
          });
        } else {
          const errorMsg = 'Kakao Maps SDK loaded, but window.kakao.maps.load is not available.';
          console.error(errorMsg);
          reject(new Error(errorMsg));
        }
      };
      script.onerror = (event) => {
        console.error('Failed to load Kakao Maps SDK script.', event);
        reject(new Error('Failed to load Kakao Maps SDK script.'));
      };
      document.head.appendChild(script);
    });
    return sdkLoadPromise.value;
  }

  _loadSdkLogic().catch(error => {
    console.error('Kakao Maps SDK auto-load failed in store:', error);
  });

  return {
    KAKAO_MAP_API_KEY,
    isMapSDKLoaded, 
    getSdkLoadPromise: () => sdkLoadPromise.value || _loadSdkLogic(), 
  };
});