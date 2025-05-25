<template>
  <div>
    <div class="header">
      <h1>금/은 가격 변동</h1>
      <div class="toggle-buttons">
        <router-link to="/gold" class="toggle-button">금</router-link>
        <router-link to="/silver" class="toggle-button">은</router-link>
      </div>
    </div>
    <div class="controls">
      <div class="date-picker">
        <label for="start-year">시작일:</label>
        <select
          id="start-year"
          :value="startYear"
          @change="emit('update:startYear', parseInt($event.target.value))"
        >
          <option v-for="year in years" :key="'start-' + year" :value="year">{{ year }}년</option>
        </select>
        <select
          id="start-month"
          :value="startMonth"
          @change="emit('update:startMonth', parseInt($event.target.value))"
        >
          <option v-for="month in 12" :key="'start-' + month" :value="month">{{ month }}월</option>
        </select>
      </div>
      <div class="date-picker">
        <label for="end-year">종료일:</label>
        <select
          id="end-year"
          :value="endYear"
          @change="emit('update:endYear', parseInt($event.target.value))"
        >
          <option v-for="year in years" :key="'end-' + year" :value="year">{{ year }}년</option>
        </select>
        <select
          id="end-month"
          :value="endMonth"
          @change="emit('update:endMonth', parseInt($event.target.value))"
        >
          <option v-for="month in 12" :key="'end-' + month" :value="month">{{ month }}월</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 부모로부터 v-model로 넘겨받을 props 정의
defineProps({
  startYear: { type: Number, required: true },
  startMonth: { type: Number, required: true },
  endYear: { type: Number, required: true },
  endMonth: { type: Number, required: true },
});

// 부모의 v-model을 업데이트하기 위한 emits 정의
const emit = defineEmits([
  'update:startYear',
  'update:startMonth',
  'update:endYear',
  'update:endMonth',
]);

// 연도 목록은 이 컨트롤 컴포넌트가 자체적으로 가질 수 있음
const currentYear = new Date().getFullYear();
const years = ref(Array.from({ length: 10 }, (_, i) => currentYear - i));
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}
h1 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}
.toggle-buttons {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  display: flex;
}
.toggle-button {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  background-color: #fff;
  color: #495057;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.toggle-button:first-of-type {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.toggle-button:last-of-type {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-left: none;
}
.router-link-exact-active {
  background-color: #4A90E2;
  color: white;
  border-color: #4A90E2;
}
.controls {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.date-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
label {
  font-size: 0.9rem;
  color: #555;
}
select {
  padding: 0.4rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
}
</style>