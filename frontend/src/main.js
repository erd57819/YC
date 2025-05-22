import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 카카오맵 API 키 가져오기
const KAKAO_MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;
console.log('Loaded API Key from .env:', KAKAO_MAP_API_KEY)

// 카카오맵 SDK 로드 함수
function loadKakaoMapSDK(apiKey, callback) {
  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services&autoload=false`; // autoload=false로 설정
  script.onload = () => {
    // window.kakao.maps.load 함수를 사용하여 지도 API 초기화
    if (window.kakao && window.kakao.maps && typeof window.kakao.maps.load === 'function') {
      window.kakao.maps.load(callback);
    } else {
      console.error('Kakao Maps SDK loaded, but window.kakao.maps.load is not available.');
      // 여기서 사용자에게 알림을 줄 수도 있습니다.
      alert('지도 서비스를 초기화하는 데 실패했습니다. 페이지를 새로고침 해보세요.');
    }
  };
  script.onerror = () => {
    console.error('Failed to load Kakao Maps SDK script.');
    alert('지도 서비스 스크립트를 불러오는 데 실패했습니다. 네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.');
  };
  document.head.appendChild(script);
}

const app = createApp(App)
const pinia = createPinia()
// pinia-plugin-persistedstate 사용 부분은 이전 단계에서 제거했으므로 생략

app.use(pinia)
app.use(router)

// 카카오맵 SDK 로드 후 앱 마운트
if (KAKAO_MAP_API_KEY) {
  loadKakaoMapSDK(KAKAO_MAP_API_KEY, () => {
    console.log('Kakao Maps SDK loaded and initialized.');
    app.mount('#app');
  });
} else {
  console.error('VITE_KAKAO_MAP_API_KEY is not defined in .env file');
  alert('카카오맵 API 키가 설정되지 않았습니다. 애플리케이션 설정을 확인해주세요.');
  // API 키가 없으면 지도 기능이 동작하지 않으므로, 여기서 앱을 마운트하거나
  // 사용자에게 심각한 오류임을 알리는 페이지를 보여줄 수 있습니다.
  // 일단은 마운트는 하지만, 지도 기능은 동작하지 않을 것입니다.
  app.mount('#app');
}