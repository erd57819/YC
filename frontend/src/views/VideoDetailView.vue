<template>
  <div class="video-detail-container">
    <button @click="goBack" class="back-button">← 뒤로가기</button>
    <div class="detail-card">
      <div class="video-player-wrapper">
        <iframe
          v-if="videoId"
          :src="embedUrl"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
          class="video-iframe"
        ></iframe>
      </div>
      <div class="video-info">
        <h2 class="video-title">{{ videoTitle }}</h2>
        <div class="video-meta">
          <span>{{ channelTitle }}</span>
          <span v-if="publishDate"> • {{ publishDate }}</span>
          <span v-if="viewCount"> • 조회수 {{ formattedViewCount }}</span>
        </div>
        <hr class="info-divider" />
        <div class="video-description-container">
          <h3 class="description-title">세부설명</h3>
          <p class="video-description" v-if="videoDescription">{{ videoDescription }}</p>
          <p v-else class="video-description">설명이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useYouTube } from '@/stores/useYouTube';

const route = useRoute();
const router = useRouter();
const { fetchVideoDetail } = useYouTube();

const videoId = ref(route.params.id);
const videoTitle = ref(route.query.title || '제목을 불러오는 중...');
const channelTitle = ref(route.query.channelTitle || '');
const publishTime = ref(route.query.publishTime || '');
const viewCount = ref(route.query.viewCount || '');
const videoDescription = ref('');

const embedUrl = computed(() => {
  return videoId.value ? `https://www.youtube.com/embed/${videoId.value}` : '';
});

const publishDate = computed(() => {
  return publishTime.value ? new Date(publishTime.value).toLocaleDateString() : '';
});

const formatViewCount = (count) => {
  if (!count) return '';
  const num = parseInt(count, 10);
  if (num >= 100000000) {
    return `${(num / 100000000).toFixed(1)}억회`;
  }
  if (num >= 10000) {
    return `${Math.round(num / 10000)}만회`;
  }
  return `${num}회`;
};

const formattedViewCount = computed(() => formatViewCount(viewCount.value));

const loadVideoDetails = async () => {
  if (videoId.value) {
    try {
      const details = await fetchVideoDetail(videoId.value);
      if (details) {
        videoTitle.value = details.snippet?.title || videoTitle.value;
        channelTitle.value = details.snippet?.channelTitle || channelTitle.value;
        publishTime.value = details.snippet?.publishedAt || publishTime.value;
        videoDescription.value = details.snippet?.description || '설명이 제공되지 않았습니다.';
        if (details.statistics?.viewCount) {
          viewCount.value = details.statistics.viewCount;
        }
      }
    } catch (error) {
      console.error('영상 상세 정보를 가져오는 데 실패했습니다:', error);
      videoDescription.value = '설명을 불러오는 데 실패했습니다.';
    }
  }
};

onMounted(() => {
  loadVideoDetails();
});

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.video-detail-container {
  padding: 20px;
  background-color: #f4f6f9; /* 이전 페이지와 유사한 배경 */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.back-button {
  align-self: flex-start;
  margin-bottom: 20px;
  padding: 8px 15px;
  background-color: #fff;
  color: #333;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #f8f9fa;
}

.detail-card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 900px; /* 카드 최대 너비 설정 */
  overflow: hidden; /* 내부 요소가 카드를 벗어나지 않도록 */
}

.video-player-wrapper {
  position: relative;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
  background-color: #000; /* 로딩 중 검은 배경 */
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none; /* iframe 테두리 제거 */
}

.video-info {
  padding: 25px 30px; /* 내부 패딩 증가 */
}

.video-title {
  font-size: 1.8rem; /* 제목 크기 증가 */
  font-weight: 600;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 10px;
  line-height: 1.3;
}

.video-meta {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px 10px; /* 메타 정보 간 간격 */
}

.info-divider {
  border: 0;
  height: 1px;
  background-color: #eef2f7;
  margin: 20px 0;
}

.video-description-container {
  margin-top: 20px;
}

.description-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.video-description {
  font-size: 1rem;
  line-height: 1.7;
  color: #333;
  white-space: pre-wrap; /* 줄바꿈 및 공백 유지 */
  word-break: break-word;
}
</style>