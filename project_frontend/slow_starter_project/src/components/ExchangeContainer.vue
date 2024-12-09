<template>
  <div class="page-background">
    <v-container class="carousel-container">
      <v-btn class="list-view-btn" @click="showCountryList" variant="outlined" color="white">전체 리스트 보기</v-btn>
      <v-carousel show-arrows="hover" hide-delimiters v-if="store.exchange_info.length > 0" :height="450">
        <v-carousel-item v-for="(group, i) in groupedExchangeData" :key="i">
          <ExchangeCardList :card-group="group" />
        </v-carousel-item>
      </v-carousel>
      <ExchangeCountryList ref="countryListRef" @country-selected="handleCountrySelect" />

      <ExchangeCalculate v-if="selectedExchangeData" :dialog="showCalculator" @update:dialog="showCalculator = $event" :exchange-data="selectedExchangeData" />
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"; // ref 추가
import { useExchangeStore } from "@/stores/exchange";
import ExchangeCardList from "./ExchangeCardList.vue";
import ExchangeCountryList from "@/components/ExchangeCountryList.vue";
import ExchangeCalculate from "@/components/ExchangeCalculate.vue";

const store = useExchangeStore();
const countryListRef = ref(null); // 추가
const showCalculator = ref(false); // 추가
const selectedExchangeData = ref(null); // 추가

const groupedExchangeData = computed(() => {
  const filteredData = store.exchange_info.filter((item) => item.cur_unit !== "KRW");

  const groups = [];

  for (let i = 0; i < filteredData.length; i += 4) {
    groups.push(filteredData.slice(i, i + 4));
  }

  return groups;
});

onMounted(() => {
  store.get_exchange_info();
});

const showCountryList = () => {
  countryListRef.value?.showDialog();
};

const handleCountrySelect = (country) => {
  selectedExchangeData.value = country;
  showCalculator.value = true;
};
</script>

<style scoped>
.page-background {
  background-color: #ffd8b8;
  min-height: 100vh;
  padding: 20px 0;
}

.carousel-container {
  margin: 10px;
  position: relative;
  max-width: 1800px;
  padding: 32px 60px;
  background-color: #fff0e6;  /* 연한 주황색으로 변경 */
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 216, 184, 0.2);
}

.v-carousel {
  height: 810px !important;
}

@media (max-width: 960px) {
  .v-carousel {
    height: 1440px !important;
  }
  .carousel-container {
    padding: 24px 32px;
  }
}

@media (max-width: 600px) {
  .v-carousel {
    height: 1800px !important;
  }
}

.list-view-btn {
  border-radius: 10%;
  position: absolute;
  top: 15px;
  right: 130px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  height: 48px;
  font-size: 1.2rem;
  background-color: #ffd8b8;
  border-color: #ffe3cd !important;
  color: #333333 !important;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.2);
}

.list-view-btn:hover {
  background-color: #ffe4d0 !important;
  border-color: #ffe4d0 !important;
}
</style>
