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
import characterIcon from '@/assets/cutebono.png'; // 이 아이콘 경로는 프로젝트에 맞게 수정해야 할 수 있습니다.

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
    messages.value.push({ sender: 'bot', text: '안녕하세요! YC 금융 챗봇입니다. 무엇을 도와드릴까요?' });
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

  // 금융 전문가 역할을 정의하는 상세 시스템 프롬프트
  const financialSystemPrompt = `
    You are 'YC 금융 챗봇', a specialized financial assistant. Your role is to provide informative and accurate answers strictly about financial topics.

    Your areas of expertise include:
    - Financial products (e.g., deposits, savings, funds, loans)
    - Investment strategies and principles
    - Asset management concepts
    - Explanations of the latest economic news and financial terminology

    You must adhere to the following rules:
    1.  **Never give direct investment advice or recommend specific financial products.** Do not say things like "You should buy this stock" or "This fund is the best option for you."
    2.  Always include a disclaimer that your answers are for informational purposes only. Remind the user to consult with a qualified professional before making any financial decisions.
    3.  Use a friendly, clear, and easy-to-understand tone.
    4.  If asked a question unrelated to finance, you must politely decline by responding with: "죄송하지만, 저는 금융 관련 질문에만 답변할 수 있습니다."
    5.  Keep your answers concise and to the point.
    6.  Answer in Korean.
  `;

  try {
    const completion = await openai.chat.completions.create({
      messages: [
        // 'You are a helpful assistant.'를 상세 프롬프트로 교체
        { role: 'system', content: financialSystemPrompt }, 
        // 이전 대화 내용을 포함하여 문맥 유지
        ...messages.value.filter(msg => msg.sender === 'user' || msg.sender === 'bot').map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        })),
        // 현재 사용자 메시지 포함
        { role: 'user', content: userMessage }
      ],
      model: 'ft:gpt-4o-mini-2024-07-18:personal::BbMFkAM0', // 필요시 'gpt-4' 등 다른 모델로 변경 가능
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
  background-color: transparent; 
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  padding: 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
  transition: transform 0.2s ease; 
}

.chatbot-toggle-button:hover {
  transform: scale(1.1); 
}

.chatbot-button-icon {
  width: 50px;
  height: 50px; 
  object-fit: cover;
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

.bot-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px; 
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