<template>
    <v-dialog v-model="dialog" width="800" transition="fade-transition">
      <v-card class="country-list-modal">
        <v-card-title class="text-center pb-2">
          환율 정보 국가 목록
        </v-card-title>
        <v-card-text>
          <div class="country-grid">
            <div 
              v-for="country in countries" 
              :key="country.cur_unit"
              class="country-item"
              @click="selectCountry(country)"
            >
              <img :src="`src/assets/flags/${country.id - 1}.png`" class="country-flag" />
              <span class="country-name">{{ country.cur_nm }}</span>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useExchangeStore } from "@/stores/exchange";
  
  const store = useExchangeStore();
  const dialog = ref(false);
  
  const countries = computed(() => {
    return store.exchange_info.filter(item => item.cur_unit !== 'KRW');
  });
  
  const emit = defineEmits(['countrySelected']);
  
  const selectCountry = (country) => {
    emit('countrySelected', country);
    dialog.value = false;
  };
  
  // 다이얼로그 표시 메서드
  const showDialog = () => {
    dialog.value = true;
  };
  
  defineExpose({ showDialog });
  </script>
  
  <style scoped>
  .country-list-modal {
    padding: 20px;
    max-height: 80vh;
    overflow-y: auto;
  }
  
  .country-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    padding: 16px;
  }
  
  .country-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .country-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    background-color: #f5f5f5;
  }
  
  .country-flag {
    width: 48px;
    height: 48px;
    object-fit: cover;
    border-radius: 50%;
    margin-bottom: 8px;
  }
  
  .country-name {
    font-size: 14px;
    text-align: center;
    color: #333;
  }
  
  /* 페이드 트랜지션 */
  .fade-transition-enter-active,
  .fade-transition-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .fade-transition-enter-from,
  .fade-transition-leave-to {
    opacity: 0;
  }
  </style>