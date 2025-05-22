<template>
  <div class="profile-view container mt-5" v-if="store.currentUser">
    <h2>{{ store.currentUser.username }}님의 프로필</h2>

    <div class="card mb-4">
      <div class="card-header">기본 정보</div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item"><strong>사용자 이름:</strong> {{ store.currentUser.username }}</li>
        <li class="list-group-item"><strong>이메일:</strong> {{ store.currentUser.email }}</li>
        <li class="list-group-item"><strong>나이:</strong> {{ store.currentUser.age }}</li>
        <li class="list-group-item"><strong>연봉:</strong> {{ store.currentUser.annual_salary ? store.currentUser.annual_salary.toLocaleString() + '원' : '정보 없음' }}</li>
        <li class="list-group-item"><strong>현재 가진 금액:</strong> {{ store.currentUser.current_assets ? store.currentUser.current_assets.toLocaleString() + '원' : '정보 없음' }}</li>
        <li class="list-group-item">
          <strong>가입 상품 ID:</strong>
          <span v-if="store.currentUser.subscribed_products_display && store.currentUser.subscribed_products_display.length > 0">
            {{ store.currentUser.subscribed_products_display.join(', ') }}
          </span>
          <span v-else>가입한 상품이 없습니다.</span>
        </li>
      </ul>
    </div>

    <div class="card mb-4">
      <div class="card-header">프로필 수정</div>
      <div class="card-body">
        <form @submit.prevent="handleUpdateProfile">
          <div class="mb-3">
            <label for="username_display" class="form-label">사용자 이름 (수정 불가)</label>
            <input type="text" class="form-control" id="username_display" :value="store.currentUser.username" disabled>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">이메일</label>
            <input type="email" class="form-control" id="email" v-model="editableProfile.email">
          </div>
          <div class="mb-3">
            <label for="age" class="form-label">나이</label>
            <input type="number" class="form-control" id="age" v-model.number="editableProfile.age">
          </div>
          <div class="mb-3">
            <label for="firstName" class="form-label">이름 (First Name)</label>
            <input type="text" class="form-control" id="firstName" v-model="editableProfile.first_name">
          </div>
          <div class="mb-3">
            <label for="lastName" class="form-label">성 (Last Name)</label>
            <input type="text" class="form-control" id="lastName" v-model="editableProfile.last_name">
          </div>
          <div class="mb-3">
            <label for="annual_salary" class="form-label">연봉 (원)</label>
            <input type="number" class="form-control" id="annual_salary" v-model.number="editableProfile.annual_salary">
          </div>
          <div class="mb-3">
            <label for="current_assets" class="form-label">현재 가진 금액 (원)</label>
            <input type="number" class="form-control" id="current_assets" v-model.number="editableProfile.current_assets">
          </div>
          <div class="mb-3">
            <label for="subscribed_products" class="form-label">가입 상품 ID (쉼표로 구분)</label>
            <input type="text" class="form-control" id="subscribed_products" v-model="editableProfile.subscribed_products">
            <small class="form-text text-muted">상품 ID를 쉼표(,)로 구분하여 입력하세요. (예: P001,P002)</small>
          </div>
          <button type="submit" class="btn btn-primary">프로필 업데이트</button>
        </form>
      </div>
    </div>
    
    <div class="card mb-4">
      <div class="card-header">맞춤 상품 추천</div>
      <div class="card-body">
        <button @click="fetchRecommendations" class="btn btn-success mb-3" :disabled="loadingRecommendations">
          {{ loadingRecommendations ? '추천받는 중...' : '나에게 맞는 상품 추천받기' }}
        </button>
        <div v-if="recommendations.length > 0">
          <h5>추천 상품 목록</h5>
          <ul class="list-group">
            <li v-for="product in recommendations" :key="product.fin_prdt_cd" class="list-group-item">
              <h6>{{ product.fin_prdt_nm }} ({{ product.kor_co_nm }})</h6>
              <p class="mb-1"><small>{{ product.product_type === 'deposit' ? '예금' : '적금' }}</small></p>
              <p class="mb-0"><small>특징: {{ product.etc_note }}</small></p>
              </li>
          </ul>
        </div>
        <p v-else-if="!loadingRecommendations && recommendationsRequested">
          추천 드릴 상품이 없거나, 프로필 정보(나이, 연봉, 자산)를 바탕으로 한 맞춤 추천을 찾지 못했습니다. 프로필 정보를 업데이트해보세요.
        </p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">가입한 금융 상품 목록 및 금리 차트</div>
      <div class="card-body">
        <p v-if="!store.currentUser.subscribed_products_details || store.currentUser.subscribed_products_details.length === 0">
          가입한 금융 상품이 없습니다.
        </p>
        <div v-else>
          <ul class="list-group mb-3">
            <li v-for="product in store.currentUser.subscribed_products_details" :key="product.fin_prdt_cd" class="list-group-item">
              <strong>{{ product.fin_prdt_nm }}</strong> ({{ product.kor_co_nm }})
              </li>
          </ul>
          <button @click="fetchChartDataAndDraw" class="btn btn-info">가입 상품 금리 차트 보기</button>
          <div class="mt-3 chart-container" style="position: relative; height:40vh; width:80vw; max-width: 600px;">
            <canvas id="subscribedProductsChart" ref="subscribedChartCanvas"></canvas>
          </div>
        </div>
      </div>
    </div>

  </div>
  <div v-else class="text-center mt-5">
    <p>사용자 정보를 불러오는 중...</p>
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAccountStore } from '@/stores/accounts';
import axios from 'axios'; // axios 직접 사용
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const store = useAccountStore();
const editableProfile = ref({
  email: '',
  age: null,
  first_name: '',
  last_name: '',
  annual_salary: null, // 추가
  current_assets: null,  // 추가
  subscribed_products: '',
});

const recommendations = ref([]);
const loadingRecommendations = ref(false);
const recommendationsRequested = ref(false); // 추천 요청 여부 상태

const subscribedChartCanvas = ref(null);
let subscribedChartInstance = null;

watch(() => store.currentUser, (newUser) => {
  if (newUser) {
    editableProfile.value.email = newUser.email || '';
    editableProfile.value.age = newUser.age || null;
    editableProfile.value.first_name = newUser.first_name || '';
    editableProfile.value.last_name = newUser.last_name || '';
    editableProfile.value.annual_salary = newUser.annual_salary || null; // 추가
    editableProfile.value.current_assets = newUser.current_assets || null; // 추가
    editableProfile.value.subscribed_products = newUser.subscribed_products || '';
  }
}, { immediate: true, deep: true });

const handleUpdateProfile = async () => {
  try {
    if (!store.currentUser || !store.currentUser.username) {
      alert('사용자 정보를 정확히 불러올 수 없습니다. 잠시 후 다시 시도하거나 재로그인 해주세요.');
      return;
    }

    // `subscribed_products`는 문자열로 유지
    const payload = {
      username: store.currentUser.username,
      email: editableProfile.value.email,
      age: editableProfile.value.age,
      first_name: editableProfile.value.first_name,
      last_name: editableProfile.value.last_name,
      annual_salary: editableProfile.value.annual_salary, // 추가
      current_assets: editableProfile.value.current_assets,   // 추가
      subscribed_products: editableProfile.value.subscribed_products,
    };
    await store.updateUserProfile(payload);
  } catch (error) {
    console.error("프로필 업데이트 중 컴포넌트 에러:", error);
  }
};

const fetchRecommendations = async () => {
  loadingRecommendations.value = true;
  recommendationsRequested.value = true; // 추천 요청 상태 true
  recommendations.value = [];
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/recommendations/', {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    recommendations.value = response.data;
  } catch (error) {
    console.error('추천 상품 로드 실패:', error);
    alert('추천 상품을 가져오는 데 실패했습니다.');
  } finally {
    loadingRecommendations.value = false;
  }
};

const fetchChartDataAndDraw = async () => {
  if (!store.currentUser || !store.currentUser.subscribed_products_details || store.currentUser.subscribed_products_details.length === 0) {
    alert("차트에 표시할 가입 상품 정보가 없습니다.");
    return;
  }
  
  const productsDetails = store.currentUser.subscribed_products_details;
  
  const chartLabels = [];
  const chartBaseRates = [];
  const chartMaxRates = [];

  productsDetails.forEach(product => {
    if (product.options && product.options.length > 0) {
      // 예시: 12개월 옵션 또는 첫 번째 옵션 사용
      const option = product.options.find(opt => opt.save_trm === '12') || product.options[0];
      if (option) {
        chartLabels.push(`${product.fin_prdt_nm.substring(0,15)}... (${option.save_trm}개월)`); // 상품명 길면 자르기
        chartBaseRates.push(parseFloat(option.intr_rate) || 0);
        chartMaxRates.push(parseFloat(option.intr_rate2) || 0);
      }
    }
  });
  
  if (chartLabels.length === 0) {
    alert("차트에 표시할 유효한 금리 정보를 찾지 못했습니다.");
    return;
  }

  drawChart(chartLabels, chartBaseRates, chartMaxRates);
};

const drawChart = (labels, baseRates, maxRates) => {
  const ctx = subscribedChartCanvas.value;
  if (!ctx) return;

  if (subscribedChartInstance) {
    subscribedChartInstance.destroy();
  }
  subscribedChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '기본 금리 (%)',
          data: baseRates,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: '최고 우대 금리 (%)',
          data: maxRates,
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: '금리 (%)' }
        },
        x: {
          ticks: {
            autoSkip: false, // 모든 라벨 표시 (필요시)
            maxRotation: 45, // 라벨 회전
            minRotation: 45
          }
        }
      },
      plugins: {
        title: { display: true, text: '가입 상품 금리 비교' },
        legend: { position: 'top' },
      }
    }
  });
};

onMounted(async () => {
  if (!store.currentUser && store.token) {
    await store.getUserProfile(); // 프로필 정보 가져오기 (subscribed_products_details 포함)
  } else if (store.currentUser) {
     // 이미 currentUser가 있다면 watch 콜백에서 editableProfile이 설정됨
     // 여기서 추가로 호출할 필요 없음
  }
});

</script>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: auto;
}
.chart-container {
  position: relative;
  height: 300px; /* 필요에 따라 높이 조정 */
  width: 100%;   /* 너비를 부모 요소에 맞춤 */
}

/* 모바일 화면 등 작은 화면에서 차트가 너무 작아지는 것을 방지하기 위해 최소 높이 설정 가능 */
@media (max-width: 600px) {
  .chart-container {
    min-height: 250px;
  }
}
</style>