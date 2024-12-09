<template>
  <div class="board-container">
    <div class="board-header">
      <h1 class="board-title">우리들의 이야기를 담는 곳</h1>
      <RouterLink :to="{ name: 'BoardCreateView' }" class="write-button">게시글 작성하기</RouterLink>
    </div>
    <div class="board-list">
      <BoardListComponent />
    </div>
  </div>
</template>

<script setup>
import BoardListComponent from '@/components/BoardListComponent.vue'
import { onMounted } from 'vue'
import { useBoardStore } from '@/stores/board'
import { RouterLink } from 'vue-router'

const store = useBoardStore()

onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getBoards()
})
</script>

<style scoped>
h1 {
  color: #0564A8;
}

.board-header {
 display: flex !important;
 justify-content: space-between ;
 align-items: center ;
 margin-bottom: 2rem;
 padding: 0 1rem ;
}

/* 게시글 목록 컨테이너 */
.board-list {
  display: grid !important;
  grid-template-columns: 1fr !important; 
  gap: 1rem !important;
  padding: 1rem !important;
  width: 100% !important; /* 전체 너비 사용 */
}

/* 각 게시글 카드 스타일 */
.board-item-container {
  width: calc(50% - 1rem) !important; /* 화면의 절반에서 gap의 절반을 뺀 크기 */
  min-width: 450px !important; /* 최소 너비 설정 */
  background: white !important;
  padding: 2rem !important;
  border-radius: 12px !important;
  border: 1px solid #e0e0e0 !important;
  transition: all 0.3s ease !important;
  height: 200px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
  margin-bottom: 2rem !important;
}

/* 호버 효과 */
.board-item-container:hover {
 transform: translateY(-5px) scale(1.02) !important; /* 위로 뜨면서 살짝 커지는 효과 */
 box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1) !important;
 background: linear-gradient(135deg, #e3f2ff 0%, #d6ebff 100%) !important; /* 호버 시 더 진한 그라데이션 */
}

/* 클릭 효과 */
.board-item-container:active {
 transform: translateY(0) scale(0.98) !important; /* 눌리는 효과 */
 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
}

.write-button:hover {
 transform: translateY(-2px) !important;
 box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
 background: linear-gradient(135deg, #e3f2ff 0%, #d6ebff 100%) !important;
}


.board-container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 2rem !important;
}

.write-button {
  background-color:#e7f0ff;
  color: #666 !important;
  padding: 0.7rem 1.5rem !important;
  border-radius: 8px !important;
  border: 1rem !important;
  transition: all 0.3s ease !important;
  font-weight: 500 !important;
  box-shadow: 0 2px 4px rgba(74, 144, 226, 0.2) !important;
}


</style>