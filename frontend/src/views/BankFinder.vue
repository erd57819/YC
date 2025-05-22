<template>
  <div class="container mt-5">
    <h1 class="mb-4">은행 찾기</h1>

    <div class="row mb-3">
      <div class="col-md-4">
        <label for="citySelect" class="form-label">시/도 선택:</label>
        <select id="citySelect" class="form-select" v-model="selectedCity" @change="onCityChange">
          <option value="">시/도를 선택하세요</option>
          <option v-for="city in cities" :key="city.name" :value="city.name">
            {{ city.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="districtSelect" class="form-label">구/군 선택:</label>
        <select id="districtSelect" class="form-select" v-model="selectedDistrict">
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

    <button class="btn btn-primary mb-4" @click="searchBankBranches" :disabled="!selectedDistrict || !selectedBank || loadingData">
      <span v-if="loadingData" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      {{ loadingData ? '데이터 로딩 중...' : '선택한 은행 지점 검색' }}
    </button>

    <div id="map" style="width:100%;height:500px;"></div>

    <div v-if="searchResults.length > 0" class="mt-4">
      <h2>검색 결과:</h2>
      <ul class="list-group">
        <li v-for="(place, index) in searchResults" :key="index" class="list-group-item">
          <h5>{{ place.place_name }}</h5>
          <p>주소: {{ place.road_address_name || place.address_name }}</p>
          <p v-if="place.phone">전화번호: {{ place.phone }}</p>
        </li>
      </ul>
    </div>
    <div v-else-if="searched && searchResults.length === 0 && !loadingData" class="mt-4 alert alert-warning">
      검색 결과가 없습니다.
    </div>
    <div v-if="loadError" class="mt-4 alert alert-danger">
      지역 및 은행 데이터를 불러오는 데 실패했습니다: {{ loadError }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
// import mapData from '/data.json' // 이 줄을 삭제합니다.

const cities = ref([])
const bankList = ref([])

const selectedCity = ref('')
const selectedDistrict = ref('')
const selectedBank = ref('')
const districts = ref([])

const map = ref(null)
const markers = ref([])
const ps = ref(null) // 장소 검색 객체
const infowindow = ref(null) // 인포윈도우 객체
const searchResults = ref([])
const searched = ref(false) // 검색 실행 여부
const loadingData = ref(true) // 데이터 로딩 상태
const loadError = ref(null) // 데이터 로드 에러 상태

// data.json 파일 로드 함수
const loadMapData = async () => {
  loadingData.value = true
  loadError.value = null
  try {
    const response = await fetch('/data.json') // public 디렉토리의 파일은 루트 경로로 접근
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    cities.value = data.mapInfo
    bankList.value = data.bankInfo
  } catch (error) {
    console.error("Failed to load map data:", error)
    loadError.value = error.message
    // 사용자에게 데이터 로드 실패를 알릴 수 있습니다.
    alert('지역 및 은행 정보를 불러오는 데 실패했습니다. 페이지를 새로고침하거나 나중에 다시 시도해주세요.')
  } finally {
    loadingData.value = false
  }
}

// 시/도 선택 변경 시 해당 구/군 목록 업데이트
const onCityChange = () => {
  selectedDistrict.value = '' // 구/군 선택 초기화
  const cityData = cities.value.find(city => city.name === selectedCity.value)
  districts.value = cityData ? cityData.countries : []
}

// 카카오맵 초기화 함수
const initMap = () => {
  if (window.kakao && window.kakao.maps) {
    const container = document.getElementById('map')
    const options = {
      center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 서울 시청 기본 위치
      level: 5,
    }
    map.value = new window.kakao.maps.Map(container, options)
    ps.value = new window.kakao.maps.services.Places(map.value)
    infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 })
  } else {
    console.error('카카오맵 API 로드 실패')
    alert('지도 서비스를 불러오는 데 실패했습니다. 잠시 후 다시 시도해주세요.')
  }
}

// 장소 검색 콜백 함수
const placesSearchCB = (data, status, pagination) => {
  searchResults.value = []
  removeMarkers()

  if (status === window.kakao.maps.services.Status.OK) {
    searchResults.value = data
    const bounds = new window.kakao.maps.LatLngBounds()
    for (let i = 0; i < data.length; i++) {
      displayMarker(data[i])
      bounds.extend(new window.kakao.maps.LatLng(data[i].y, data[i].x))
    }
    if (map.value) {
        map.value.setBounds(bounds)
    }
  } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.')
  } else if (status === window.kakao.maps.services.Status.ERROR) {
    alert('검색 중 오류가 발생했습니다.')
  }
  searched.value = true
}

// 마커 표시 함수
const displayMarker = (place) => {
  if (!map.value) return;
  const marker = new window.kakao.maps.Marker({
    map: map.value,
    position: new window.kakao.maps.LatLng(place.y, place.x),
  })
  markers.value.push(marker)

  window.kakao.maps.event.addListener(marker, 'click', () => {
    if (infowindow.value && map.value) {
        infowindow.value.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>')
        infowindow.value.open(map.value, marker)
    }
  })
}

// 모든 마커 제거 함수
const removeMarkers = () => {
  for (let i = 0; i < markers.value.length; i++) {
    markers.value[i].setMap(null)
  }
  markers.value = []
}

// 은행 지점 검색 함수
const searchBankBranches = () => {
  if (loadingData.value) {
    alert('데이터를 로딩 중입니다. 잠시 후 시도해주세요.')
    return
  }
  if (!selectedDistrict.value || !selectedBank.value) {
    alert('검색할 지역(구/군)과 은행을 모두 선택해주세요.')
    return
  }
  if (!ps.value) {
    alert('지도 서비스가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.')
    return;
  }

  const keyword = `${selectedDistrict.value} ${selectedBank.value}`
  console.log(`검색 키워드: ${keyword}`)
  
  const placesInstance = new window.kakao.maps.services.Places();
  placesInstance.keywordSearch(keyword, placesSearchCB)

  const geocoder = new window.kakao.maps.services.Geocoder();
  geocoder.addressSearch(selectedDistrict.value, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK && map.value) {
      // const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);
      // map.value.setCenter(coords); // 검색 결과에 따라 setBounds로 자동 이동될 수 있음
    }
  });
}

onMounted(async () => {
  await loadMapData() // data.json 로드
  if (loadError.value) { // 데이터 로드 실패 시 지도 초기화 시도 안함
    return;
  }

  if (window.kakao && window.kakao.maps) {
    window.kakao.maps.load(initMap); // 카카오맵 API가 로드된 후 initMap 실행
  } else {
    const script = document.querySelector('script[src*="dapi.kakao.com/v2/maps/sdk.js"]');
    if (script) {
      script.onload = () => {
        window.kakao.maps.load(initMap);
      };
    } else {
       console.error('카카오맵 API 스크립트를 찾을 수 없습니다.');
       alert('지도 서비스를 위한 스크립트를 찾을 수 없습니다.');
    }
  }
})

watch([selectedDistrict, selectedBank], () => {
  searchResults.value = []
  searched.value = false
  removeMarkers()
})

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