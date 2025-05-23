<template>
  <div class="chatbot-container">
    <button v-if="!isChatOpen" @click="toggleChat" class="chatbot-toggle-button">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-message-square"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
    </button>

    <div v-if="isChatOpen" class="chat-window">
      <div class="chat-header">
        <span>YC 챗봇</span>
        <button @click="toggleChat" class="close-chat-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
      <div class="chat-body" ref="chatBody">
        <div v-for="(message, index) in messages" :key="index" :class="['message-bubble', message.sender]">
          <p>{{ message.text }}</p>
        </div>
        <div v-if="isLoading" class="message-bubble bot">
          <p>답변을 생성 중입니다...</p>
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

const OPENAI_API_KEY = import.meta.env.VITE_OPEN_AI_API_KEY;
const openai = OPENAI_API_KEY ? new OpenAI({ apiKey: OPENAI_API_KEY, dangerouslyAllowBrowser: true }) : null;

const isChatOpen = ref(false);
const userInput = ref('');
const messages = ref([]);
const isLoading = ref(false);
const chatBody = ref(null); // 채팅창 스크롤을 위한 ref

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
  if (isChatOpen.value && messages.value.length === 0) {
    // 채팅창이 열릴 때 초기 메시지 (선택 사항)
    messages.value.push({ sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?' });
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
        { role: 'system', content: 'You are a helpful assistant.' }, // 챗봇의 역할 설정 (필요에 따라 수정)
        ...messages.value.filter(msg => msg.sender === 'user' || msg.sender === 'bot').map(msg => ({ // 이전 대화 내용 포함 (선택적)
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        })),
        { role: 'user', content: userMessage }
      ],
      model: 'gpt-3.5-turbo', // 사용하려는 모델 선택
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

.chatbot-toggle-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.chatbot-toggle-button:hover {
  background-color: #0056b3;
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

.message-bubble {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 15px;
  margin-bottom: 10px;
  font-size: 0.9em;
  word-wrap: break-word;
}

.message-bubble.user {
  background-color: #007bff;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 5px;
}

.message-bubble.bot {
  background-color: #e9ecef;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 5px;
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