<template>
  <div>
    <h5 class="mt-4 mb-3">기본 정보 수정</h5>
    
    <form @submit.prevent="updateProfile">
      <div class="info-item">
        <label for="nickname">닉네임</label>
        <div class="input-group">
          <input type="text" class="form-control" id="nickname" v-model="editableUser.nickname">
        </div>
      </div>

      <div class="info-item">
        <label for="age">나이</label>
        <div class="input-group">
          <input type="number" class="form-control" id="age" v-model.number="editableUser.age">
        </div>
      </div>

      <div class="info-item">
        <label for="salary">연봉 (만원)</label>
        <div class="input-group">
          <input type="number" class="form-control" id="salary" v-model.number="editableUser.salary">
        </div>
      </div>

      <div class="info-item">
        <label for="wealth">자산 (만원)</label>
        <div class="input-group">
          <input type="number" class="form-control" id="wealth" v-model.number="editableUser.wealth">
        </div>
      </div>
      
      <div class="d-flex justify-content-end mt-4">
        <button type="submit" class="btn btn-primary">수정 완료</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore();
const editableUser = ref({
  nickname: '',
  age: null,
  salary: null,
  wealth: null,
});

watch(() => accountStore.user, (newUser) => {
  if (newUser) {
    editableUser.value = { ...newUser };
  }
}, { immediate: true });

const updateProfile = () => {
  const payload = {
    nickname: editableUser.value.nickname,
    age: editableUser.value.age,
    salary: editableUser.value.salary,
    wealth: editableUser.value.wealth,
  };
  accountStore.updateUser(payload);
};
</script>

<style scoped>
.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.info-item label {
  width: 100px;
  font-weight: bold;
  color: #555;
  flex-shrink: 0;
}
.info-item .input-group {
  flex-grow: 1;
}
.btn-primary {
  background-color: #34495e;
  border-color: #34495e;
}
.btn-primary:hover {
  background-color: #2c3e50;
  border-color: #2c3e50;
}
</style>