<template>
  <v-sheet class="mx-auto" width="80%" elevation="4" height="auto" rounded>
    <v-container class="mt-5 px-0 pb-0 pt-10">
      <v-form class="my-0 px-2" @submit.prevent="signUp">
        <v-row>
          <!-- 아이디 입력 -->
          <v-col cols="6">
            <v-text-field
              class="ms-5"
              hint="사용하실 아이디를 입력해주세요"
              label="Username*"
              variant="outlined"
              v-model="username"
              :error-messages="v$.username.$errors.map(e => e.$message)"
            ></v-text-field>
          </v-col>

          <!-- 이메일 입력 -->
          <v-col cols="12" class="d-flex">
    <v-text-field
      class="ms-5"
      hint="이메일은 ***.com의 형태로 입력해주세요"
      label="Email*"
      variant="outlined"
      v-model="emailPrefix"
      @blur="updateEmail"
    ></v-text-field>
    <span class="mt-4 mx-2">@</span>
    <v-text-field
      variant="outlined"
      v-model="emailCustomDomain"
      :disabled="emailDomain !== '직접 입력하기'"
      @input="handleCustomDomain"
      placeholder="직접 입력"
    ></v-text-field>
    <v-select
      :items="emailDomains"
      v-model="emailDomain"
      variant="outlined"
      @change="updateEmail"
    ></v-select>
  </v-col>

          <!-- 비밀번호 입력 -->
          <v-col cols="6">
            <v-text-field
              class="ms-5"
              hint="비밀번호는 10자 이상으로 설정해주세요"
              label="Password*"
              variant="outlined"
              type="password"
              v-model="password1"
              :error-messages="v$.password1.$errors.map(e => e.$message)"
            ></v-text-field>
          </v-col>

          <!-- 비밀번호 확인 -->
          <v-col cols="6">
            <v-text-field
              hint="비밀번호를 한 번 더 입력해주세요"
              class="me-5"
              label="Check Password*"
              variant="outlined"
              type="password"
              v-model="password2"
              :error-messages="v$.password2.$errors.map(e => e.$message)"
            ></v-text-field>
          </v-col>

          <!-- 이름 입력 -->
          <v-col cols="6">
            <v-text-field
              class="ms-5"
              hint="성함을 입력해주세요"
              label="이름*"
              variant="outlined"
              v-model="first_name"
              :error-messages="v$.first_name.$errors.map(e => e.$message)"
            ></v-text-field>
          </v-col>

          <!-- 성별 선택 -->
          <v-col cols="6">
            <v-radio-group
              class="ms-5"
              label="Gender*"
              v-model="gender"
              inline
            >
              <v-radio label="남성" value="M" color="primary"></v-radio>
              <v-radio label="여성" value="F" color="primary"></v-radio>
            </v-radio-group>
          </v-col>

          <!-- 나이 입력 -->
          <v-col cols="6">
            <v-text-field
              class="ms-5"
              hint="만 나이를 입력해주세요"
              label="Age*"
              variant="outlined"
              type="number"
              v-model="age"
              :error-messages="v$.age.$errors.map(e => e.$message)"
            ></v-text-field>
          </v-col>

          <!-- 약관 동의 체크박스 -->
          <!-- <v-col class="py-0" cols="6">
            <v-checkbox 
              class="mx-10" 
              color="#F9A825" 
              label="(필수) 서비스 이용약관 동의" 
              v-model="selected"
              value="service"
            ></v-checkbox>
          </v-col>

          <v-col class="py-0" cols="6">
            <v-checkbox 
              class="mx-10" 
              color="#F9A825" 
              label="(필수) 개인정보 처리 동의" 
              v-model="selected"
              value="info"
            ></v-checkbox>
          </v-col> -->
        </v-row>

        <!-- 가입하기 버튼 -->
        <v-row justify="center">
          <v-col cols="auto">
            <v-btn class="mb-5 button-custom" type="submit">가입하기</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
  </v-sheet>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, maxLength, minValue, maxValue, sameAs } from '@vuelidate/validators'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useUserStore()

// 폼 데이터
const username = ref('')
const emailPrefix = ref('')
const emailDomain = ref('직접 입력하기')
const emailCustomDomain = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')
const first_name = ref('')
const gender = ref('M')
const age = ref('')
// const selected = ref([])

const emailDomains = ['직접 입력하기', 'naver.com', 'gmail.com', 'kakao.com']

// 유효성 검사 규칙
const rules = {
  username: { required, maxLength: maxLength(20) },
  password1: { required, minLength: minLength(10) },
  password2: { required, sameAs: sameAs(password1) },
  first_name: { required },
  gender: { required },
  age: { 
    required, 
    minValue: minValue(1), 
    maxValue: maxValue(130) 
  },

}


const v$ = useVuelidate(rules, {
  username,
  password1,
  password2,
  first_name,
  gender,
  age,

})

const updateEmail = () => {
  let domain = emailDomain.value
  if (emailDomain.value === '직접 입력하기') {
    domain = emailCustomDomain.value
  }
  email.value = emailPrefix.value + '@' + domain
}

const handleCustomDomain = (event) => {
  const cursorPosition = event.target.selectionStart
  const value = emailCustomDomain.value

  if (value && !value.includes('.')) {
    emailCustomDomain.value = value + '.com'
    // 다음 tick에서 커서 위치 복원
    nextTick(() => {
      event.target.setSelectionRange(cursorPosition, cursorPosition)
    })
  }
  updateEmail()
}
const signUp = async () => {
  // 약관 동의 확인 추가
  // if (!selected.value.includes('service') || !selected.value.includes('info')) {
  //   alert('필수 약관에 모두 동의해주세요.')
  //   return
  // }
  
  const result = await v$.value.$validate()
  if (!result) return
  // const formattedDate = new Date(target_date.value).toISOString().split('T')[0]

  try {
    const payload = {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
      first_name: first_name.value,
      gender: gender.value,
      age: parseInt(age.value),
    }

    await store.signUp(payload)
    router.push('/')
  } catch (error) {
    console.error('회원가입 실패:', error)
    alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
  }
}
</script>

<style scoped>
.button-custom {
  background-color: #046FD9;
  color: #D3E8FF;
}
</style>