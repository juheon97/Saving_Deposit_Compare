<template>
    <div class="password-container">
      <v-card class="pa-6" elevation="2" style="background-color: white;">
        <v-card-title class="text-center text-h5 mb-6">
          비밀번호 변경
        </v-card-title>
  
        <v-form @submit.prevent="handleSubmit" v-model="isFormValid">
          <v-text-field
            v-model="currentPassword"
            :rules="[rules.required]"
            label="현재 비밀번호"
            type="password"
            variant="outlined"
            class="mb-4"
            hide-details="auto"
          ></v-text-field>
  
          <v-text-field
            v-model="newPassword"
            :rules="[rules.required, rules.min]"
            label="새 비밀번호"
            type="password"
            variant="outlined"
            class="mb-4"
            hide-details="auto"
          ></v-text-field>
  
          <v-text-field
            v-model="confirmPassword"
            :rules="[rules.required]"
            label="새 비밀번호 확인"
            type="password"
            variant="outlined"
            class="mb-6"
            hide-details="auto"
          ></v-text-field>
  
          <!-- 에러 메시지를 폼과 버튼 사이에 배치 -->
          <v-row justify="end" class="mt-4">
              <v-col cols="auto">
                  <v-btn
                  color="primary"
                class="me-4"
                @click="handleSubmit"
                :disabled="!isFormValid"
              >
                확인
              </v-btn>
              <v-btn
              color="grey-lighten-1"
              @click="goBack"
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
  
        <!-- 비밀번호 변경 확인 모달 -->
        <PasswordConfirmation
          :show="showConfirmDialog"
          @update:show="showConfirmDialog = $event"
          :passwords="{
            currentPassword,
            newPassword,
            confirmPassword
          }"
          @confirmed="confirmChange"
        />
      </v-card>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useProfileStore } from '@/stores/profile';
  import { useUserStore } from '@/stores/user';
  import PasswordConfirmation from './PasswordConfirmation.vue';

  
  const router = useRouter();
  const profileStore = useProfileStore();
  const userStore = useUserStore()
  
  const currentPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');
  const isFormValid = ref(false);
  const showConfirmDialog = ref(false);
  const showMessage = ref(false);
  const message = ref('');
  const messageType = ref('');
  
  const rules = {
    required: value => !!value || '필수 입력 항목입니다',
    min: v => v.length >= 8 || '비밀번호는 최소 8자 이상이어야 합니다'
  };
  
  const handleSubmit = () => {
    if (!isFormValid.value) return;
    
    if (newPassword.value !== confirmPassword.value) {
      message.value = '새 비밀번호가 일치하지 않습니다.';
      messageType.value = 'error';
      showMessage.value = true;
      return;
    }
  
    showConfirmDialog.value = true;
  };
  
  const goBack = () => {
    router.push('/profile');
  };
  
  const confirmChange = async () => {
    const result = await profileStore.changePassword(
      currentPassword.value,
      newPassword.value,
      confirmPassword.value
    );
  
    message.value = result.message;
    messageType.value = result.success ? 'success' : 'error';
    showMessage.value = true;
  
    if (result.success) {
      message.value = '비밀번호가 변경되었습니다. 다시 로그인해주세요.';
      await userStore.logOut()
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    }
  };
  
  </script>
  
  <style scoped>
.password-container {
  max-width: 600px;
  margin: 0 auto;
}

.message-container {
  margin: 1rem 0;  /* 위아래 여백 추가 */
  display: flex;
  justify-content: center;
}

.message-box {
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 500;
  width: 100%;  /* 너비를 100%로 변경 */
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

.v-form {
  margin-bottom: 1rem;
}

.v-btn {
  text-transform: none;
}
</style>