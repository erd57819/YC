<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const username = ref('')
const password = ref('')
const password2 = ref('') // password1, password2 대신 password와 passwordConfirmation으로 가정
const age = ref(null) // age 필드 추가

const accountStore = useAccountStore()

const signup = function () {
  const payload = {
    username: username.value,
    password1: password.value, // 실제 필드명에 맞게 수정
    password2: password2.value, // 실제 필드명에 맞게 수정
    age: age.value, // age 값 추가
  }
  accountStore.signUp(payload)
}
</script>

<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signup">
      <label for="username">사용자 이름:</label>
      <input type="text" id="username" v-model.trim="username"><br>
      <label for="password">비밀번호:</label>
      <input type="password" id="password" v-model.trim="password"><br>
      <label for="password2">비밀번호 확인:</label>
      <input type="password" id="password2" v-model.trim="password2"><br>
      <label for="age">나이:</label>
      <input type="number" id="age" v-model.trim="age"><br> <input type="submit" value="회원가입">
    </form>
  </div>
</template>

<style scoped>

</style>