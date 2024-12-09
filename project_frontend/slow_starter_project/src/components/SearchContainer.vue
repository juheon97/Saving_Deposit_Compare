<template>
  <div>
    <SearchFilterSection
      @update-filters="handleFilterUpdate"
    />


    <SearchItemResult
      :results="filteredResults"
      :loading="loading"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useSearchStore } from '@/stores/search';
import SearchFilterSection from './SearchFilterSection.vue';
import SearchItemResult from './SearchItemResult.vue';

const searchStore = useSearchStore();
const loading = ref(false);
const currentFilters = ref({
  productType: 'all',
  joinWays: []
});

// 필터링된 결과 계산
// SearchContainer.vue의 filteredResults computed 부분 수정

const filteredResults = computed(() => {
  let results = [];
  
  // 상품 타입에 따른 필터링
  if (currentFilters.value.productType === 'all' || currentFilters.value.productType === 'deposit') {
    results.push(...searchStore.depositProducts.map(product => ({
      ...product,
      Deposit_code: 1
    })));
  }
  
  if (currentFilters.value.productType === 'all' || currentFilters.value.productType === 'saving') {
    results.push(...searchStore.savingProducts.map(product => ({
      ...product,
      Deposit_code: 2
    })));
  }

  // 가입방법 필터링
  if (currentFilters.value.joinWays?.length > 0) {
    results = results.filter(product => {
      return currentFilters.value.joinWays.some(way => {
        switch(way) {
          case 'internet':
            return product.join_way_internet;
          case 'smart':
            return product.join_way_smart;
          case 'store':
            return product.join_way_store;
          default:
            return false;
        }
      });
    });
  }

  return results;
});

// 필터 업데이트 핸들러
const handleFilterUpdate = (newFilters) => {
  currentFilters.value = { ...newFilters };
};

// 검색 실행
const handleSearch = async () => {
  loading.value = true;
  try {
    if (searchStore.depositProducts.length === 0 && searchStore.savingProducts.length === 0) {
      await Promise.all([
        searchStore.get_deposit_products_info(),
        searchStore.get_saving_products_info()
      ]);
    }
  } catch (error) {
    console.error('검색 중 오류 발생:', error);
    alert('검색 중 오류가 발생했습니다.');
  } finally {
    loading.value = false;
  }
};

// 초기 데이터 로드
handleSearch();
</script>