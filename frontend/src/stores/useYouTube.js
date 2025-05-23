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
        part: 'snippet,statistics,contentDetails'
      }
    })
    return data.items[0]
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

  return { searchVideos, fetchVideoDetail, fetchChannel }
}
