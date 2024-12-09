<template>
    <v-dialog 
      :model-value="dialog" 
      @update:model-value="$emit('update:dialog', $event)"
      width="600"
    >
      <v-card class="calculator-modal">
        <v-card-title class="text-center pb-2">
          환률 계산기
        </v-card-title>
        
        <v-card-text>
          <div class="calculator-content">
            <!-- 입력 통화 -->
            <div class="currency-box">
              <div class="currency-info">
                <img :src="`/src/assets/flags/${exchangeData.id - 1}.png`" class="currency-flag" />
                <div class="currency-details">
                  <div class="country-name">{{ exchangeData.cur_nm }}</div>
                  <div class="currency-code">{{ exchangeData.cur_unit }}</div>
                </div>
              </div>
              <v-text-field
                v-model="inputAmount"
                type="number"
                variant="outlined"
                density="compact"
                placeholder="입력하세요"
                hide-details
                hide-spin-buttons
              />
            </div>
  
            <div class="equals-sign">=</div>
  
            <!-- 결과 통화 -->
            <div class="currency-box ">
              <div class="currency-info">
                <img src="/src/assets/flags/south_korea.png" class="currency-flag" />
                <div class="currency-details">
                  <div class="country-name">대한민국</div>
                  <div class="currency-code">KRW</div>
                </div>
              </div>
              <div class="result-field">
                {{ calculatedResult }} 원
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </template>
   
   <script setup>
   import { ref, computed, watch } from 'vue';
   
   const props = defineProps({
    exchangeData: {
      type: Object,
      required: true
    },
    dialog: {
      type: Boolean,
      required: true
    }
   });
   
   const emit = defineEmits(['update:dialog']);
   
   const inputAmount = ref('');
   
   // 계산 로직
   const calculatedResult = computed(() => {
    if (!inputAmount.value) return '0';
    // 쉼표 제거 후 계산
    const rate = Number(props.exchangeData.deal_bas_r.replace(/,/g, ''));
    return new Intl.NumberFormat('ko-KR').format(rate * Number(inputAmount.value));
   });
   
   // dialog가 닫힐 때 입력값 초기화
   watch(() => props.dialog, (newVal) => {
    if (!newVal) {
      inputAmount.value = '';
    }
   });
   </script>
   
   <style scoped>
   .calculator-modal {
  padding: 30px;
  background-color: #ffd8b8;
}

.calculator-content {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.currency-box {
  border: 1px solid #ffe4d0;
  border-radius: 12px;
  padding: 18px;
  background: white;
}

.currency-info {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 12px;
}

.currency-flag {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
}

.currency-details {
  display: flex;
  flex-direction: column;
}

.country-name {
  font-size: 21px;
  color: #333333;
  font-weight: 500;
}

.currency-code {
  font-size: 18px;
  color: #333333;
}

.equals-sign {
  font-size: 36px;
  font-weight: bold;
  color: #333333;
  text-align: center;
  margin: 7px 0;
}

.result-field {
  font-size: 24px;
  color: #333333;
  padding: 12px;
  background: #fff5ee;
  border-radius: 6px;
  text-align: right;
}

:deep(.v-text-field input) {
  text-align: right;
  font-size: 24px !important;
  color: #333333;
}

:deep(.v-text-field) {
  margin-top: 6px;
  background-color: #fff5ee;
}

:deep(.v-card-title) {
  font-size: 27px !important;
  padding: 15px 0;
  color: #333333;
}

:deep(.v-field__overlay) {
  background-color: #fff5ee !important;
}

:deep(.v-field__outline) {
  --v-field-border-color: #ffe4d0 !important;
}
   </style>