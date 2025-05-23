<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useYouTube } from '@/stores/useYouTube'

const route = useRoute()

const { fetchVideoDetail } = useYouTube()
const video = ref(null)
const loading = ref(true)

onMounted(async () => {
  video.value = await fetchVideoDetail(route.params.id)
  loading.value = false
})
</script>

<template>
  <div class="container py-4" v-if="!loading && video">
    <h3 class="mb-3">{{ video.snippet.title }}</h3>

    <div class="ratio ratio-16x9 mb-3">
      <iframe
        :src="`https://www.youtube.com/embed/${video.id}`"
        title="YouTube video player"
        allowfullscreen
      ></iframe>
    </div>

    <p v-html="video.snippet.description"></p>
  </div>

  <div v-else class="text-center py-5">로딩 중…</div>
</template>

