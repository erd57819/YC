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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMapStore } from '@/stores/mapStore'

const mapStore = useMapStore()
const mapInstance = ref(null)
const searchKeyword = ref('')
const searchResults = ref([])
const markers = ref([])

onMounted(async () => {
  try {
    await mapStore.loadKakaoSdk() // SDK 로드 및 API 키 가져오기
    if (mapStore.isSdkLoaded && window.kakao && window.kakao.maps) {
      initMap()
    } else {
      console.error("Kakao Maps SDK could not be initialized.")
    }
  } catch (error) {
    console.error("Error during map initialization:", error)
  }
})

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new window.kakao.maps.LatLng(37.566826, 126.9786567), // 초기 중심 서울 시청
    level: 5
  }
  mapInstance.value = new window.kakao.maps.Map(container, options)
}

const searchPlaces = () => {
  if (!searchKeyword.value.trim()) {
    alert('검색어를 입력해주세요.')
    return
  }
  if (!mapInstance.value || !window.kakao.maps.services) {
    alert('지도가 초기화되지 않았거나 검색 서비스 사용이 불가능합니다.')
    return
  }

  // 기존 마커 및 검색 결과 초기화
  removeMarkers()
  searchResults.value = []

  const ps = new window.kakao.maps.services.Places()
  ps.keywordSearch(searchKeyword.value, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      searchResults.value = data
      displayPlaces(data)
      if (data.length > 0) {
        const bounds = new window.kakao.maps.LatLngBounds()
        data.forEach(place => bounds.extend(new window.kakao.maps.LatLng(place.y, place.x)))
        mapInstance.value.setBounds(bounds)
      }
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 존재하지 않습니다.')
    } else if (status === window.kakao.maps.services.Status.ERROR) {
      alert('검색 중 오류가 발생했습니다.')
    }
  })
}

const displayPlaces = (places) => {
  places.forEach(place => {
    const marker = new window.kakao.maps.Marker({
      map: mapInstance.value,
      position: new window.kakao.maps.LatLng(place.y, place.x)
    })
    markers.value.push(marker)

    // 마커에 클릭이벤트를 등록합니다
    window.kakao.maps.event.addListener(marker, 'click', function() {
        // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
        const infowindow = new window.kakao.maps.InfoWindow({
            content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
        });
        infowindow.open(mapInstance.value, marker);
    });
  })
}

const removeMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

</script>

<style scoped>
#map {
  border: 1px solid #ccc;
}
</style>