<template>
  <div class="login-view">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="card-title text-center mb-4">Log In</h1>
            <form @submit.prevent="submitLogIn" class="needs-validation" novalidate>
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" v-model.trim="username" required>
                <div class="invalid-feedback">
                  Please enter your username.
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model.trim="password" required>
                <div class="invalid-feedback">
                  Please enter your password.
                </div>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">Log In</button>
              </div>
            </form>
            <p class="text-center mt-3">
              Don't have an account? <RouterLink :to="{ name: 'SignUpView' }">Sign Up</RouterLink>
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
  // Bootstrap 폼 유효성 검사 스크립트 초기화
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
  // 폼 유효성 검사
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