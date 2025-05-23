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

  function _loadSdkLogic() { // 내부 로직 함수로 변경
    // sdkLoadPromise가 이미 존재하고 완료되지 않았다면 반환 (중복 실행 방지)
    if (sdkLoadPromise.value && !isMapSDKLoaded.value) {
      return sdkLoadPromise.value;
    }
    if (isMapSDKLoaded.value) {
      return Promise.resolve(window.kakao);
    }

    sdkLoadPromise.value = new Promise((resolve, reject) => {
      // ... (이전과 동일한 SDK 로딩 로직) ...
      // 성공 시: isMapSDKLoaded.value = true; resolve(window.kakao);
      // 실패 시: reject(new Error(...));
      if (!KAKAO_MAP_API_KEY) {
        const errorMsg = '카카오맵 API 키가 설정되지 않았습니다. 애플리케이션 설정을 확인해주세요.';
        console.error(errorMsg);
        return reject(new Error('Kakao API Key is missing'));
      }

      // 이미 스크립트가 로드되었는지 확인
      if (window.kakao && window.kakao.maps) {
        // ... (중복 로드 처리 로직) ...
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

  // 스토어가 처음 인스턴스화될 때 SDK 로드를 자동으로 시작
  _loadSdkLogic().catch(error => {
    // 여기서 에러를 처리하거나, isMapSDKLoaded 상태를 통해 컴포넌트에서 처리하도록 할 수 있습니다.
    console.error('Kakao Maps SDK auto-load failed in store:', error);
  });

  return {
    KAKAO_MAP_API_KEY,
    isMapSDKLoaded, // 컴포넌트에서 이 상태를 구독하여 SDK 사용 가능 여부 확인
    getSdkLoadPromise: () => sdkLoadPromise.value || _loadSdkLogic(), // 필요시 Promise를 얻을 수 있는 함수
  };
});