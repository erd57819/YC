<template>
  <div class="container mt-5">
    <h1 class="mb-4">은행 찾기</h1>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="row mb-3">
      <div class="col-md-4">
        <label for="citySelect" class="form-label">시/도 선택:</label>
        <select id="citySelect" class="form-select" v-model="selectedCity">
          <option value="">시/도를 선택하세요</option>
          <option v-for="city in cities" :key="city.name" :value="city.name">
            {{ city.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="districtSelect" class="form-label">구/군 선택:</label>
        <select id="districtSelect" class="form-select" v-model="selectedDistrict" :disabled="!selectedCity">
          <option value="">구/군을 선택하세요</option>
          <option v-for="district in districts" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="bankSelect" class="form-label">은행 선택:</label>
        <select id="bankSelect" class="form-select" v-model="selectedBank">
          <option value="">은행을 선택하세요</option>
          <option v-for="bank in bankList" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
    </div>

    <button class="btn btn-primary mb-4" @click="searchBankBranches" :disabled="!selectedDistrict || !selectedBank || isLoading">
      <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      {{ isLoading ? '검색 중...' : '선택한 은행 지점 검색' }}
    </button>

    <div id="map" style="width:100%;height:500px;"></div>

    <div v-if="searchResults.length > 0" class="mt-4">
      <h2>검색 결과:</h2>
      <ul class="list-group">
        <li v-for="place in searchResults" :key="place.id" class="list-group-item">
          <h5>{{ place.place_name }}</h5>
          <p>주소: {{ place.road_address_name || place.address_name }}</p>
          <p v-if="place.phone">전화번호: {{ place.phone }}</p>
        </li>
      </ul>
    </div>
    <div v-else-if="searched && !isLoading" class="mt-4 alert alert-warning">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useMapStore } from '@/stores/map';

// Pinia 스토어 사용
const mapStore = useMapStore();

// 드롭다운 선택 및 데이터 상태
const cities = ref([]);
const bankList = ref([]);
const selectedCity = ref('');
const selectedDistrict = ref('');
const selectedBank = ref('');

// UI 제어 상태
const isLoading = ref(false);
const errorMessage = ref('');
const searched = ref(false);

// 지도 및 검색 관련 상태
const mapInstance = ref(null);
const markers = ref([]);
let kakaoServices = null; // Places, InfoWindow 등 카카오 서비스를 담을 객체
const searchResults = ref([]);

// 선택된 시/도에 따라 구/군 목록을 동적으로 계산
const districts = computed(() => {
  const cityData = cities.value.find(c => c.name === selectedCity.value);
  return cityData ? cityData.countries : [];
});

// 시/도 선택이 바뀌면, 선택했던 구/군 초기화
watch(selectedCity, () => {
  selectedDistrict.value = '';
});

// 검색 조건이 바뀌면, 이전 검색 결과 초기화
watch([selectedDistrict, selectedBank], () => {
  searchResults.value = [];
  searched.value = false;
  removeMarkers();
});

// 지도 및 마커 관련 함수들
const initMap = (kakao) => {
  const container = document.getElementById('map');
  const options = {
    center: new kakao.maps.LatLng(37.566826, 126.9786567), // 서울 시청
    level: 5,
  };
  mapInstance.value = new kakao.maps.Map(container, options);
  kakaoServices = {
    places: new kakao.maps.services.Places(),
    infowindow: new kakao.maps.InfoWindow({ zIndex: 1 }),
  };
};

const displayMarker = (place) => {
  if (!mapInstance.value || !kakaoServices) return;
  const marker = new window.kakao.maps.Marker({
    map: mapInstance.value,
    position: new window.kakao.maps.LatLng(place.y, place.x),
  });
  markers.value.push(marker);

  window.kakao.maps.event.addListener(marker, 'click', () => {
    kakaoServices.infowindow.setContent(`<div style="padding:5px;font-size:12px;">${place.place_name}</div>`);
    kakaoServices.infowindow.open(mapInstance.value, marker);
  });
};

const removeMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];
};

// 핵심 로직 함수
const loadSelectionData = async () => {
  try {
    const response = await fetch('/data.json');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    cities.value = data.mapInfo;
    bankList.value = data.bankInfo;
  } catch (error) {
    console.error("Failed to load map data:", error);
    throw new Error('지역/은행 정보를 불러오는 데 실패했습니다.');
  }
};

const searchBankBranches = () => {
  if (!kakaoServices) {
    errorMessage.value = '지도 서비스가 준비되지 않았습니다.';
    return;
  }
  isLoading.value = true;
  searched.value = false;
  
  const keyword = `${selectedDistrict.value} ${selectedBank.value}`;
  
  kakaoServices.places.keywordSearch(keyword, (data, status) => {
    removeMarkers();
    searchResults.value = [];
    
    if (status === window.kakao.maps.services.Status.OK) {
      searchResults.value = data;
      const bounds = new window.kakao.maps.LatLngBounds();
      data.forEach(place => {
        displayMarker(place);
        bounds.extend(new window.kakao.maps.LatLng(place.y, place.x));
      });
      mapInstance.value.setBounds(bounds);
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      // 결과 없음 메시지는 템플릿의 v-else-if가 처리
    } else {
      errorMessage.value = '검색 중 오류가 발생했습니다.';
    }
    
    isLoading.value = false;
    searched.value = true;
  });
};

// 컴포넌트 마운트 시 실행될 초기화 로직
onMounted(async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await loadSelectionData();
    const kakao = await mapStore.getSdkLoadPromise();
    initMap(kakao);
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
});

</script>

<style scoped>
.container {
  max-width: 900px;
}
#map {
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>