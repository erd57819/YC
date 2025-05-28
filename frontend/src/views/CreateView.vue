<template>
  <div class="create-view">
    <h1 class="mb-4">개시글 작성</h1>
    <form @submit.prevent="createArticleHandler" class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input type="text" class="form-control" id="title" v-model.trim="title" required>
        <div class="invalid-feedback">
          Please enter a title.
        </div>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea class="form-control" id="content" rows="10" v-model.trim="content" required></textarea>
        <div class="invalid-feedback">
          Please enter some content.
        </div>
      </div>
      <button type="submit" class="btn btn-primary">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const title = ref('')
const content = ref('')
const store = useArticleStore()
const accountStore = useAccountStore()
const router = useRouter()

onMounted(() => {
  // 로그인하지 않은 경우 로그인 페이지로 리디렉션
  if (!accountStore.isLogin) {
    alert('Please log in to create an article.')
    router.push({ name: 'LogInView' })
  }

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

const createArticleHandler = () => {
  if (!title.value || !content.value) {
    // 폼 유효성 검사에 걸리도록 하고, 수동으로 클래스 추가 (Bootstrap 기본 동작 활용)
    const form = document.querySelector('.needs-validation')
    if (form) {
      form.classList.add('was-validated')
    }
    return;
  }
  store.createArticle({ title: title.value, content: content.value }) //
}
</script>

<style scoped>
.create-view {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}
</style>