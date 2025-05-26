<template>
  <div style="max-width: 800px; margin: auto;">
    <Bar v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
    <p v-else>차트를 표시할 데이터가 없습니다.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  products: {
    type: Array,
    required: true,
  },
});

const chartData = computed(() => {
  const labels = [];
  const baseRates = []; 
  const primeRates = []; 

  props.products.forEach(sub => {
    const product = sub.product_info;
    labels.push(`[${product.kor_co_nm}] ${product.fin_prdt_nm.substring(0, 10)}..`);
    
    const options = product.options;
    let bestOption = null;
    if (options && options.length > 0) {
      bestOption = options.find(o => o.save_trm === '12') || 
                   options.reduce((max, o) => (parseFloat(o.intr_rate2) > parseFloat(max.intr_rate2) ? o : max), options[0]);
    }
    
    baseRates.push(bestOption && bestOption.intr_rate !== null ? parseFloat(bestOption.intr_rate) : 0);
    primeRates.push(bestOption && bestOption.intr_rate2 !== null ? parseFloat(bestOption.intr_rate2) : 0);
  });

  return {
    labels,
    datasets: [
      {
        label: '저축 금리 (%)',
        backgroundColor: '#0d6efd',
        data: baseRates,
        borderRadius: 4,
        barPercentage: 0.7,
        categoryPercentage: 0.7,
      },
      {
        label: '최고 우대금리 (%)',
        backgroundColor: '#6c757d',
        data: primeRates,
        borderRadius: 4,
        barPercentage: 0.7,
        categoryPercentage: 0.7,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, 
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      },
      ticks: {
        callback: function(value) {
          return value.toFixed(2) + '%';
        }
      }
    },
    x: {
      ticks: {
        font: {
          size: 10 
        }
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: false, 
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y.toFixed(2) + '%';
          }
          return label;
        }
      }
    }
  }
};
</script>

<style scoped>
/* 필요시 스타일 추가 */
</style>