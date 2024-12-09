<template>
  <v-card class="exchange-card">
    <img :src="`src/assets/flags/${exchangeData.id - 1}.png`" class="flag-image" />
    <v-card-title>{{ exchangeData.cur_nm }} ({{ exchangeData.cur_unit }})</v-card-title>
    <v-card-text>
      <div>받을때 {{ exchangeData.ttb }}원 | 보낼 때 {{ exchangeData.tts }}원</div>
    </v-card-text>
    <div class="rate-corner">매매가 : {{ exchangeData.deal_bas_r }}원</div>
    <v-btn 
      class="calculate-btn" 
      @click="openCalculator"
      variant="outlined"
      color="blue"
    >
      계산하기
    </v-btn>
  </v-card>
  <ExchangeCalculate 
    :dialog="showCalculator"
    @update:dialog="showCalculator = $event"
    :exchange-data="exchangeData"
  />
</template>

<script setup>


import { ref } from 'vue';
import ExchangeCalculate from '@/components/ExchangeCalculate.vue';

const props = defineProps({
  exchangeData: {
    type: Object,
    required: true
  }
})

const showCalculator = ref(false);

const openCalculator = () => {
  showCalculator.value = true;
};


</script>

<style scoped>
.exchange-card {
  position: relative;
  height: 100%;
  width: 100%;
  padding: 24px; /* 내부 패딩 추가 */
}

.flag-image {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 108px;  /* 1.8배 증가 */
  height: 90px;  /* 1.8배 증가 */
  object-fit: contain;
  border-radius: 8px;  /* 증가 */
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);  /* 그림자 효과 강화 */
}

.rate-corner {
  position: absolute;
  bottom: 20px;
  left: 20px;
  font-size: 2.7rem; /* 1.8배 증가 */
  font-weight: bold;
  color: #111111;
}

.calculate-btn {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background-color: white;
  font-size: 1.2rem;
  padding: 12px 24px;
  display: flex;  /* Flexbox 추가 */
  align-items: center;  /* 수직 중앙 정렬 */
  justify-content: center;  /* 수평 중앙 정렬 */
  min-width: 120px;  /* 최소 너비 설정 */
  height: 48px;  /* 높이 설정 */
}

/* v-btn 내부의 텍스트 정렬을 위한 추가 스타일 */
:deep(.v-btn__content) {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>