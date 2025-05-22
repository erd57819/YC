<template>
  <div>
    <div class="container">
      <div class="search-panel">
        <h2>은행 찾기</h2>
        <div class="form-group">
          <label for="province">광역시/도:</label>
          <select id="province" v-model="selectedProvince" @change="onProvinceChange">
            <option value="">광역시/도를 선택하세요</option>
            <option v-for="province in provinces" :key="province.name" :value="province.name">
              {{ province.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="city">시/군/구:</label>
          <select id="city" v-model="selectedCity" :disabled="!selectedProvince" @change="onCityChange">
            <option value="">시/군/구를 선택하세요</option>
            <option v-for="city in cities" :key="city" :value="city">
              {{ city }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="bank">은행:</label>
          <select id="bank" v-model="selectedBank" :disabled="!selectedCity" @change="onBankChange">
            <option value="">은행을 선택하세요</option>
            <option v-for="bankName in bankList" :key="bankName" :value="bankName">
              {{ bankName }}
            </option>
          </select>
        </div>
        <button id="search-btn" :disabled="!isSearchButtonEnabled" @click="searchBank">찾기</button>
      </div>
      <div id="map" ref="mapContainer"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';

// Reactive state
const mapData = ref(null);
const selectedProvince = ref('');
const selectedCity = ref('');
const selectedBank = ref('');

const mapInstance = ref(null); // map -> mapInstance로 변경 (중복 방지)
const clustererInstance = ref(null); // clusterer -> clustererInstance로 변경
const infowindowInstance = ref(null); // infowindow -> infowindowInstance로 변경
const markers = ref([]);
const mapContainer = ref(null);

// Computed properties for dynamic select options
const provinces = computed(() => mapData.value?.mapInfo || []);
const cities = computed(() => {
  if (!selectedProvince.value || !mapData.value) return [];
  const province = mapData.value.mapInfo.find(p => p.name === selectedProvince.value);
  return province ? province.countries : [];
});
const bankList = computed(() => mapData.value?.bankInfo || []);

const isSearchButtonEnabled = computed(() => {
  return !!(selectedProvince.value && selectedCity.value && selectedBank.value);
});

// Kakao Maps SDK 로드 확인 및 초기화 함수
const initializeMap = () => {
  if (window.kakao && window.kakao.maps && mapContainer.value) {
    const mapOption = {
      center: new window.kakao.maps.LatLng(37.49818, 127.027386), // 기본 중심 좌표 (강남역 부근)
      level: 5
    };
    try {
      mapInstance.value = new window.kakao.maps.Map(mapContainer.value, mapOption);

      clustererInstance.value = new window.kakao.maps.MarkerClusterer({
        map: mapInstance.value,
        averageCenter: true,
        minLevel: 7, // 클러스터 할 최소 지도 레벨
        disableClickZoom: true // 클러스터 마커를 클릭했을 때 지도가 확대되지 않도록 설정
      });

      infowindowInstance.value = new window.kakao.maps.InfoWindow({ zIndex: 1, removable: true });

      // 클러스터 클릭 이벤트
      if (clustererInstance.value) {
        window.kakao.maps.event.addListener(clustererInstance.value, 'clusterclick', function(cluster) {
          const center = cluster.getCenter();
          const currentLevel = mapInstance.value.getLevel();
          // 현재 레벨에서 1레벨 확대하고, 클릭한 클러스터의 중심으로 이동
          mapInstance.value.setLevel(currentLevel - 1, { anchor: center });
        });
      }
      console.log("카카오맵 초기화 완료.");
    } catch (error) {
      console.error("지도 로딩 또는 클러스터러/인포윈도우 생성 실패:", error);
      alert("지도 관련 기능 초기화에 실패했습니다. API 키 또는 네트워크 연결을 확인하세요.");
    }
  } else {
    console.error("Kakao Maps SDK가 로드되지 않았거나 mapContainer가 없습니다.");
    // SDK가 로드될 때까지 재시도하거나 사용자에게 알림 (단, 무한 루프 주의)
    // 이 부분은 onMounted에서 처리하는 것이 더 적절할 수 있습니다.
  }
};

// Fetch data and setup UI elements
const loadDataAndSetup = async () => {
  try {
    const response = await fetch('/data.json'); // public 폴더의 data.json
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    mapData.value = await response.json();
    if (!mapData.value || !Array.isArray(mapData.value.mapInfo) || !Array.isArray(mapData.value.bankInfo)) {
      alert("지도 데이터 형식이 올바르지 않습니다.");
      mapData.value = null;
    }
  } catch (error) {
    console.error("지도 데이터 로딩 실패:", error);
    alert(`지도 데이터를 불러오는 데 실패했습니다: ${error.message}.`);
  }
};

// Event handlers for select changes
const onProvinceChange = () => {
  selectedCity.value = '';
  selectedBank.value = '';
  removeMarkersFromMap(); // 지역 변경 시 마커 초기화
};

const onCityChange = () => {
  selectedBank.value = '';
  removeMarkersFromMap(); // 지역 변경 시 마커 초기화
};

const onBankChange = () => {
  // 은행 변경 시 특별한 동작이 필요하면 여기에 추가
};

// Remove markers from map
const removeMarkersFromMap = () => {
  if (infowindowInstance.value && infowindowInstance.value.getMap()) {
    infowindowInstance.value.close();
  }
  if (clustererInstance.value) {
    clustererInstance.value.clear(); // 클러스터러의 마커들을 초기화합니다.
  }
  markers.value = []; // 내부 마커 배열도 비웁니다.
};

// Search for banks
const searchBank = () => {
  removeMarkersFromMap();

  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services || !window.kakao.maps.services.Places) {
    alert("장소 검색 서비스를 사용할 수 없습니다. Kakao Maps SDK를 확인해주세요.");
    return;
  }

  const ps = new window.kakao.maps.services.Places();
  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`;

  ps.keywordSearch(keyword, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      if (data.length === 0) {
        alert('검색 결과가 없습니다.');
        return;
      }

      const newMarkers = [];
      const bounds = new window.kakao.maps.LatLngBounds();

      data.forEach(place => {
        const position = new window.kakao.maps.LatLng(place.y, place.x);
        const marker = new window.kakao.maps.Marker({
          position: position,
          title: place.place_name
        });

        window.kakao.maps.event.addListener(marker, 'click', () => {
          if (infowindowInstance.value) {
            const content = `<div style="padding:5px;font-size:12px;white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${place.place_name}</div>`;
            infowindowInstance.value.setContent(content);
            infowindowInstance.value.open(mapInstance.value, marker);
          }
        });

        newMarkers.push(marker);
        bounds.extend(position);
      });

      if (clustererInstance.value) {
        clustererInstance.value.addMarkers(newMarkers);
      }
      markers.value = newMarkers;

      if (newMarkers.length > 0 && mapInstance.value) {
        mapInstance.value.setBounds(bounds);
        // 검색 결과가 하나일 경우 너무 확대되는 것을 방지하고 적절한 레벨로 조정
        if (newMarkers.length === 1) {
           mapInstance.value.setLevel(Math.min(mapInstance.value.getLevel(), 5)); // 예시: 최대 5레벨까지만 확대
        }
      }

    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 없습니다.');
    } else if (status === window.kakao.maps.services.Status.ERROR) {
      alert('검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    } else {
      alert(`알 수 없는 오류 발생 (상태 코드: ${status})`);
    }
  });
};

// Lifecycle hook
onMounted(async () => {
  await loadDataAndSetup(); // 데이터 먼저 로드

  // Kakao Maps SDK 스크립트가 이미 로드되었는지 확인
  // index.html에서 autoload=false로 설정했으므로, kakao.maps.load를 사용해야 합니다.
  if (window.kakao && window.kakao.maps) {
    window.kakao.maps.load(() => { // SDK의 모든 기능이 로드된 후 지도 초기화
      initializeMap();
    });
  } else {
    console.error("카카오맵 SDK를 찾을 수 없습니다. index.html의 스크립트 로드 및 API 키 설정을 확인하세요.");
    alert("카카오맵 SDK 로드에 실패했습니다. 페이지를 새로고침하거나 API 키 설정을 확인해주세요.");
  }
});

// Watchers (선택사항, @change 핸들러로 이미 처리 중이라면 중복될 수 있음)
watch(selectedProvince, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedCity.value = '';
    selectedBank.value = '';
    // removeMarkersFromMap(); // 이 부분은 onProvinceChange에서 이미 처리
  }
});

watch(selectedCity, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedBank.value = '';
    // removeMarkersFromMap(); // 이 부분은 onCityChange에서 이미 처리
  }
});

</script>

<style scoped>
body { /* body 스타일은 전역으로 App.vue나 index.css에서 관리하는 것이 좋습니다. */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  background-color: #ffffff;
  color: #333;
  line-height: 1.6;
}

h1 {
  text-align: center;
  color: #ffffff;
  background-color: #ffaa55;
  padding: 15px 15px;
  margin: 0 0 30px 0;
  font-size: 1.6em;
  font-weight: 600;
  border-radius: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

h2 {
  text-align: left;
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
  border-bottom: none;
  padding-bottom: 0;
}

.container {
  display: flex;
  gap: 20px;
  padding: 0 30px;
  flex-wrap: wrap;
}

.search-panel {
  width: 300px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  background-color: #ffffff;
  box-shadow: none;
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex-shrink: 0;
  height: fit-content; /* 컨텐츠 높이에 맞춤 */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
    font-weight: normal;
    font-size: 0.9em;
    color: #555;
    margin-bottom: 2px;
}

select {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  font-size: 0.95em;
  -webkit-appearance: menulist; /* 표준 브라우저 모양을 위해 menulist 사용 */
  -moz-appearance: menulist;
  appearance: menulist;
  background-image: none; /* 기본 화살표 제거 (선택적) */
}

select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: none;
}

select:disabled {
    background-color: #e9ecef;
    cursor: not-allowed;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #ffaa55;
  color: white;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 10px;
  transform: none; /* 기본값 */
}

button:hover:not(:disabled) {
    background-color: #f8993a;
    transform: none; /* 호버 시 변형 없음 */
}

button:active:not(:disabled) {
    transform: none; /* 클릭 시 변형 없음 */
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

#map {
  flex-grow: 1;
  min-width: 400px;
  height: 600px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: none;
}

@media (max-width: 768px) {
    .container {
        flex-direction: column;
        padding: 0 15px;
    }
    .search-panel {
        width: 100%;
        max-width: none;
        margin-bottom: 20px;
        order: 1; /* 모바일에서 검색 패널이 먼저 오도록 */
    }
    #map {
        width: 100%;
        min-width: unset; /* 모바일에서 min-width 해제 */
        height: 450px; /* 모바일에서 지도 높이 조정 */
        order: 2; /* 모바일에서 지도가 검색 패널 다음에 오도록 */
    }
    h1 {
        margin-bottom: 20px;
        font-size: 1.4em;
    }
}
</style>