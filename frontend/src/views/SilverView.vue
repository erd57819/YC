<template>
  <div class="chart-container">
    <goods-vue
      v-model:startYear="startYear"
      v-model:startMonth="startMonth"
      v-model:endYear="endYear"
      v-model:endMonth="endMonth"
    />
    <div class="chart-wrapper">
      <Line v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
      <div v-else class="no-data-message">
        <p>선택된 기간에 해당하는 데이터가 없습니다. 다른 날짜를 선택해주세요.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import GoodsVue from '@/components/goods.vue';
import { useGoldStore } from '@/stores/golds'; // Pinia 스토어 임포트
import { storeToRefs } from 'pinia';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const store = useGoldStore();
// 스토어에서 silverData를 반응형 참조로 가져옵니다.
const { silverData: fetchedSilverPriceData } = storeToRefs(store);

const startYear = ref(2024);
const startMonth = ref(1); // 시작 월을 1월로 변경하여 초기 데이터 범위를 넓힙니다.
const endYear = ref(2024);
const endMonth = ref(new Date().getMonth() + 1); // 현재 월로 설정

onMounted(() => {
  store.fetchSilverData(); // 스토어 액션을 호출하여 은 시세 데이터를 가져옵니다.
});

const chartData = computed(() => {
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

  // --- 날짜 필터링 기능 추가 ---
  // 시작일(1일)과 종료일(해당 월의 마지막 날)을 Date 객체로 생성
  const startDate = new Date(startYear.value, startMonth.value - 1, 1);
  // endMonth.value는 1부터 시작하므로, Date 객체에서 월은 0부터 시작하기에 그대로 사용합니다.
  // new Date(year, month, 0)은 해당 month의 마지막 날을 의미합니다.
  const endDate = new Date(endYear.value, endMonth.value, 0, 23, 59, 59);

  // 선택된 날짜 범위에 맞는 데이터만 필터링
  const filteredData = fetchedSilverPriceData.value.filter(item => {
    const itemDate = new Date(item.price_date);
    return itemDate >= startDate && itemDate <= endDate;
  });
  // --- 필터링 로직 끝 ---

  // 필터링된 데이터를 날짜순으로 정렬
  const sortedData = [...filteredData].sort((a, b) => new Date(a.price_date) - new Date(b.price_date));

  return {
    labels: sortedData.map(item => new Date(item.price_date).toLocaleDateString()),
    datasets: [{
      label: '은 가격 ',
      borderColor: '#4A90E2',
      data: sortedData.map(item => parseFloat(item.high_price)), // 예시로 'high_price' 사용, 필요시 'low_price' 등으로 변경
      tension: 0.4,
      borderWidth: 2,
      pointBackgroundColor: 'white',
      pointBorderColor: '#4A90E2',
      pointHoverRadius: 8,
      pointHoverBorderWidth: 3,
    }],
  };
});

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
  position: relative; /* 데이터 없음 메시지 중앙 정렬을 위해 추가 */
}
.no-data-message { /* 데이터가 없을 때 사용자에게 안내 메시지를 표시하기 위한 스타일 */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
}
</style>