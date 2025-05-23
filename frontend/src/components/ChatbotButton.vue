<template>
  <div class="chatbot-container">
    <button v-if="!isChatOpen" @click="toggleChat" class="chatbot-toggle-button">
      <img :src="characterIcon" alt="챗봇 열기" class="chatbot-button-icon"/>
    </button>

    <div v-if="isChatOpen" class="chat-window">
      <div class="chat-header">
        <span>YC 챗봇</span>
        <button @click="toggleChat" class="close-chat-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
      <div class="chat-body" ref="chatBody">
        <div v-for="(message, index) in messages" :key="index" :class="['message-wrapper', message.sender === 'bot' ? 'bot-wrapper' : 'user-wrapper']">
          <div :class="['message-bubble', message.sender]">
            <div v-if="message.sender === 'bot'" class="bot-message-content">
              <img :src="characterIcon" alt="봇 아바타" class="bot-avatar"/>
              <p>{{ message.text }}</p>
            </div>
            <p v-else>{{ message.text }}</p>
          </div>
        </div>
        <div v-if="isLoading" class="message-wrapper bot-wrapper">
          <div class="message-bubble bot">
            <div class="bot-message-content">
              <img :src="characterIcon" alt="봇 아바타" class="bot-avatar"/>
              <p>답변을 생성 중입니다...</p>
            </div>
          </div>
        </div>
      </div>
      <div class="chat-footer">
        <input
          type="text"
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="메시지를 입력하세요..."
          :disabled="isLoading"
        />
        <button @click="sendMessage" :disabled="isLoading">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import OpenAI from 'openai';
// 1. 캐릭터 이미지 import (src/assets 폴더에 이미지가 있다고 가정)
import characterIcon from '@/assets/cutebono.png'; // 파일명을 실제 이미지 파일명으로 변경하세요.

const OPENAI_API_KEY = import.meta.env.VITE_OPEN_AI_API_KEY;
const openai = OPENAI_API_KEY ? new OpenAI({ apiKey: OPENAI_API_KEY, dangerouslyAllowBrowser: true }) : null;

const isChatOpen = ref(false);
const userInput = ref('');
const messages = ref([]);
const isLoading = ref(false);
const chatBody = ref(null);

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
  if (isChatOpen.value && messages.value.length === 0) {
    messages.value.push({ sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?' });
  }
  if(isChatOpen.value) {
    scrollToBottom();
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  if (!userInput.value.trim()) return;
  if (!openai) {
    messages.value.push({ sender: 'user', text: userInput.value });
    messages.value.push({ sender: 'bot', text: 'OpenAI API 키가 설정되지 않았습니다.' });
    userInput.value = '';
    scrollToBottom();
    return;
  }

  const userMessage = userInput.value;
  messages.value.push({ sender: 'user', text: userMessage });
  userInput.value = '';
  isLoading.value = true;
  scrollToBottom();

  try {
    const completion = await openai.chat.completions.create({
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        ...messages.value.filter(msg => msg.sender === 'user' || msg.sender === 'bot').map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        })),
        { role: 'user', content: userMessage }
      ],
      model: 'gpt-3.5-turbo',
    });

    const botResponse = completion.choices[0]?.message?.content?.trim();
    if (botResponse) {
      messages.value.push({ sender: 'bot', text: botResponse });
    } else {
      messages.value.push({ sender: 'bot', text: '죄송합니다. 답변을 생성하는데 실패했습니다.' });
    }
  } catch (error) {
    console.error('OpenAI API 호출 오류:', error);
    messages.value.push({ sender: 'bot', text: '오류가 발생했습니다. 잠시 후 다시 시도해주세요.' });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

/* 챗봇 토글 버튼 스타일 수정 */
.chatbot-toggle-button {
  background-color: transparent; /* 배경색 투명으로 변경 */
  border: none;                 /* 테두리 제거 */
  border-radius: 50%;           /* 아이콘이 원형이 아니라면 이 부분도 조절 가능 */
  width: 60px;                  /* 아이콘 크기에 맞춰 조절 (아래 아이콘 크기와 동일하게) */
  height: 60px;                 /* 아이콘 크기에 맞춰 조절 (아래 아이콘 크기와 동일하게) */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  padding: 0;                   /* 패딩 제거 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 기존 그림자 유지 */
  /* transition 은 box-shadow 등에 적용될 수 있으나, 배경색 변경이 없으므로 수정 또는 제거 가능 */
  transition: transform 0.2s ease; /* 클릭/호버 시 약간의 인터랙션 효과 */
}

.chatbot-toggle-button:hover {
  /* background-color: #0056b3; 배경색 변경 효과 제거 */
  transform: scale(1.1); /* 호버 시 약간 확대되는 효과 (선택 사항) */
}

/* 챗봇 토글 버튼 내부 아이콘 이미지 스타일 수정 */
.chatbot-button-icon {
  width: 50px;  /* 버튼 크기에 맞게 원하는 크기로 설정 (예: 50px) */
  height: 50px; /* 버튼 크기에 맞게 원하는 크기로 설정 (예: 50px) */
  object-fit: cover;
  /* border-radius: 50%; 이미지가 원형일 경우, 캐릭터 모양에 따라 조정 */
}

.chat-window {
  width: 350px;
  height: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.close-chat-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
}

.chat-body {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.message-wrapper {
  display: flex;
  margin-bottom: 10px;
  width: 100%;
}

.message-wrapper.user-wrapper {
  justify-content: flex-end;
}

.message-wrapper.bot-wrapper {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 15px;
  font-size: 0.9em;
  word-wrap: break-word;
}

.message-bubble.user {
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 5px;
}

.message-bubble.bot {
  background-color: transparent;
  padding: 0;
  display: flex;
}

.bot-message-content {
  display: flex;
  align-items: flex-start;
  background-color: #e9ecef;
  color: #333;
  padding: 8px 12px;
  border-radius: 15px;
  border-bottom-left-radius: 5px;
}

/* 봇 아바타 이미지 스타일 수정 */
.bot-avatar {
  width: 50px;   /* 기존 30px 에서 크기 증가 (예: 40px) */
  height: 50px;  /* 기존 30px 에서 크기 증가 (예: 40px) */
  border-radius: 50%;
  margin-right: 10px; /* 텍스트와의 간격, 필요시 조정 */
  flex-shrink: 0;
  object-fit: cover;
}

.message-bubble.bot .bot-message-content p {
  margin: 0;
}

.chat-footer {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.chat-footer input[type="text"] {
  flex-grow: 1;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 8px 12px;
  margin-right: 10px;
  font-size: 0.9em;
}

.chat-footer input[type="text"]:disabled {
  background-color: #f8f9fa;
}

.chat-footer button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
}

.chat-footer button:hover {
  background-color: #0056b3;
}

.chat-footer button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}
</style>