<template>
  <v-container fluid class="recommend-container">
    <v-card class="recommend-card">
      <v-card-title class="card-header">
        <span class="title-text">연령대별 추천 상품</span>
        <v-btn-toggle
          v-model="localSelectedType"
          mandatory
          class="toggle-buttons"
          rounded="lg"
          density="comfortable"
        >
          <v-btn value="deposit" class="toggle-btn">예금</v-btn>
          <v-btn value="saving" class="toggle-btn">적금</v-btn>
        </v-btn-toggle>
      </v-card-title>

      <v-container class="content-container">
        <v-row class="age-group-row">
          <v-col cols="6" v-for="age in ['20', '30', '40', '50']" :key="age">
            <v-card class="age-group-card">
              <RecommendItemList 
                :title="`${age}대 추천상품`" 
                :products="getProducts(age)"
              />
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <v-divider></v-divider>
      <RecommendCountGraph class="graph-section"/>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRecommendStore } from '@/stores/recommend'
import RecommendItemList from './RecommendItemList.vue'
import RecommendCountGraph from './RecommendCountGraph.vue'

const store = useRecommendStore()
const localSelectedType = ref('deposit')

// 로컬 상태가 변경될 때 store 업데이트
watch(localSelectedType, (newValue) => {
  // console.log('Selected type changed:', newValue)  // 디버깅용
  store.changeProductType(newValue)
})

// store의 selectedType이 변경될 때 로컬 상태 업데이트
watch(() => store.selectedType, (newValue) => {
  localSelectedType.value = newValue
})

const getProducts = (ageGroup) => {
  return store.getTopProductsByAge(ageGroup)
}

onMounted(() => {
  store.getProducts()
})
</script>

<style scoped>
.recommend-container {
  --primary-color: #ffd8b8;
  --primary-light: #ffe4d0;
  --primary-dark: #ffcca3;
  --bg-light: #fff5ee;
  --hover-color: #fff0e6;
  
  background-color: var(--primary-color);
  padding: 2rem;
  min-height: 100vh;
}

.recommend-card {
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(255, 216, 184, 0.1) !important;
}

.card-header {
  padding: 1.5rem 2rem !important;
  background-color: white;
  border-bottom: 1px solid rgba(255, 216, 184, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333333;
}

.toggle-buttons {
  background-color: var(--bg-light);
  border-radius: 8px;
  padding: 4px;
}

.toggle-btn {
  min-width: 80px !important;
  letter-spacing: 0.5px;
  color: #333333 !important;
}

.toggle-btn.v-btn--active {
  background-color: var(--primary-color) !important;
  color: #333333 !important;
}

.content-container {
  padding: 1.5rem;
  background-color: white;
}

.age-group-row {
  margin: 0 -12px;
}

.age-group-card {
  height: 100%;
  border-radius: 12px;
  background-color: white !important;
  transition: all 0.3s ease;
  padding: 1rem;
  border: 1px solid rgba(255, 216, 184, 0.1);
}

.age-group-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(255, 216, 184, 0.15) !important;
  border-color: var(--primary-light);
  background-color: var(--hover-color) !important;
}

.graph-section {
  padding: 1.5rem;
  background-color: white;
  border-top: 1px solid rgba(255, 216, 184, 0.2);
}

@media (max-width: 960px) {
  .recommend-container {
    padding: 1rem;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .age-group-row > .v-col {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>