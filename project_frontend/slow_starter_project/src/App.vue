<template>
  <div> 
    <!-- 임시로 해놓은 것임! 마지막에 변경할 것! -->
     <!-- CommenHeader컴포넌트, Home뷰 배치하기. -->
  <header>
    <CommonHeaderComponent/>
    <RouterView/>
    
  </header>

      <!-- 챗봇 버튼 (우측 하단 고정) -->
      <div class="chatbot-container">
      <v-btn
        color="blue"
        icon="mdi-message-text"
        size="large"
        @click="openChatbot"
        class="chatbot-button"
      >
        <v-icon>mdi-robot</v-icon>
      </v-btn>
    </div>

    <!-- 챗봇 모달 컴포넌트 -->
    <ModalChatBotComponent 
      v-model="showChatbot" 
      @close="closeChatbot"
    />
  


  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import ModalChatBotComponent from '@/components/ModalChatBotComponent.vue';
import CommonHeaderComponent from './components/CommonHeaderComponent.vue';

const showChatbot = ref(false);

const openChatbot = () => {
  showChatbot.value = true;
};

const closeChatbot = () => {
  showChatbot.value = false;
};

import { onMounted } from 'vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()

onMounted(async () => {
  await userStore.initializeAuth()
  // 디버깅용 콘솔 로그
  console.log('Token:', localStorage.getItem('token'))
  console.log('UserId:', localStorage.getItem('userId'))
  console.log('UserInfo:', userStore.userInfo)
})

</script>



<style scoped>

.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}

.chatbot-button:hover {
  transform: scale(1.1);
}

</style>