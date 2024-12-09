<template>
  <div class="search-view-wrapper">
    <div class="search-container">
      <SearchContainer />
    </div>
  </div>
</template>

<script setup>
import SearchContainer from "@/components/SearchContainer.vue";
</script>

<style scoped>
.search-view-wrapper {
  min-height: 100vh;
  width: 100%;
  background-color: #ffd8b8;
  padding: 2rem 1rem;
}

.search-container {
  max-width: 1800px;
  margin: 0 auto;
  background-color: #ffead8;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

/* 반응형 디자인을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .search-view-wrapper {
    padding: 1rem 0.5rem;
  }
  
  .search-container {
    padding: 1rem;
  }
}
</style>