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
import { useGoldStore } from '@/stores/golds';
import { storeToRefs } from 'pinia';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const store = useGoldStore();
const { goldData: fetchedGoldPriceData } = storeToRefs(store);

const startYear = ref(2024);
const startMonth = ref(1); // 시작 월을 1월로 변경하여 초기 데이터 범위를 넓힙니다.
const endYear = ref(2024);
const endMonth = ref(new Date().getMonth() + 1);

onMounted(() => {
  store.fetchGoldData();
});

const chartData = computed(() => {
  if (!fetchedGoldPriceData.value || fetchedGoldPriceData.value.length === 0) {
    return {
      labels: [],
      datasets: [{
        label: '금 가격',
        borderColor: '#E6B333',
        data: [],
        tension: 0.4,
        borderWidth: 2,
        pointBackgroundColor: 'white',
        pointBorderColor: '#E6B333',
        pointHoverRadius: 8,
        pointHoverBorderWidth: 3,
      }],
    };
  }

  // --- 날짜 필터링 기능 추가 ---
  // 시작일(1일)과 종료일(해당 월의 마지막 날)을 Date 객체로 생성
  const startDate = new Date(startYear.value, startMonth.value - 1, 1);
  const endDate = new Date(endYear.value, endMonth.value, 0, 23, 59, 59);

  // 선택된 날짜 범위에 맞는 데이터만 필터링
  const filteredData = fetchedGoldPriceData.value.filter(item => {
    const itemDate = new Date(item.price_date);
    return itemDate >= startDate && itemDate <= endDate;
  });
  // --- 필터링 로직 끝 ---

  // 필터링된 데이터를 날짜순으로 정렬
  const sortedData = [...filteredData].sort((a, b) => new Date(a.price_date) - new Date(b.price_date));

  return {
    labels: sortedData.map(item => new Date(item.price_date).toLocaleDateString()),
    datasets: [{
      label: '금 가격',
      borderColor: '#E6B333',
      data: sortedData.map(item => parseFloat(item.high_price)),
      tension: 0.4,
      borderWidth: 2,
      pointBackgroundColor: 'white',
      pointBorderColor: '#E6B333',
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
  position: relative;
}
.no-data-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #6c757d;
}
</style>