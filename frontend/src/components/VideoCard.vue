<script setup>
import { useRouter } from 'vue-router'
defineProps({ video: Object })
const router = useRouter()
const open = (id) => router.push({ name: 'video', params: { id } })
</script>

<template>
  <div class="card h-100">
    <img
      :src="video.snippet.thumbnails.medium.url"
      class="card-img-top"
      :alt="video.snippet.title"
      @click="open(video.id.videoId)"
      style="cursor: pointer"
    />
    <div class="card-body">
      <h6 class="card-title">{{ video.snippet.title }}</h6>
      <p class="card-text text-muted mb-0">{{ video.snippet.channelTitle }}</p>
    </div>
    <slot></slot>
  </div>
</template>
