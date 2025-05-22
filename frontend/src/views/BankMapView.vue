<template>
  <div class="container mt-4">
    <h2>근처 은행 찾기 [cite: 77]</h2>
    <div class="row mb-3">
      <div class="col-md-4">
        <input type="text" class="form-control" v-model="searchKeyword" placeholder="지역 또는 은행명 입력 (예: 강남구 우리은행) [cite: 78]">
      </div>
      <div class="col-md-2">
        <button class="btn btn-primary w-100" @click="searchPlaces">은행 검색</button>
      </div>
    </div>
    <div id="map" style="width:100%;height:500px;"></div>
    <div v-if="searchResults.length" class="mt-3">
      <h4>검색 결과:</h4>
      <ul class="list-group">
        <li v-for="place in searchResults" :key="place.id" class="list-group-item">
          <h5>{{ place.place_name }}</h5>
          <p>{{ place.road_address_name || place.address_name }}</p>
          <p v-if="place.phone">전화번호: {{ place.phone }}</p>
        </li>
      </ul>
    </div>
     <div v-if="!mapStore.isSdkLoaded && !initializationError" class="alert alert-info mt-3">
      지도를 로드 중입니다... API 키 설정을 확인해주세요.
    </div>
    <div v-if="initializationError" class="alert alert-danger mt-3">
      {{ initializationError }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMapStore } from '@/stores/mapStore' //

const mapStore = useMapStore()
const mapInstance = ref(null) // 카카오맵 인스턴스
const searchKeyword = ref('') // 검색어
const searchResults = ref([]) // 검색 결과 목록
const markers = ref([]) // 지도에 표시된 마커들
const placesService = ref(null) // Places 서비스 객체
const initializationError = ref(null); // 초기화 오류 메시지

onMounted(async () => {
  try {
    initializationError.value = null;
    // mapStore에서 SDK 로드가 완료될 때까지 기다립니다.
    await mapStore.loadKakaoSdk(); // loadKakaoSdk가 Promise를 반환하고 완료를 기다림
    
    if (mapStore.isSdkLoaded) {
      initializeMap();
    } else {
      // SDK 로드 실패에 대한 추가적인 사용자 알림이나 처리가 필요할 수 있습니다.
      console.error("카카오맵 SDK 로드 후에도 isSdkLoaded가 false입니다.");
      initializationError.value = "지도 서비스를 로드하는 데 실패했습니다. (SDK 로드 실패). 잠시 후 다시 시도해주세요.";
      // alert("지도 서비스를 로드하는 데 실패했습니다. (SDK 로드 실패). 잠시 후 다시 시도해주세요.");
    }
  } catch (error) {
    console.error("카카오맵 SDK 로드 중 에러 발생:", error);
    initializationError.value = "지도 서비스를 로드하는 데 실패했습니다. API 키 또는 네트워크 연결을 확인해주세요.";
    // alert("지도 서비스를 로드하는 데 실패했습니다. API 키 또는 네트워크 연결을 확인해주세요.");
  }
});

const initializeMap = () => {
  if (window.kakao && window.kakao.maps && window.kakao.maps.Map) {
    const container = document.getElementById('map');
    if (!container) {
      console.error("'map' ID를 가진 DOM 요소를 찾을 수 없습니다.");
      initializationError.value = "지도를 표시할 DOM 요소를 찾을 수 없습니다.";
      // alert("지도를 표시할 DOM 요소를 찾을 수 없습니다.");
      return;
    }
    const options = {
      center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 초기 중심 서울 시청
      level: 5
    };
    mapInstance.value = new window.kakao.maps.Map(container, options);

    if (window.kakao.maps.services && window.kakao.maps.services.Places) {
      placesService.value = new window.kakao.maps.services.Places();
    } else {
      console.error("kakao.maps.services.Places 객체를 사용할 수 없습니다. SDK 로드 시 'services' 라이브러리가 포함되었는지 확인하세요.");
      initializationError.value = "장소 검색 서비스를 초기화할 수 없습니다.";
      // alert("장소 검색 서비스를 초기화할 수 없습니다.");
    }
  } else {
    console.error("Kakao Maps SDK가 제대로 로드되지 않았거나 Map 객체를 사용할 수 없습니다.");
    initializationError.value = "지도 초기화에 실패했습니다. SDK가 올바르게 로드되지 않았습니다.";
    // alert("지도 초기화에 실패했습니다. SDK가 올바르게 로드되지 않았습니다.");
  }
};

const searchPlaces = () => {
  if (!searchKeyword.value.trim()) {
    alert('검색어를 입력해주세요.');
    return;
  }
  if (!mapInstance.value) {
    alert('지도가 아직 초기화되지 않았습니다. 잠시 후 다시 시도해주세요.');
    return;
  }
  if (!placesService.value) {
     alert('장소 검색 서비스 사용이 불가능합니다. 지도 초기화 상태를 확인해주세요.');
     return;
  }

  // 기존 마커 및 검색 결과 초기화
  removeMarkers();
  searchResults.value = [];

  placesService.value.keywordSearch(searchKeyword.value, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      searchResults.value = data;
      displayPlaces(data);
      if (data.length > 0) {
        const bounds = new window.kakao.maps.LatLngBounds();
        data.forEach(place => bounds.extend(new window.kakao.maps.LatLng(place.y, place.x)));
        mapInstance.value.setBounds(bounds);
      }
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 존재하지 않습니다.');
    } else if (status === window.kakao.maps.services.Status.ERROR) {
      alert('검색 중 오류가 발생했습니다.');
    }
  });
};

const displayPlaces = (places) => {
  places.forEach(place => {
    const markerPosition = new window.kakao.maps.LatLng(place.y, place.x);
    const marker = new window.kakao.maps.Marker({
      map: mapInstance.value,
      position: markerPosition
    });
    markers.value.push(marker);

    // 마커에 클릭이벤트를 등록합니다
    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:5px;font-size:12px;min-width:150px;">${place.place_name}</div>`,
      removable: true // 인포윈도우를 닫을 수 있는 x 버튼 추가 (선택 사항)
    });

    window.kakao.maps.event.addListener(marker, 'click', function() {
      infowindow.open(mapInstance.value, marker);
    });
  });
};

const removeMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];
};

</script>

<style scoped>
#map {
  border: 1px solid #ccc;
}
.list-group-item h5 {
  margin-bottom: 0.25rem;
}
.list-group-item p {
  margin-bottom: 0.1rem;
  font-size: 0.9rem;
}
</style>