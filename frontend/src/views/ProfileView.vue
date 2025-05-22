<template>
  <div class="profile-view container mt-5" v-if="store.currentUser">
    <h2>{{ store.currentUser.username }}님의 프로필</h2>

    <div class="card mb-4">
      <div class="card-header">기본 정보</div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item"><strong>사용자 이름:</strong> {{ store.currentUser.username }}</li>
        <li class="list-group-item"><strong>이메일:</strong> {{ store.currentUser.email }}</li>
        <li class="list-group-item"><strong>나이:</strong> {{ store.currentUser.age }}</li>
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
            <label for="subscribed_products" class="form-label">가입 상품 ID (쉼표로 구분)</label>
            <input type="text" class="form-control" id="subscribed_products" v-model="editableProfile.subscribed_products">
            <small class="form-text text-muted">상품 ID를 쉼표(,)로 구분하여 입력하세요. (예: P001,P002)</small>
          </div>
          <button type="submit" class="btn btn-primary">프로필 업데이트</button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header">가입한 금융 상품 목록</div>
      <div class="card-body">
        <p v-if="!store.currentUser.subscribed_products_display || store.currentUser.subscribed_products_display.length === 0">
          가입한 금융 상품이 없습니다.
        </p>
        <ul v-else class="list-group">
          <li v-for="productId in store.currentUser.subscribed_products_display" :key="productId" class="list-group-item">
            상품 ID: {{ productId }} (상세 정보 및 금리 차트 연동 필요)
          </li>
        </ul>
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
import { ref, onMounted, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()
const editableProfile = ref({
  email: '',
  age: null,
  first_name: '',
  last_name: '',
  subscribed_products: '', // 쉼표로 구분된 문자열로 관리
})

// currentUser가 변경될 때마다 editableProfile을 업데이트
watch(() => store.currentUser, (newUser) => {
  if (newUser) {
    editableProfile.value = {
      email: newUser.email || '',
      age: newUser.age || null,
      first_name: newUser.first_name || '',
      last_name: newUser.last_name || '',
      // subscribed_products는 백엔드에서 쉼표 구분 문자열로 오므로 그대로 사용
      subscribed_products: newUser.subscribed_products || '', 
    }
  }
}, { immediate: true }) // 즉시 실행하여 초기 마운트 시에도 적용

const handleUpdateProfile = async () => {
  try {
    // subscribed_products는 이미 문자열이므로 별도 변환 불필요
    const payload = { ...editableProfile.value };
    await store.updateUserProfile(payload)
    // 성공 시 store의 currentUser가 자동으로 업데이트되므로 editableProfile도 watch에 의해 갱신됨
  } catch (error) {
    // 에러 처리는 store에서 이미 alert로 하고 있음
    console.error("프로필 업데이트 중 컴포넌트 에러:", error)
  }
}

onMounted(() => {
  if (!store.currentUser && store.token) {
    store.getUserProfile() // currentUser가 없으면 프로필 정보 다시 요청
  }
})
</script>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: auto;
}
</style>