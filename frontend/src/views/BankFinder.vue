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

const map = ref(null);
const clusterer = ref(null);
const infowindow = ref(null);
const markers = ref([]);
const mapContainer = ref(null); // Ref for the map div

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
      center: new window.kakao.maps.LatLng(37.49818, 127.027386),
      level: 5
    };
    try {
      map.value = new window.kakao.maps.Map(mapContainer.value, mapOption);

      clusterer.value = new window.kakao.maps.MarkerClusterer({
        map: map.value,
        averageCenter: true,
        minLevel: 7,
        disableClickZoom: true
      });

      infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1, removable: true });

      // 클러스터 클릭 이벤트
      if (clusterer.value) {
        window.kakao.maps.event.addListener(clusterer.value, 'clusterclick', function(cluster) {
          const center = cluster.getCenter();
          const currentLevel = map.value.getLevel();
          map.value.setLevel(currentLevel - 1, { anchor: center });
        });
      }

    } catch (error) {
      console.error("지도 로딩 또는 클러스터러/인포윈도우 생성 실패:", error);
      alert("지도 관련 기능 초기화에 실패했습니다. API 키 또는 네트워크 연결을 확인하세요.");
    }
  } else {
    console.error("Kakao Maps SDK가 로드되지 않았거나 mapContainer가 없습니다.");
    // SDK가 로드될 때까지 재시도하거나 사용자에게 알림
    setTimeout(initializeMap, 100); // 100ms 후 재시도
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
      mapData.value = null; // 유효하지 않은 데이터일 경우 null 처리
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
};

const onCityChange = () => {
  selectedBank.value = '';
};

const onBankChange = () => {
  // searchBtn 활성화는 computed property (isSearchButtonEnabled)가 처리
};

// Remove markers from map
const removeMarkersFromMap = () => {
  if (infowindow.value && infowindow.value.getMap()) {
    infowindow.value.close();
  }
  if (clusterer.value) {
    clusterer.value.clear();
  } else {
    markers.value.forEach(marker => marker.setMap(null));
  }
  markers.value = [];
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
          if (infowindow.value) {
            const content = `<div style="padding:5px;font-size:12px;white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${place.place_name}</div>`;
            infowindow.value.setContent(content);
            infowindow.value.open(map.value, marker);
          }
        });

        newMarkers.push(marker);
        bounds.extend(position);
      });

      if (clusterer.value) {
        clusterer.value.addMarkers(newMarkers);
      } else {
        newMarkers.forEach(marker => marker.setMap(map.value));
      }
      markers.value = newMarkers; // Update the reactive markers ref

      if (newMarkers.length > 0 && map.value) {
        map.value.setBounds(bounds);
        if (newMarkers.length === 1) {
           map.value.setLevel(map.value.getLevel() > 3 ? map.value.getLevel() - 2 : 3); // 단일 마커 시 적절히 확대
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
  if (window.kakao && window.kakao.maps) {
      window.kakao.maps.load(() => { // SDK의 모든 기능이 로드된 후 지도 초기화
        initializeMap();
      });
  } else {
    // 만약 index.html에서 스크립트 로딩이 실패했거나 아직 로드 중일 경우 처리
    // 이 경우, index.html의 스크립트 태그가 정상적으로 앱키와 함께 포함되어 있는지 확인 필요
    const script = document.createElement('script');
    script.onload = () => window.kakao.maps.load(() => initializeMap());
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_KAKAO_APP_KEY&libraries=services,clusterer&autoload=false`; // autoload=false 필수, 앱키 변경
    document.head.appendChild(script);
    alert("카카오맵 SDK를 동적으로 로드합니다. index.html 설정을 확인해주세요.");
  }
});

// Watchers to reset child selections when parent changes (alternative to direct event handling)
watch(selectedProvince, () => {
  selectedCity.value = '';
  selectedBank.value = '';
});

watch(selectedCity, () => {
  selectedBank.value = '';
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