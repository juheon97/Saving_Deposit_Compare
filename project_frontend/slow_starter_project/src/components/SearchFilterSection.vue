<template>
  <v-card class="search-filter-card mb-4" style="border-radius: 3;">
    <v-card-text >
      <!-- 제목 추가 -->
      <h2 class="filter-title mb-4" style="padding:1">상품 검색</h2>

      <!-- 상품 유형 선택 탭 -->
      <div class="mb-6">
        <div class="filter-section-label mb-2" style="padding:1" >상품 유형</div>
        <v-tabs
          style="border-radius: 8%;"
          v-model="filterOptions.productType"
          class="product-type-tabs"
          color="primary"
          grow
        >
          <v-tab value="all" class="custom-tab">
            <v-icon icon="mdi-view-grid-outline" class="mr-2" />
            전체 상품
          </v-tab>
          <v-tab value="deposit" class="custom-tab">
            <v-icon icon="mdi-piggy-bank-outline" class="mr-2" />
            예금 상품
          </v-tab>
          <v-tab value="saving" class="custom-tab">
            <v-icon icon="mdi-cash-multiple" class="mr-2" />
            적금 상품
          </v-tab>
        </v-tabs>
      </div>

      <!-- 가입 방법 선택 -->
      <div class="join-ways-section">
        <div class="filter-section-label mb-3">가입 방법</div>
        <v-chip-group
          v-model="filterOptions.joinWays"
          multiple
          class="mt-2"
          column
        >
          <v-chip
            filter
            value="internet"
            class="custom-chip"
            variant="elevated"
          >
            <v-icon start icon="mdi-desktop-classic" class="mr-2" />
            인터넷 뱅킹
          </v-chip>
          <v-chip
            filter
            value="smart"
            class="custom-chip"
            variant="elevated"
          >
            <v-icon start icon="mdi-cellphone" class="mr-2" />
            모바일 뱅킹
          </v-chip>
          <v-chip
            filter
            value="store"
            class="custom-chip"
            variant="elevated"
          >
            <v-icon start icon="mdi-store" class="mr-2" />
            영업점 방문
          </v-chip>
        </v-chip-group>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['update-filters'])

const filterOptions = reactive({
  productType: 'all',
  joinWays: []
})

watch(() => filterOptions.productType, (newValue) => {
  emit('update-filters', {
    productType: newValue,
    joinWays: filterOptions.joinWays
  })
}, { deep: true })

watch(() => filterOptions.joinWays, (newValue) => {
  emit('update-filters', {
    productType: filterOptions.productType,
    joinWays: newValue
  })
}, { deep: true })
</script>

<style scoped>
.search-filter-card {
  background-color: #ffffff;
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.filter-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333333;
  margin-bottom: 1.5rem;
}

.filter-section-label {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333333;
  margin-bottom: 0.5rem;
}

.product-type-tabs {
  background-color: #fff5ee;
  border-radius: 12px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.1);
}

.custom-tab {
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0;
  border-radius: 8px !important;
  min-height: 48px;
  color: #333333;
}

.custom-tab:hover {
  background-color: #ffe4d0;
}

.join-ways-section {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.1);
}

.custom-chip {
  border-radius: 8%;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0 16px;
  height: 40px;
  margin-right: 12px;
  margin-bottom: 8px;
  border: 1px solid #ffd8b8;
  background-color: #ffffff !important;
  transition: all 0.2s ease;
  color: #333333;
}

.custom-chip:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 216, 184, 0.2);
  background-color: #fff5ee !important;
}

.custom-chip.v-chip--selected {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
  border-color: #ffd8b8;
}

:deep(.v-tab--selected) {
  background-color: #ffd8b8;
  color: #333333 !important;
}

:deep(.v-tabs .v-slide-group__content) {
  border: none;
}
</style>