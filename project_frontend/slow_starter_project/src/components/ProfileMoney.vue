<template>
  <v-card variant="outlined" class="mt-4">
    <v-card-title class="text-h6 bg-light-blue-lighten-5 py-3" style="padding:10px;">
      수익 계산기
    </v-card-title>
    <v-card-text>
      <v-row>
        <!-- Term Filters -->
        <v-col cols="12">
          <v-chip-group
            v-model="selectedTerm"
            selected-class="bg-primary"
          >
            <v-chip
              v-for="month in [36, 24, 12, 6, 3, 1]"
              :key="month"
              :value="month"
              filter
              variant="outlined"
            >
              {{ month }}개월
            </v-chip>
          </v-chip-group>
        </v-col>

        <!-- Rate Type Switch -->
        <v-col cols="12">
          <v-btn-toggle
            v-model="rateType"
            mandatory
            rounded="lg"
          >
            <v-btn value="basic" size="small">기본금리</v-btn>
            <v-btn value="special" size="small">우대금리</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <!-- 예금 계산 -->
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">
              예금 수익 계산
            </v-card-title>
            <v-list density="compact">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-cash</v-icon>
                </template>
                <v-list-item-title>원금</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ formatMoney(profileStore.user_info.balance_deposit) }}원
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-chart-line</v-icon>
                </template>
                <v-list-item-title>총 수익</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ calculateDepositTotal }}원
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="info">mdi-calendar-month</v-icon>
                </template>
                <v-list-item-title>월 이자</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ calculateDepositMonthly }}원
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <!-- 적금 계산 -->
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">
              적금 수익 계산
            </v-card-title>
            <v-list density="compact">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-cash-multiple</v-icon>
                </template>
                <v-list-item-title>월 납입금</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ formatMoney(profileStore.user_info.balance_saving) }}원
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-chart-line</v-icon>
                </template>
                <v-list-item-title>총 수익</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ calculateSavingTotal }}원
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="info">mdi-calendar-month</v-icon>
                </template>
                <v-list-item-title>월 이자</v-list-item-title>
                <v-list-item-subtitle class="text-right">
                  {{ calculateSavingMonthly }}원
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useProfileStore } from '@/stores/profile';

const profileStore = useProfileStore();
const selectedTerm = ref(12);
const rateType = ref('basic');

const formatMoney = (amount) => {
  return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

const getSelectedRate = (type, rateType) => {
  const options = type === 'deposit' ? 
    profileStore.selectedRates.deposit : 
    profileStore.selectedRates.saving;
    
  if (!options) return 0;
  
  const option = options.find(opt => opt.save_trm === selectedTerm.value);
  return option ? option[rateType] : 0;
};

const calculateDepositTotal = computed(() => {
  const principal = profileStore.user_info.balance_deposit;
  const rate = rateType.value === 'basic' ? 
    getSelectedRate('deposit', 'intr_rate') : 
    getSelectedRate('deposit', 'intr_rate2');
  
  const interest = principal * (rate / 100) * (selectedTerm.value / 12);
  return formatMoney(Math.round(interest));
});

const calculateDepositMonthly = computed(() => {
  const total = parseFloat(calculateDepositTotal.value.replace(/,/g, ''));
  return formatMoney(Math.round(total / selectedTerm.value));
});

const calculateSavingTotal = computed(() => {
  const monthlyDeposit = profileStore.user_info.balance_saving;
  const rate = rateType.value === 'basic' ? 
    getSelectedRate('saving', 'intr_rate') : 
    getSelectedRate('saving', 'intr_rate2');
  
  let total = 0;
  for (let i = 0; i < selectedTerm.value; i++) {
    const monthsRemaining = selectedTerm.value - i;
    total += monthlyDeposit * (rate / 100) * (monthsRemaining / 12);
  }
  return formatMoney(Math.round(total));
});

const calculateSavingMonthly = computed(() => {
  const total = parseFloat(calculateSavingTotal.value.replace(/,/g, ''));
  return formatMoney(Math.round(total / selectedTerm.value));
});
</script>

<style scoped>
/* 카드 전체 스타일 */
:deep(.v-card) {
  background-color: white !important;
}

/* 카드 제목 */
:deep(.bg-light-blue-lighten-5) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

/* 텍스트 색상 */
:deep(.text-h6),
:deep(.text-subtitle-1),
:deep(.v-list-item-title),
:deep(.v-list-item-subtitle) {
  color: #333333 !important;
}

/* 칩 그룹 스타일 */
:deep(.v-chip) {
  border-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-chip--selected) {
  background-color: #ffd8b8 !important;
  color: #fff5ee !important;
}

:deep(.v-chip:hover) {
  background-color: #fff0e6 !important;
}

/* 버튼 토글 스타일 */
:deep(.v-btn-toggle) {
  background-color: #fff0e6 !important;
  border-color: #ffd8b8 !important;
}

:deep(.v-btn) {
  color: #333333 !important;
}

:deep(.v-btn--active) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn:hover) {
  background-color: #fff5ee !important;
}

/* 아이콘 색상 */
:deep(.v-icon.text-primary),
:deep(.v-icon.text-success),
:deep(.v-icon.text-info) {
  color: #333333 !important;
}

/* 서브카드 스타일 */
:deep(.v-card.v-card--variant-outlined) {
  border-color: #ffd8b8 !important;
}

:deep(.v-card.v-card--variant-outlined:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 216, 184, 0.2);
}

/* 리스트 아이템 호버 효과 */
:deep(.v-list-item:hover) {
  background-color: #fff5ee !important;
}

/* 금액 텍스트 정렬 */
:deep(.text-right) {
  color: #333333 !important;
  font-weight: 500;
}

.bg-primary {
  background-color: #fff5ee !important;
}

</style>