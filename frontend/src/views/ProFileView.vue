<template>
  <div class="profile-container my-5">
    <div v-if="accountStore.user" class="profile-layout">
      <div class="sidebar">
        <ul class="nav flex-column">
          <li class="nav-item">
            <a class="nav-link disabled" href="#">포트폴리오 수정</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="#">기본 정보 수정</a>
          </li>
        </ul>
      </div>

      <div class="content">
        <h3>{{ accountStore.user.username }}님의 프로필 페이지</h3>
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
    </div>
    <div v-else class="text-center">
      <p>로그인 후 이용해주세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore();
const editableUser = ref({
  nickname: '',
  age: 0,
  salary: 0,
  wealth: 0,
});

// 컴포넌트가 마운트되거나 user 정보가 변경될 때 editableUser를 최신화합니다.
onMounted(() => {
  if (accountStore.user) {
    Object.assign(editableUser.value, accountStore.user);
  }
});

// 로그인 상태가 변경될 때 (페이지 새로고침 등) 다시 데이터를 할당합니다.
watch(() => accountStore.user, (newUser) => {
  if (newUser) {
    Object.assign(editableUser.value, newUser);
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
.profile-container {
  max-width: 960px;
  margin: auto;
}
.profile-layout {
  display: flex;
}
.sidebar {
  flex: 0 0 200px;
  border-right: 1px solid #dee2e6;
  padding-right: 20px;
}
.sidebar .nav-link {
  color: #333;
  font-weight: bold;
}
.sidebar .nav-link.active {
  color: #0d6efd;
  background-color: #e9ecef;
}
.sidebar .nav-link.disabled {
  color: #adb5bd;
}

.content {
  flex-grow: 1;
  padding-left: 30px;
}

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

.form-control[readonly] {
  background-color: #f8f9fa;
  cursor: not-allowed;
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