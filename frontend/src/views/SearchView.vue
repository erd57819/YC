<script setup>
import { ref } from 'vue'
import { useYouTube } from '@/stores/useYouTube'
import VideoCard from '@/components/VideoCard.vue'

const query  = ref('')
const videos = ref([])
const loading = ref(false)
const { searchVideos } = useYouTube()


const onSearch = async () => {
  if (!query.value.trim()) return
  loading.value = true
  videos.value  = await searchVideos(query.value)
  loading.value = false
}
</script>

<template>
<form class="search-box d-flex align-items-center gap-2 mb-4" @submit.prevent="onSearch">
  <i class="bi bi-search search-icon"></i>
  <input
    v-model="query"
    class="form-control input-search shadow-sm"
    placeholder="검색어를 입력하세요"
  />
  <button type="submit" class="btn btn-primary">검색</button>
</form>

  <div class="container">
    <div v-if="loading" class="text-center py-5">로딩 중…</div>

    <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
      <div v-for="v in videos" :key="v.id.videoId" class="col">
        <VideoCard :video="v" class="h-100" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-box {
  flex-direction: row; 
}

.search-box button.btn {
  white-space: nowrap;
  min-width: 60px;
}
</style>