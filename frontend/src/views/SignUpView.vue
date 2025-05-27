<template>
  <div class="signup-view">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h1 class="card-title text-center mb-4">회원가입</h1>
            <form @submit.prevent="submitSignUp" class="needs-validation" novalidate>
              <div class="mb-3">
                <label for="username" class="form-label">아이디</label>
                <input type="text" class="form-control" id="username" v-model.trim="username" required>
                <div class="invalid-feedback">
                  아이디를 입력해주세요.
                </div>
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">비밀번호</label>
                <input type="password" class="form-control" id="password" v-model.trim="password" required minlength="8">
                <div class="invalid-feedback">
                  비밀번호를 입력해주세요. (최소 8자)
                </div>
              </div>

              <div class="mb-3">
                <label for="confirmPassword" class="form-label">비밀번호확인</label>
                <input type="password" class="form-control" id="confirmPassword" v-model.trim="confirmPassword" required>
                <div class="invalid-feedback" v-if="password !== confirmPassword && confirmPassword">
                  비밀번호가 일치하지 않습니다.
                </div>
                 <div class="invalid-feedback" v-else>
                  비밀번호를 다시 입력해주세요.
                </div>
              </div>


              <div class="mb-3">
                <label for="nickname" class="form-label">닉네임</label>
                <input type="text" class="form-control" id="nickname" v-model.trim="nickname">
              </div>

              <div class="mb-3">
                <label for="age" class="form-label">나이</label>
                <input type="number" class="form-control" id="age" v-model.number="age" min="1">
              </div>

              <div class="mb-3">
                <label for="salary" class="form-label">연봉</label>
                <input type="number" class="form-control" id="salary" v-model.number="salary" min="0">
              </div>

              <div class="mb-3">
                <label for="wealth" class="form-label">총 자산</label>
                <input type="number" class="form-control" id="wealth" v-model.number="wealth" min="0">
              </div>

              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-primary btn-lg">회원가입</button>
              </div>
            </form>
            <p class="text-center mt-3">
              계정이 있으신가요? <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
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
const confirmPassword = ref('')
const nickname = ref('')
const age = ref(null)
const salary = ref(null)
const wealth = ref(null)

const accountStore = useAccountStore()

onMounted(() => {
  const forms = document.querySelectorAll('.needs-validation')
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity() || password.value !== confirmPassword.value) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })
})

const submitSignUp = () => {
  if (password.value !== confirmPassword.value) {
    const form = document.querySelector('.needs-validation');
    if (form) form.classList.add('was-validated');
    return
  }
  
  const form = document.querySelector('.needs-validation');
  if (form && !form.checkValidity()) {
    form.classList.add('was-validated');
    return;
  }

  const payload = {
    username: username.value,
    password1: password.value, 
    password2: confirmPassword.value,
    nickname: nickname.value,
    age: age.value,
    salary: salary.value,
    wealth: wealth.value,
  }

  Object.keys(payload).forEach(key => {
    if (payload[key] === null || payload[key] === '') {
      delete payload[key];
    }
  });

  accountStore.signUp(payload)
}
</script>

<style scoped>
.signup-view {
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f8f9fa;
}
.card {
  border: none;
}
</style>