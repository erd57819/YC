<template>
  <div class="search-view-container">
    <h2 class="page-title">관심 정보 검색</h2>
    <div class="search-bar-container">
      <form @submit.prevent="performSearch" class="search-form">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="무엇이 궁금하시나요?"
          class="search-input"
        />
        <button type="submit" class="search-button">찾기</button>
      </form>
    </div>

    <div v-if="searchResults.length > 0" class="results-grid">
      <div
        v-for="video in searchResults"
        :key="video.id.videoId"
        class="result-card"
        @click="goToVideo(video)"
      >
        <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title" class="card-thumbnail" />
        <div class="card-content">
          <h5 class="card-title">{{ video.snippet.title }}</h5>
          <div class="card-meta">
            <p class="card-channel">{{ video.snippet.channelTitle }}</p>
            <p v-if="video.statistics" class="card-views">
              조회수 {{ formatViewCount(video.statistics.viewCount) }}
            </p>
          </div>
          <p class="card-date">{{ new Date(video.snippet.publishTime).toLocaleDateString() }}</p>
        </div>
      </div>
    </div>
    <div v-else-if="isLoading" class="loading-state">
      <p>검색 중...</p>
    </div>
    <div v-else class="no-results">
      <p>검색 결과가 없습니다. 관심 있는 키워드를 검색해보세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useYouTube } from '@/stores/useYouTube';

const searchQuery = ref('');
const searchResults = ref([]);
const isLoading = ref(false);
const router = useRouter();
const { searchVideos, fetchVideosByIds } = useYouTube();

const formatViewCount = (count) => {
  if (!count) return '0회';
  if (count >= 100000000) {
    return `${(count / 100000000).toFixed(1)}억회`;
  }
  if (count >= 10000) {
    return `${Math.round(count / 10000)}만회`;
  }
  return `${count}회`;
};

const performSearch = async () => {
  if (!searchQuery.value.trim()) {
    alert('검색어를 입력해주세요.');
    return;
  }
  isLoading.value = true;
  searchResults.value = [];

  try {
    const initialVideos = await searchVideos(searchQuery.value, 12);
    if (initialVideos.length === 0) {
      isLoading.value = false;
      return;
    }

    const videoIds = initialVideos.map(video => video.id.videoId);
    const detailedVideos = await fetchVideosByIds(videoIds);
    const detailedVideosMap = new Map(detailedVideos.map(video => [video.id, video]));

    const combinedResults = initialVideos.map(video => {
      const details = detailedVideosMap.get(video.id.videoId);
      return {
        ...video,
        statistics: details ? details.statistics : null,
      };
    });

    searchResults.value = combinedResults;
  } catch (error) {
    console.error('검색 중 오류가 발생했습니다.', error);
    alert('동영상을 검색하는 중 오류가 발생했습니다.');
  } finally {
    isLoading.value = false;
  }
};

const goToVideo = (video) => {
  router.push({
    name: 'video',
    params: { id: video.id.videoId },
    query: {
      title: video.snippet.title,
      channelTitle: video.snippet.channelTitle,
      publishTime: video.snippet.publishTime,
      viewCount: video.statistics ? video.statistics.viewCount : '0',
    },
  });
};
</script>

<style scoped>
.search-view-container {
  padding: 40px;
  background-color: #f4f6f9;
  min-height: 100vh;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: left;
  color: #333;
}

.search-bar-container {
  background-color: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-width: 700px;
  margin: 0 auto 2.5rem;
}

/* === ▼▼▼ 검색창 스타일 수정 ▼▼▼ === */
.search-form {
  display: flex;
  /* gap을 제거하고, form 자체에 둥근 테두리를 적용합니다 */
  border-radius: 50px;
  border: 1px solid #dcdfe6;
  overflow: hidden; /* 내부 요소가 테두리를 벗어나지 않도록 합니다 */
  transition: border-color 0.2s, box-shadow 0.2s;
}

/* input에 포커스가 될 때, 전체 form의 스타일을 변경합니다 */
.search-form:focus-within {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.search-input {
  flex-grow: 1;
  /* 개별 테두리와 둥근 모서리를 제거합니다 */
  border: none;
  border-radius: 0;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  background-color: transparent;
  outline: none; /* 포커스 시 기본 테두리 제거 */
}

/* input의 개별 포-커스 효과는 제거합니다 */
.search-input:focus {
  box-shadow: none;
}

.search-button {
  padding: 0.75rem 1.5rem;
  background-color: #343a40;
  color: white;
  border: none;
  /* 개별 둥근 모서리를 제거합니다 */
  border-radius: 0;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}
/* === ▲▲▲ 검색창 스타일 수정 ▲▲▲ === */

.search-button:hover {
  background-color: #495057;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.result-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #e0e0e0;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
  border-color: #c0c0c0;
}

.card-thumbnail {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-content {
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #303133;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.8em;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 0.5rem;
}

.card-channel, .card-views {
  font-size: 0.85rem;
  color: #606266;
  margin: 0;
}

.card-date {
  font-size: 0.8rem;
  color: #909399;
  margin-top: 0.25rem;
  text-align: right;
}

.loading-state, .no-results {
  text-align: center;
  margin-top: 4rem;
  color: #6c757d;
  font-size: 1.1rem;
}
</style>