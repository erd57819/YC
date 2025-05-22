<template>
  <div class="container mt-5">
    <h2>회원가입</h2>
    <form @submit.prevent="performSignUp">
      <div class="mb-3">
        <label for="username" class="form-label">사용자 이름</label>
        <input type="text" class="form-control" id="username" v.model.trim="username" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input type="email" class="form-control" id="email" v.model.trim="email" required>
      </div>
      <div class="mb-3">
        <label for="age" class="form-label">나이</label>
        <input type="number" class="form-control" id="age" v.model.number="age" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input type="password" class="form-control" id="password" v.model="password" required>
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input type="password" class="form-control" id="password2" v.model="password2" required>
      </div>
      <button type="submit" class="btn btn-primary">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const username = ref('')
const email = ref('')
const age = ref(null)
const password = ref('')
const password2 = ref('')

const store = useAccountStore()

const performSignUp = () => {
  if (password.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }
  store.signUp({
    username: username.value,
    email: email.value,
    age: age.value,
    password: password.value,
    password2: password2.value,
  })
}
</script>

<style scoped>
/* 필요한 경우 스타일 추가 */
</style>