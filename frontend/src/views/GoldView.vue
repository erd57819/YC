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
import { ref, computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import GoodsVue from '@/components/goods.vue';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// --- 상태 관리 (날짜) ---
const startYear = ref(2024);
const startMonth = ref(8);
const endYear = ref(2024);
const endMonth = ref(8);

// --- 차트 데이터 (은 전용) ---
const priceData = {
  silver: [22, 24, 23, 26, 25, 28, 26, 30, 29, 32, 30, 35, 31, 33, 30, 34, 32, 36],
};
const labels = ref(Array.from({ length: 18 }, (_, i) => (i % 2 === 0 ? i + 2 : '')));

const chartData = computed(() => ({
  labels: labels.value,
  datasets: [{
    label: '은 가격',
    borderColor: '#4A90E2',
    data: priceData.silver,
    tension: 0.4,
    borderWidth: 2,
    pointBackgroundColor: 'white',
    pointBorderColor: '#4A90E2',
    pointHoverRadius: 8,
    pointHoverBorderWidth: 3,
  }],
}));

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