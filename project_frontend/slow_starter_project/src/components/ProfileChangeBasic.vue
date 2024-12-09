<template>
  <v-dialog
    :model-value="isOpen"
    @update:model-value="$emit('close')"
    width="600px"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5 pa-4">
        기본 정보 수정
        <v-spacer></v-spacer>
        <v-btn icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.first_name"
                  :placeholder="profileStore.user_info.first_name"
                  label="이름"
                  variant="outlined"
                  prepend-inner-icon="mdi-account"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.email"
                  :placeholder="profileStore.user_info.email"
                  label="이메일"
                  variant="outlined"
                  prepend-inner-icon="mdi-email"
                  type="email"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-select
                  v-model="formData.gender"
                  :items="[
                    { title: '남성', value: 'M' },
                    { title: '여성', value: 'F' }
                  ]"
                  label="성별"
                  variant="outlined"
                  prepend-inner-icon="mdi-gender-male-female"
                  item-title="title"
                  item-value="value"
                ></v-select>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.age"
                  :placeholder="String(profileStore.user_info.age)"
                  label="나이"
                  variant="outlined"
                  prepend-inner-icon="mdi-calendar"
                  type="number"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.balance_deposit"
                  :placeholder="String(profileStore.user_info.balance_deposit)"
                  label="예금 금액"
                  variant="outlined"
                  prepend-inner-icon="mdi-bank"
                  type="number"
                  :min="10000000"
                  :max="1000000000"
                  :step="10000"
                  :hint="'최소 1000만원, 최대 10억원'"
                  persistent-hint
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="formData.balance_saving"
                  :placeholder="String(profileStore.user_info.balance_saving)"
                  label="적금 월 납입금액"
                  variant="outlined"
                  prepend-inner-icon="mdi-piggy-bank"
                  type="number"
                  :min="100000"
                  :max="1000000"
                  :step="10000"
                  :hint="'최소 10만원, 최대 100만원'"
                  persistent-hint
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="outlined"
          @click="$emit('close')"
        >
          취소
        </v-btn>
        <v-btn
          color="primary"
          class="ml-2"
          @click="handleSubmit"
        >
          수정
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { useProfileStore } from "@/stores/profile";

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close']);
const profileStore = useProfileStore();

const formData = ref({
  first_name: "",
  email: "",
  gender: "",
  age: "",
  balance_deposit: "",
  balance_saving: ""
});

const handleSubmit = async () => {
  await profileStore.updateBasicInfo(formData.value);
  emit('close');
};
</script>

<style scoped>
.v-dialog > .v-card {
  border-radius: 8px;
  background-color: white;
}

/* 카드 제목 스타일 */
:deep(.v-card-title) {
  background-color: #ffd8b8;
  color: #333333;
}

/* 텍스트 필드 스타일 */
:deep(.v-field__input) {
  color: #333333 !important;
}

:deep(.v-label) {
  color: #333333 !important;
}

:deep(.v-field__outline) {
  color: #ffd8b8 !important;
}

:deep(.v-field--focused .v-field__outline) {
  color: #ffd8b8 !important;
}

:deep(.v-field__prepend-inner .v-icon) {
  color: #333333 !important;
}

/* 힌트 텍스트 스타일 */
:deep(.v-field__hint) {
  color: #666666 !important;
}

/* 셀렉트 필드 스타일 */
:deep(.v-select .v-field) {
  color: #333333 !important;
}

:deep(.v-select__selection) {
  color: #333333 !important;
}

/* 버튼 스타일 */
:deep(.v-btn.v-btn--variant-outlined) {
  border-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn.v-btn--variant-outlined.error) {
  border-color: #ef5350 !important;
  color: #ef5350 !important;
}

:deep(.v-btn.text-primary) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn:not(.error):hover) {
  background-color: #fff0e6 !important;
}

/* 닫기 아이콘 버튼 */
:deep(.v-btn--icon) {
  color: #333333 !important;
}

/* 폼 전체 텍스트 색상 */
:deep(.v-card-text) {
  color: #333333 !important;
}

/* 포커스 상태의 필드 스타일 */
:deep(.v-field--focused) {
  background-color: #fff5ee !important;
}

/* 호버 상태의 필드 스타일 */
:deep(.v-field:hover) {
  background-color: #fff5ee !important;
}

/* 셀렉트 메뉴 스타일 */
:deep(.v-select__content) {
  background-color: white !important;
}

:deep(.v-list-item) {
  color: #333333 !important;
}

:deep(.v-list-item--active) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-list-item:hover) {
  background-color: #fff0e6 !important;
}
</style>