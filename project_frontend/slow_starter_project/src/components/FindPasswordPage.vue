<template>
    <v-container>
      <v-card class="mx-auto pa-8 pt-10 pb-4" elevation="4" max-width="448" rounded="lg">
        <v-card-title class="text-center text-h5 mb-6">
          비밀번호 찾기
        </v-card-title>
  
        <v-form ref="form" @submit.prevent="handleSubmit" v-model="isFormValid">
          <v-text-field
            v-model="username"
            :rules="[rules.required]"
            label="아이디"
            placeholder="아이디를 입력하세요"
            variant="outlined"
            class="mb-4"
            hide-details="auto"
          ></v-text-field>
  
          <v-text-field
            v-model="email"
            :rules="[rules.required, rules.email]"
            label="이메일"
            placeholder="이메일을 입력하세요"
            variant="outlined"
            class="mb-6"
            hide-details="auto"
          ></v-text-field>
  
          <v-row justify="end" class="mt-4">
            <v-col cols="auto">
              <v-btn
                color="primary"
                class="me-4"
                @click="handleSubmit"
                :disabled="!isFormValid"
                :loading="loading"
              >
                임시비밀번호 생성
              </v-btn>
              <v-btn
                color="grey-lighten-1"
                @click="goToLogin"
              >
                되돌아가기
              </v-btn>
            </v-col>
          </v-row>
  
          <div class="text-center message-container" v-if="showMessage">
            <div :class="['message-box', messageType]">
              {{ message }}
            </div>
          </div>
        </v-form>
  
        <!-- 임시비밀번호 생성 완료 모달 -->
        <TemporaryPassword
          v-if="showTempPassword"
          :show="showTempPassword"
          :temp-password="tempPassword"
          @update:show="handleModalClose"
        />
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import TemporaryPassword from './TemporaryPassword.vue'
  
  const router = useRouter()
  const userStore = useUserStore()
  const form = ref(null)
  
  // Form fields
  const username = ref('')
  const email = ref('')
  const isFormValid = ref(false)
  const loading = ref(false)
  
  // Message handling
  const showMessage = ref(false)
  const message = ref('')
  const messageType = ref('')
  
  // Modal handling
  const showTempPassword = ref(false)
  const tempPassword = ref('')
  
  // Validation rules
  const rules = {
    required: value => !!value || '필수 입력 항목입니다',
    email: value => {
      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return pattern.test(value) || '유효한 이메일 주소를 입력해주세요'
    }
  }
  
  // Form submission handler
  const handleSubmit = async () => {
    if (!isFormValid.value) return
  
    loading.value = true
    showMessage.value = false
  
    try {
      const response = await userStore.findPassword({
        username: username.value,
        email: email.value
      });
  
      if (response.success) {
        tempPassword.value = response.tempPassword
        showTempPassword.value = true
        message.value = ''
        showMessage.value = false
      } else {
        message.value = response.message
        messageType.value = 'error'
        showMessage.value = true
      }
    } catch (error) {
      message.value = '서버 오류가 발생했습니다.'
      messageType.value = 'error'
      showMessage.value = true
    } finally {
      loading.value = false
    }
  }
  
  // Navigation handlers
  const goToLogin = () => {
    router.push('/login')
  }
  
  const handleModalClose = (value) => {
    showTempPassword.value = value
    if (!value) {
      // Modal이 닫힐 때 로그인 페이지로 이동
      router.push('/login')
    }
  }
  
  // Reset form
  const resetForm = () => {
    if (form.value) {
      form.value.reset()
    }
    username.value = ''
    email.value = ''
    showMessage.value = false
    message.value = ''
    loading.value = false
  }
  </script>
  
  <style scoped>
  .message-container {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
  }
  
  .message-box {
    padding: 12px 24px;
    border-radius: 4px;
    font-weight: 500;
    width: 100%;
  }
  
  .message-box.error {
    background-color: #ffebee;
    color: #d32f2f;
    border: 1px solid #ffcdd2;
  }
  
  .message-box.success {
    background-color: #e8f5e9;
    color: #2e7d32;
    border: 1px solid #c8e6c9;
  }
  
  .v-btn {
    text-transform: none;
  }
  
  /* Form field spacing */
  .v-text-field {
    margin-bottom: 16px;
  }
  
  /* Card responsiveness */
  @media (max-width: 600px) {
    .v-card {
      margin: 0;
      padding: 16px !important;
    }
    
    .v-row {
      margin: 0;
    }
    
    .v-col {
      padding: 8px 0;
    }
  }
  </style>