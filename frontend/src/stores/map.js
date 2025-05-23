// frontend/src/stores/map.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useMapStore = defineStore('map', () => {
  const KAKAO_MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;
  const isMapSDKLoaded = ref(false);
  // const mapInstance = ref(null); // 필요시 지도 객체 저장용

  if (!KAKAO_MAP_API_KEY) {
    console.warn('VITE_KAKAO_MAP_API_KEY is not defined in .env file. Map features will be unavailable.');
  } else {
    console.log('Loaded API Key in mapStore:', KAKAO_MAP_API_KEY);
  }

  function loadKakaoMapSDK() {
    return new Promise((resolve, reject) => {
      if (!KAKAO_MAP_API_KEY) {
        const errorMsg = '카카오맵 API 키가 설정되지 않았습니다. 애플리케이션 설정을 확인해주세요.';
        console.error(errorMsg);
        alert(errorMsg);
        return reject(new Error('Kakao API Key is missing'));
      }

      // 이미 스크립트가 로드되었는지 확인 (중복 로드 방지)
      if (window.kakao && window.kakao.maps) {
        console.log('Kakao Maps SDK already loaded or script tag exists.');
        // autoload=false로 설정했으므로, 명시적으로 load 함수 호출 필요
        if (typeof window.kakao.maps.load === 'function' && !isMapSDKLoaded.value) {
          window.kakao.maps.load(() => {
            console.log('Kakao Maps SDK initialized (already loaded script).');
            isMapSDKLoaded.value = true;
            resolve(window.kakao);
          });
        } else if (isMapSDKLoaded.value) {
          resolve(window.kakao); // 이미 초기화 완료된 경우
        } else {
          // 스크립트는 있지만 load가 호출되지 않은 경우 (또는 이전 호출이 실패한 경우)
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
      // autoload=false로 설정하여 window.kakao.maps.load()를 통해 명시적으로 초기화
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_API_KEY}&libraries=services&autoload=false`;
      
      script.onload = () => {
        if (window.kakao && window.kakao.maps && typeof window.kakao.maps.load === 'function') {
          window.kakao.maps.load(() => {
            console.log('Kakao Maps SDK loaded and initialized via store.');
            isMapSDKLoaded.value = true;
            resolve(window.kakao); // Kakao SDK 객체를 resolve
          });
        } else {
          const errorMsg = 'Kakao Maps SDK loaded, but window.kakao.maps.load is not available.';
          console.error(errorMsg);
          alert('지도 서비스를 초기화하는 데 실패했습니다. 페이지를 새로고침 해보세요.');
          reject(new Error(errorMsg));
        }
      };
      script.onerror = (event) => {
        console.error('Failed to load Kakao Maps SDK script.', event);
        alert('지도 서비스 스크립트를 불러오는 데 실패했습니다. 네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.');
        reject(new Error('Failed to load Kakao Maps SDK script.'));
      };
      document.head.appendChild(script);
    });
  }

  return {
    KAKAO_MAP_API_KEY,
    isMapSDKLoaded,
    // mapInstance,
    loadKakaoMapSDK,
  };
});