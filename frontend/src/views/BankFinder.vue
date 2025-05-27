<template>
  <div class="bank-finder-container">
    <div class="controls-panel">
      <h2 class="panel-title">은행 찾기</h2>
      
      <div class="form-group">
        <label for="city">시/도 선택:</label>
        <select id="city" v-model="selectedCity" @change="onCityChange" class="form-select">
          <option value="">시/도를 선택하세요</option>
          <option v-for="city in cities" :key="city.name" :value="city.name">
            {{ city.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="district">시/군/구 선택:</label>
        <select id="district" v-model="selectedDistrict" class="form-select" :disabled="!selectedCity">
          <option value="">시/군/구를 선택하세요</option>
          <option v-for="district in districts" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="bank">은행 선택:</label>
        <select id="bank" v-model="selectedBank" class="form-select">
          <option value="">은행을 선택하세요</option>
          <option v-for="bankName in bankList" :key="bankName" :value="bankName">
            {{ bankName }}
          </option>
        </select>
      </div>

      <button @click="searchBankBranches" class="search-button" :disabled="!selectedCity || !selectedDistrict || !selectedBank">
        선택 지점 검색
      </button>
    </div>

    <div class="map-results-panel">
      <div id="kakaoMap" class="map-container">
        <div v-if="!mapStore.isMapSDKLoaded && !sdkLoadError" class="map-loading">
          지도를 불러오는 중입니다...
        </div>
        <div v-if="sdkLoadError" class="map-error">
          지도 SDK를 불러오는 데 실패했습니다. API 키를 확인하거나 네트워크 연결을 점검해주세요.
        </div>
      </div>
      <div class="results-list-container">
        <h3 v-if="places.length > 0" class="results-title">검색 결과 ({{ places.length }}건)</h3>
        <ul v-if="places.length > 0" class="results-list">
          <li v-for="(place, index) in places" :key="index" @click="panTo(place.y, place.x)" class="result-item">
            <h4>{{ place.place_name }}</h4>
            <p v-if="place.road_address_name">주소: {{ place.road_address_name }}</p>
            <p v-else-if="place.address_name">주소: {{ place.address_name }}</p>
            <p v-if="place.phone">전화번호: {{ place.phone }}</p>
          </li>
        </ul>
        <div v-if="!isLoading && searched && places.length === 0" class="no-results">
          선택하신 조건에 맞는 은행 지점이 없습니다.
        </div>
        <div v-if="isLoading" class="loading-results">
          지점을 검색 중입니다...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useMapStore } from '@/stores/map';

const mapStore = useMapStore();

const cities = ref([]);
const bankList = ref([]);
const selectedCity = ref('');
const selectedDistrict = ref('');
const selectedBank = ref('');
const districts = ref([]);

let kakaoMap = null;
let placesService = null;
let markers = [];
const places = ref([]);
const isLoading = ref(false);
const searched = ref(false); // 검색 시도 여부
const sdkLoadError = ref(false); // SDK 로드 에러 상태

// 데이터 로드 (public/data.json)
async function loadSelectData() {
  try {
    const response = await fetch('/data.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    cities.value = data.mapInfo;
    bankList.value = data.bankInfo;
  } catch (error) {
    console.error("Failed to load data.json:", error);
    // 사용자에게 알림을 줄 수도 있습니다.
  }
}

function onCityChange() {
  selectedDistrict.value = ''; // 시/군/구 선택 초기화
  const cityData = cities.value.find(c => c.name === selectedCity.value);
  districts.value = cityData ? cityData.countries : [];
}

async function initializeMap() {
  if (!mapStore.isMapSDKLoaded) {
    try {
      await mapStore.getSdkLoadPromise(); // SDK 로드 기다리기
    } catch (error) {
      console.error("BankFinder: Kakao Maps SDK failed to load in store.", error);
      sdkLoadError.value = true;
      return;
    }
  }
  
  // window.kakao와 window.kakao.maps가 정의되었는지 확인
  if (window.kakao && window.kakao.maps) {
    const mapContainer = document.getElementById('kakaoMap');
    if (!mapContainer) {
        console.error("BankFinder: Map container not found.");
        sdkLoadError.value = true;
        return;
    }
    const mapOption = {
      center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 기본 중심: 서울 시청
      level: 7,
    };
    kakaoMap = new window.kakao.maps.Map(mapContainer, mapOption);
    placesService = new window.kakao.maps.services.Places(kakaoMap);
    sdkLoadError.value = false;
  } else {
    console.error("BankFinder: Kakao Maps SDK not available on window object after load.");
    sdkLoadError.value = true;
  }
}


function searchBankBranches() {
  if (!selectedCity.value || !selectedDistrict.value || !selectedBank.value) {
    alert('모든 검색 조건을 선택해주세요.');
    return;
  }
  if (!placesService) {
    alert('지도 서비스가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.');
    console.error("Places service is not initialized.");
    return;
  }

  isLoading.value = true;
  searched.value = true;
  places.value = [];
  removeMarkers();

  const query = `${selectedCity.value} ${selectedDistrict.value} ${selectedBank.value}`;
  
  placesService.keywordSearch(query, (data, status, pagination) => {
    isLoading.value = false;
    if (status === window.kakao.maps.services.Status.OK) {
      places.value = data;
      displayMarkers(data);
      if (data.length > 0) {
        // 첫 번째 검색 결과로 지도 중심 이동
        const firstPlace = data[0];
        const moveLatLng = new window.kakao.maps.LatLng(firstPlace.y, firstPlace.x);
        kakaoMap.setCenter(moveLatLng);
        kakaoMap.setLevel(5); // 확대 레벨 조정
      }
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      // 검색 결과 없음 처리
    } else {
      console.error("장소 검색 중 오류 발생:", status);
      alert("장소 검색 중 오류가 발생했습니다.");
    }
  }, { size: 15 }); // 한 페이지에 15개 결과 요청
}

function displayMarkers(placesData) {
  placesData.forEach(place => {
    const markerPosition = new window.kakao.maps.LatLng(place.y, place.x);
    const marker = new window.kakao.maps.Marker({
      position: markerPosition,
      map: kakaoMap,
    });

    const infowindow = new window.kakao.maps.InfoWindow({
        content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
    });

    window.kakao.maps.event.addListener(marker, 'mouseover', () => {
        infowindow.open(kakaoMap, marker);
    });
    window.kakao.maps.event.addListener(marker, 'mouseout', () => {
        infowindow.close();
    });
     window.kakao.maps.event.addListener(marker, 'click', () => {
        panTo(place.y, place.x);
    });

    markers.push(marker);
  });
}

function removeMarkers() {
  markers.forEach(marker => marker.setMap(null));
  markers = [];
}

function panTo(lat, lng) {
  if (kakaoMap) {
    const moveLatLng = new window.kakao.maps.LatLng(lat, lng);
    kakaoMap.panTo(moveLatLng);
  }
}

onMounted(async () => {
  await loadSelectData();
  await initializeMap();
});

</script>

<style scoped>
.bank-finder-container {
  display: flex;
  height: calc(100vh - 80px); /* 헤더 높이 등을 고려하여 조정 */
  padding: 20px;
  gap: 20px;
  background-color: #f8f9fa;
}

.controls-panel {
  width: 350px;
  padding: 25px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
  margin-bottom: 8px;
}

.form-select {
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-select:disabled {
  background-color: #e9ecef;
  opacity: 0.7;
}

.search-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  transition: background-color 0.2s;
  margin-top: 10px; /* 버튼 위 간격 */
}

.search-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.search-button:disabled {
  background-color: #3c9cf0;
  cursor: not-allowed;
}

.map-results-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden; /* 내부 스크롤을 위해 */
}

.map-container {
  height: 60%; /* 오른쪽 패널의 높이 비율 */
  min-height: 400px; /* 최소 높이 보장 */
  border-radius: 12px 12px 0 0; /* 상단 모서리만 둥글게 */
  background-color: #e9ecef; /* 지도 로딩 전 배경 */
}
.map-loading, .map-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 1.2rem;
  color: #6c757d;
}

.results-list-container {
  height: 40%; /* 오른쪽 패널의 높이 비율 */
  padding: 20px;
  overflow-y: auto;
  border-top: 1px solid #dee2e6; /* 지도와 결과 리스트 구분선 */
}

.results-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 15px;
}

.results-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.result-item {
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.result-item:hover {
  background-color: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.result-item h4 {
  font-size: 1rem;
  font-weight: 500;
  color: #007bff;
  margin: 0 0 5px 0;
}

.result-item p {
  font-size: 0.85rem;
  color: #6c757d;
  margin: 3px 0;
}

.no-results, .loading-results {
  text-align: center;
  padding: 20px;
  color: #6c757d;
  font-size: 1rem;
}

</style>