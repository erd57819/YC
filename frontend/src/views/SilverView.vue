<template>
  <div class="chart-container">
    <goods-vue
      v-model:startYear="startYear"
      v-model:startMonth="startMonth"
      v-model:endYear="endYear"
      v-model:endMonth="endMonth"
    />
    <div class="chart-wrapper">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'; // onMounted 추가
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import GoodsVue from '@/components/goods.vue';
import { useGoldStore } from '@/stores/golds'; // Pinia 스토어 임포트
import { storeToRefs } from 'pinia'; // storeToRefs 임포트

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// --- Pinia 스토어 사용 설정 ---
const store = useGoldStore();
// 스토어에서 silverData를 반응형 참조로 가져옵니다.
const { silverData: fetchedSilverPriceData } = storeToRefs(store);

// --- 상태 관리 (날짜) - 기존 코드 유지 ---
const startYear = ref(2024);
const startMonth = ref(8);
const endYear = ref(2024);
const endMonth = ref(8);

// --- 컴포넌트가 마운트될 때 데이터 가져오기 ---
onMounted(() => {
  store.fetchSilverData(); // 스토어 액션을 호출하여 은 시세 데이터를 가져옵니다.
});

// --- 차트 데이터 (스토어에서 가져온 동적 데이터 사용) ---
const chartData = computed(() => {
  // fetchedSilverPriceData.value가 없거나 비어있으면 기본 차트 구조 반환
  if (!fetchedSilverPriceData.value || fetchedSilverPriceData.value.length === 0) {
    return {
      labels: [],
      datasets: [{
        label: '은 가격',
        borderColor: '#4A90E2',
        data: [],
        tension: 0.4,
        borderWidth: 2,
        pointBackgroundColor: 'white',
        pointBorderColor: '#4A90E2',
        pointHoverRadius: 8,
        pointHoverBorderWidth: 3,
      }],
    };
  }

  // 날짜순으로 정렬 (API 응답이 이미 정렬되어 있다면 생략 가능)
  const sortedData = [...fetchedSilverPriceData.value].sort((a, b) => new Date(a.price_date) - new Date(b.price_date));

  return {
    labels: sortedData.map(item => new Date(item.price_date).toLocaleDateString()), // 날짜 데이터로 라벨 설정
    datasets: [{
      label: '은 가격 ', // 또는 '고가', '평균가' 등 필요에 따라 수정
      borderColor: '#4A90E2',
      // API에서 받은 데이터 중 'low_price' 또는 'high_price'를 사용합니다.
      // 여기서는 예시로 'low_price'를 사용합니다. 필요에 따라 'high_price' 등으로 변경하세요.
      data: sortedData.map(item => parseFloat(item.high_price)),
      tension: 0.4,
      borderWidth: 2,
      pointBackgroundColor: 'white',
      pointBorderColor: '#4A90E2',
      pointHoverRadius: 8,
      pointHoverBorderWidth: 3,
    }],
  };
});

// --- 차트 옵션 - 기존 코드 유지 ---
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: false },
    x: { grid: { display: false }, ticks: { align: 'start' } },
  },
  interaction: { mode: 'index', intersect: false },
  elements: { point: { radius: 0 } },
});
</script>

<style scoped>
.chart-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.chart-wrapper {
  height: 350px;
}
</style>