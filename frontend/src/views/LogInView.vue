<template>
  <div class="login-view">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="card-title text-center mb-4">로그인</h1>
            <form @submit.prevent="submitLogIn" class="needs-validation" novalidate>
              <div class="mb-3">
                <label for="username" class="form-label">아이디</label>
                <input type="text" class="form-control" id="username" v-model.trim="username" required>
                <div class="invalid-feedback">
                  아이디를 입력해주세요.
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">비밀번호</label>
                <input type="password" class="form-control" id="password" v-model.trim="password" required>
                <div class="invalid-feedback">
                  비밀번호를 입력해주세요.
                </div>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">로그인</button>
              </div>
            </form>
            <p class="text-center mt-3">
              계정이 없으신가요? <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const username = ref('')
const password = ref('')
const accountStore = useAccountStore()

onMounted(() => {
  const forms = document.querySelectorAll('.needs-validation')
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })
})

const submitLogIn = () => {
  const form = document.querySelector('.needs-validation');
  if (form && !form.checkValidity()) {
    form.classList.add('was-validated');
    return;
  }
  accountStore.logIn({ username: username.value, password: password.value }) //
}
</script>

<style scoped>
.login-view {
  padding-top: 40px;
  padding-bottom: 40px;
}
.card {
  border: none;
}
</style>