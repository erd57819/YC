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
import { useAccountStore } from '@/stores/accounts' //

const store = useAccountStore()
const editableProfile = ref({
  // username은 수정 폼에서 직접 관리하지 않고, store.currentUser의 값을 사용합니다.
  email: '',
  age: null,
  first_name: '',
  last_name: '',
  subscribed_products: '',
})

// store.currentUser가 변경될 때 (예: 최초 로드 또는 업데이트 후) editableProfile 동기화
watch(() => store.currentUser, (newUser) => {
  if (newUser) {
    editableProfile.value.email = newUser.email || '';
    editableProfile.value.age = newUser.age || null;
    editableProfile.value.first_name = newUser.first_name || '';
    editableProfile.value.last_name = newUser.last_name || '';
    editableProfile.value.subscribed_products = newUser.subscribed_products || '';
  }
}, { immediate: true, deep: true }) // deep: true는 currentUser 객체 내부 변경 감지 (선택 사항)

const handleUpdateProfile = async () => {
  try {
    // 현재 로그인한 사용자의 username을 payload에 포함하여 전송합니다.
    if (!store.currentUser || !store.currentUser.username) {
        alert('사용자 정보를 정확히 불러올 수 없습니다. 잠시 후 다시 시도하거나 재로그인 해주세요.');
        return;
    }

    const payload = {
      username: store.currentUser.username, // 현재 사용자의 username을 사용 (변경 불가로 가정)
      email: editableProfile.value.email,
      age: editableProfile.value.age,
      first_name: editableProfile.value.first_name,
      last_name: editableProfile.value.last_name,
      subscribed_products: editableProfile.value.subscribed_products,
    };
    await store.updateUserProfile(payload)
    // 성공 시 store.updateUserProfile 내부에서 currentUser가 업데이트되고,
    // watch에 의해 editableProfile도 최신 정보로 동기화될 수 있습니다.
    // 필요하다면 여기서 추가적인 성공 알림이나 페이지 이동 로직을 넣을 수 있습니다.
  } catch (error) {
    // 에러 처리는 store의 updateUserProfile에서 이미 alert로 하고 있음
    console.error("프로필 업데이트 중 컴포넌트 에러:", error)
  }
}

onMounted(() => {
  // 페이지 마운트 시 store에 currentUser 정보가 없으면 가져오도록 시도
  if (!store.currentUser && store.token) {
    store.getUserProfile();
  }
})
</script>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: auto;
}
</style>