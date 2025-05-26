import axios from 'axios'
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const BASE = 'https://www.googleapis.com/youtube/v3'

export function useYouTube() {
  const searchVideos = async (q, maxResults = 50) => {
    const { data } = await axios.get(`${BASE}/search`, {
      params: {
        key: API_KEY,
        part: 'snippet',
        type: 'video',
        q,
        maxResults
      }
    })
    return data.items
  }

  const fetchVideoDetail = async (videoId) => {
    const { data } = await axios.get(`${BASE}/videos`, {
      params: {
        key: API_KEY,
        id: videoId,
        part: 'snippet,statistics,contentDetails' // 여기 statistics가 이미 있네요!
      }
    })
    return data.items[0]
  }
  
  // 여러 비디오의 정보를 ID를 기반으로 한 번에 가져오는 함수 추가
  const fetchVideosByIds = async (videoIds) => {
    const { data } = await axios.get(`${BASE}/videos`, {
      params: {
        key: API_KEY,
        id: videoIds.join(','), // ID 목록을 콤마로 연결
        part: 'statistics,snippet' // 필요한 정보만 요청
      }
    });
    return data.items;
  }


  const fetchChannel = async (channelId) => {
    const { data } = await axios.get(`${BASE}/channels`, {
      params: {
        key: API_KEY,
        id: channelId,
        part: 'snippet,statistics'
      }
    })
    return data.items[0]
  }

  // 새로 추가한 함수를 반환 객체에 포함
  return { searchVideos, fetchVideoDetail, fetchChannel, fetchVideosByIds }
}