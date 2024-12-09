
<template>
  <v-container>
    <v-card class="mx-auto pa-8 pt-10 pb-4" elevation="4" max-width="448" rounded="lg">
      <v-form @submit.prevent="login">
        <div class="text-subtitle-1 text-medium-emphasis">Username</div>

        <v-text-field 
          v-model="username" 
          density="compact" 
          placeholder="아이디" 
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password
        </div>

        <v-text-field
          v-model="password"
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          density="compact"
          placeholder="비밀번호"
          prepend-inner-icon="mdi-lock-outline"
          variant="outlined"
          @click:append-inner="visible = !visible"
        ></v-text-field>

        <!-- 비밀번호 찾기 링크 추가 -->
        <div class="text-right mb-3">
          <router-link 
            to="/find_password"
            class="find-password-link"
          >
            비밀번호 찾기
          </router-link>
        </div>

        <v-btn 
          type="submit" 
          class="mb-8" 
          color="blue-darken-3" 
          size="large" 
          variant="tonal" 
          block
        >
          Log In
        </v-btn>
      </v-form>

      <v-card-text class="text-center">
        <router-link 
          to="/signup"
          class="text-blue-darken-3 text-decoration-none"
        >
          회원가입
          <v-icon icon="mdi-arrow-right"></v-icon>
        </router-link>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useUserStore()
const visible = ref(false)
const username = ref('')
const password = ref('')

const login = async () => {
  if (!username.value || !password.value) return

  const payload = {
    username: username.value,
    password: password.value
  }
  
  await store.logIn(payload)
}
</script>

<style scoped>
.find-password-link {
  font-size: 0.75rem;  /* 작은 폰트 사이즈 */
  color: #90CAF9;  /* 연한 하늘색 */
  text-decoration: underline;  /* 밑줄 */
  transition: color 0.2s ease;  /* 호버 효과를 위한 트랜지션 */
}

.find-password-link:hover {
  color: #64B5F6;  /* 호버시 약간 진한 하늘색 */
}
</style>