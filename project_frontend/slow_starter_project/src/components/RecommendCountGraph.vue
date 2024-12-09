<!-- RecommendCountGraph.vue -->
<template>
  <v-card class="graph-card">
    <v-card-title class="graph-header">
      <span class="graph-title">연령대별 상품 선호도</span>
      <v-btn-toggle
        v-model="localAgeGroup"
        mandatory
        class="age-toggle"
        rounded="lg"
        density="comfortable"
      >
        <v-btn 
          v-for="age in ['20', '30', '40', '50']" 
          :key="age" 
          :value="age"
          class="age-btn"
        >
          {{ age }}대
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text>
      <div class="chart-container">
        <template v-if="!hasData">
          <v-sheet class="no-data-sheet">
            <v-icon size="40" color="grey">mdi-chart-bar-off</v-icon>
            <span class="text-h6 mt-3 text-grey">데이터가 없습니다</span>
          </v-sheet>
        </template>
        <template v-else>
          <v-sheet class="chart-sheet">
            <v-row align="center" justify="center" class="chart-row">
              <v-col 
                v-for="(item, index) in chartData" 
                :key="index" 
                cols="4"
                class="chart-col"
              >
                <v-card 
                  :color="getBarColor(item.value)" 
                  class="chart-bar"
                  :style="`height: ${getBarHeight(item.value)}px`"
                >
                  <v-card-text class="bar-content">
                    <div class="bar-title">{{ item.title }}</div>
                    <div class="bar-value">{{ item.value }}회</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-sheet>
        </template>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRecommendStore } from '@/stores/recommend'

const store = useRecommendStore()
const localAgeGroup = ref('20')

// 로컬 상태가 변경될 때 store 업데이트
watch(localAgeGroup, (newValue) => {
  console.log('Age group changed:', newValue)  // 디버깅용
  store.changeAgeGroup(newValue)
})

// store의 selectedAgeGroup이 변경될 때 로컬 상태 업데이트
watch(() => store.selectedAgeGroup, (newValue) => {
  localAgeGroup.value = newValue
})

const chartData = computed(() => {
  const data = store.getCurrentAgeGroupData
  if (!data || data.length === 0) return []
  
  return data.map(item => ({
    value: item.userCount || 0,
    title: item.fin_prdt_nm || '상품명 없음',
  }))
})

const hasData = computed(() => {
  return chartData.value.length > 0
})

const getBarColor = (value) => {
  // 부드러운 하늘색 그라데이션으로 변경
  const base = 60; // 기본 밝기
  const intensity = Math.min(Math.floor((value / 10) * 30), 100);
  return `rgba(96, 165, 250, ${(base + intensity) / 100})`;
}

const getBarHeight = (value) => {
  const minHeight = 100;
  const maxHeight = 300;
  const height = (value / 10) * 50 + minHeight;
  return Math.min(height, maxHeight);
}


</script>

<style scoped>
.graph-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(255, 216, 184, 0.1) !important;
  margin-top: 2rem;
  background-color: #ffd8b8;
}

.graph-header {
  padding: 1.5rem 2rem !important;
  background-color: white;
  border-bottom: 1px solid rgba(255, 216, 184, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.graph-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333333;
}

.age-toggle {
  background-color: #fff0e6;
  border-radius: 8px;
  padding: 4px;
}

.age-btn {
  min-width: 60px !important;
  letter-spacing: 0.5px;
  color: #333333 !important;
}

.age-btn.v-btn--active {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

.chart-container {
  min-height: 400px;
  padding: 1.5rem;
  background-color: white;
}

.no-data-sheet {
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #fff0e6;
  border-radius: 12px;
}

.chart-sheet {
  padding: 1.5rem;
}

.chart-row {
  gap: 1rem;
}

.chart-col {
  display: flex;
  flex-direction: column;
}

.chart-bar {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  min-height: 100px;
}

.chart-bar:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(255, 216, 184, 0.2);
}

.bar-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
}

.bar-title {
  font-size: 0.875rem;
  color: #333333;
  text-align: center;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.bar-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333333;
  text-align: center;
  margin-top: auto;
}

@media (max-width: 960px) {
  .graph-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .chart-col {
    flex: 0 0 100%;
    max-width: 100%;
  }
  
  .bar-title {
    font-size: 0.8rem;
  }
  
  .bar-value {
    font-size: 1.25rem;
  }
}
</style>