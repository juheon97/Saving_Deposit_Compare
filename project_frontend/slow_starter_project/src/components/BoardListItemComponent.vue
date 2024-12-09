<template>
  <div class="board-item-container">
    <h5 class="board-id">{{ board.id }}</h5>
    <p class="board-title">{{ board.title }}</p>
    <p class="board-content">{{ board.content }}</p>
    <RouterLink 
      :to="{ name: 'BoardDetailView', params: { id: board.id } }"  
      class="detail-link"
    >
      글 읽으러 가기~🌟
    </RouterLink>
    <hr class="divider">
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  board: Object
})
</script>

<style scoped>
.board-item-container {
 background-color: #fff1e6 !important;  /* #ffd8b8와 비슷한 매우 연한 색상 */
 padding: 1.5rem !important;
 border-radius: 8px !important;
 margin-bottom: 1rem !important;
 cursor: pointer !important;
 transition: all 0.2s ease !important;
 border: 1px solid #ffe4d3 !important;
}

.board-item-container:hover {
 background-color: #ffe4d3 !important;  /* 호버 시 조금 더 진한 색상 */
 transform: translateY(-2px) !important;
 box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

.board-item-container:active {
 background-color: #ffd8b8 !important;  /* 클릭 시 더 진한 색상 */
 transform: translateY(0) !important;
}

.board-id {
  color: #444;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.board-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #222;
  margin-bottom: 0.5rem;
}

.board-content {
  color: #444;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.detail-link {
  display: inline-block;
  color: #ff9f66;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: 1px solid #ff9f66;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.detail-link:hover {
  background-color: #ff9f66;
  color: white;
}

.divider {
  margin: 1.5rem 0;
  border: none;
  border-top: 1px solid #ffe4d3;
}
</style>