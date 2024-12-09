<template>
  <v-dialog
    v-model="localModelValue"
    width="auto"
    :retain-focus="false"
    transition="dialog-bottom-transition"
  >
  <v-card class="chatbot-modal">
    <v-toolbar color="blue" title="금융 상담 챗봇">
      <template v-slot:append>
        <v-btn
          icon="mdi-close"
          @click="handleClose"
          variant="text"
        ></v-btn>
      </template>
    </v-toolbar>
    
    <v-card-text class="pa-0">
      <div class="chatbot-content d-flex flex-column">
        <!-- 메시지 영역 -->
        <v-list ref="messageContainer" class="flex-grow-1 overflow-y-auto pa-4" bg-color="transparent">
          <v-list-item v-for="(message, index) in messages" :key="index">
            <div
              class="message"
              :class="{
                'user-message': message.role === 'user',
                'assistant-message': message.role === 'assistant',
                'system-message': message.role === 'system',
              }"
            >
              <pre class="message-content">{{ message.content }}</pre>
            </div>
          </v-list-item>
        </v-list>

        <!-- 예시 질문 영역 -->
        <div class="example-questions px-4 pb-2" v-if="showExamples">
          <v-chip-group>
            <v-chip
              v-for="(question, index) in exampleQuestions"
              :key="index"
              color="blue-lighten-4"
              @click="sendExampleQuestion(question)"
              class="ma-1"
            >
              {{ question }}
            </v-chip>
          </v-chip-group>
        </div>

        <!-- 입력 영역 -->
        <div class="message-input pa-4">
          <v-progress-linear
            v-if="loading"
            color="blue"
            indeterminate
            class="mb-4"
          ></v-progress-linear>
          
          <div class="d-flex gap-2">
            <v-text-field
              v-model="inputMessage"
              placeholder="질문을 입력하세요..."
              @keyup.enter="handleSubmit"
              hide-details
              variant="outlined"
              class="flex-grow-1"
            >
              <template v-slot:append-inner>
                <v-icon
                  color="blue-lighten-1"
                  @click="toggleExamples"
                >
                  {{ showExamples ? 'mdi-chevron-down' : 'mdi-chevron-up' }}
                </v-icon>
              </template>
            </v-text-field>
            <v-btn
              color="blue"
              @click="handleSubmit"
              :disabled="loading"
              class="px-4"
            >
              전송
            </v-btn>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
 </v-dialog> 
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:modelValue', 'close']);

const localModelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// 상태 관리
const messages = ref([
  { role: 'system', content: '금융상담 챗봇입니다.' },
  { role: 'assistant', content: '안녕하세요! 금융 상품에 대해 궁금하신 점을 물어보세요!' }
]);
const inputMessage = ref('');
const loading = ref(false);
const messageContainer = ref(null);
const showExamples = ref(false);

// 예시 질문 목록
const exampleQuestions = [
  "국민은행 예금 추천해주세요",
  "우리은행에서 가입할만한 적금 있나요?",
  "신한은행 최고금리 상품 알려주세요",
  "지금 제일 금리 높은 상품이 뭐예요?",
  "예금과 적금의 차이가 뭔가요?",
  "1000만원 예금하면 이자가 얼마인가요?"
];

// 은행 상품 데이터
const bankProducts = {
  KB: {
    deposits: [
      { name: "KB Star 정기예금", rate: 3.75, minPeriod: 12, feature: "자유로운 입출금" },
      { name: "KB 특별우대예금", rate: 3.55, minPeriod: 6, feature: "우대금리 제공" }
    ],
    savings: [
      { name: "KB Smart★취적금", rate: 4.45, minPeriod: 12, feature: "모바일 전용" },
      { name: "KB Young Youth 적금", rate: 4.25, minPeriod: 6, feature: "만 39세 이하 가입" }
    ]
  },
  WOORI: {
    deposits: [
      { name: "우리 Super정기예금", rate: 3.80, minPeriod: 12, feature: "고금리 제공" },
      { name: "우리 핫딜예금", rate: 3.60, minPeriod: 3, feature: "단기 상품" }
    ],
    savings: [
      { name: "우리 으쓱적금", rate: 4.50, minPeriod: 12, feature: "자동이체 우대" },
      { name: "우리 데일리적금", rate: 4.30, minPeriod: 6, feature: "수시입금 가능" }
    ]
  },
  SHINHAN: {
    deposits: [
      { name: "신한 피그뱅크예금", rate: 3.70, minPeriod: 12, feature: "온라인 전용" },
      { name: "신한 안신예금", rate: 3.50, minPeriod: 6, feature: "임차보증금 대출용" }
    ],
    savings: [
      { name: "신한 퍼스트적금", rate: 4.40, minPeriod: 12, feature: "첫 거래 우대" },
      { name: "신한 두배드림적금", rate: 4.20, minPeriod: 6, feature: "이벤트 참여 가능" }
    ]
  }
};

// OpenAI API 호출
const getChatbotResponse = async (userInput) => {
  try {
    const response = await axios.post(
      '/api/chat/chat/completions',  // URL을 프록시 설정에 맞게 수정
      {
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: `당신은 금융 전문가입니다. 다음 금융 상품 정보를 바탕으로 상담을 제공해주세요:
            ${JSON.stringify(bankProducts, null, 2)}
            
            주요 규칙:
            1. 예금과 적금의 차이점을 명확히 설명해주세요.
            2. 수익 계산시 구체적인 숫자를 사용해 설명해주세요.
            3. 고객의 상황에 맞는 맞춤형 조언을 제공해주세요.
            4. 실제 계산 예시를 포함해주세요.
            5. 답변은 친절하고 이해하기 쉽게 작성해주세요.`
          },
          ...messages.value,
          { role: "user", content: userInput }
        ]
      }
    );
    
    return {
      success: true,
      content: response.data.choices[0].message.content
    };
  } catch (error) {
    console.error('API Error:', error);
    return {
      success: false,
      error: error.response?.status === 429 ? 'RATE_LIMIT' : 'API_ERROR'
    };
  }
};

// 로컬 응답 생성 (기존 코드와 동일)
const getLocalResponse = (userInput) => {
  // ... (기존 getLocalResponse 함수 내용 유지)
};

// handleSubmit 함수
const handleSubmit = async () => {
  if (!inputMessage.value.trim()) return;

  loading.value = true;
  const userMessage = { role: 'user', content: inputMessage.value };
  messages.value.push(userMessage);

  try {
    const apiResponse = await getChatbotResponse(userMessage.content);
    
    if (apiResponse.success) {
      messages.value.push({ 
        role: 'assistant', 
        content: apiResponse.content 
      });
    } else {
      // API 오류 시 로컬 응답 사용
      const localResponse = getLocalResponse(userMessage.content);
      messages.value.push({ 
        role: 'assistant',
        content: localResponse
      });

      if (apiResponse.error === 'RATE_LIMIT') {
        messages.value.push({
          role: 'system',
          content: '※ 현재 일시적으로 AI 응답이 제한되어 기본 응답으로 안내해드렸습니다. 잠시 후 다시 시도해주세요.'
        });
      }
    }
  } catch (error) {
    console.error('Error:', error);
    const localResponse = getLocalResponse(userMessage.content);
    messages.value.push({ 
      role: 'assistant',
      content: localResponse
    });
  } finally {
    loading.value = false;
    inputMessage.value = '';
    await nextTick();
    scrollToBottom();
  }
};

// 나머지 함수들 (기존과 동일)
const sendExampleQuestion = (question) => {
  inputMessage.value = question;
  handleSubmit();
  showExamples.value = false;
};

const toggleExamples = () => {
  showExamples.value = !showExamples.value;
};

const scrollToBottom = () => {
  if (messageContainer.value) {
    const container = messageContainer.value.$el;
    container.scrollTop = container.scrollHeight;
  }
};

const handleClose = () => {
  emit('close');
};

watch(messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
}, { deep: true });

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chatbot-modal {
  border-radius: 16px;
  overflow: hidden;
}

.chatbot-content {
  height: 600px;
  width: 400px;
}

.example-questions {
  background-color: rgb(241, 245, 249);
  border-top: 1px solid #e0e0e0;
  max-height: 100px;
  overflow-y: auto;
}

.message {
  margin-bottom: 16px;
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 8px;
}

.user-message {
  margin-left: auto;
  background-color: #1976d2;
  color: white;
}

.assistant-message {
  margin-right: auto;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.system-message {
  text-align: center;
  background-color: #e3f2fd;
  margin: 8px auto;
  font-weight: bold;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  margin: 0;
}

.message-input {
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

@media (max-width: 960px) {
  .chatbot-modal {
    width: 90vw;
    max-height: 90vh;
    margin: 0 auto;
  }

  .chatbot-content {
    width: 100%;
    height: 70vh;
  }
}
</style>