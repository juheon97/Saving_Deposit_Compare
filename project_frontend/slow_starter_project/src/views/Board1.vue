<template>
  <div class="board-container">
    <div class="board-header">
      <div class="header-left">
        <router-link to="/boards" class="back-button">
          <span>←</span> 뒤로가기
        </router-link>
        <h1 class="board-title">일반 게시판</h1>
      </div>
      <RouterLink 
        :to="{ name: 'BoardCreateView', params: { boardType: 'board1' }}" 
        class="write-button"
      >
        게시글 작성하기
      </RouterLink>
    </div>
    
    <div class="board-list">
      <table class="board-table">
        <thead>
          <tr>
            <th width="10%"></th>
            <th width="40%">제목</th>
            <th width="15%">작성일</th>
            <th width="15%">수정일</th>
            <th width="10%">좋아요</th>
          </tr>
        </thead>
          
        <tbody>
          <tr v-for="board in store.boards" :key="board.id" class="board-row">
            <td></td>
            <td>
              <RouterLink 
                :to="{ name: 'BoardDetailView', params: { boardType: 'board1', id: board.id }}" 
                class="title-link"
              >
                {{ board.title }}
              </RouterLink>
            </td>
            <td>{{ formatDate(board.created_at) }}</td>
            <td>{{ formatDate(board.updated_at) }}</td>
            <td>
              <ReadOnlyLikeComponent
                :is-liked="board.is_liked"
                :like-count="board.like_count"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBoardStore } from '@/stores/board'
import { RouterLink } from 'vue-router'
import ReadOnlyLikeComponent from '@/components/ReadOnlyLikeComponent.vue'

const store = useBoardStore()

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  return `${year}.${month}.${day} ${hours}:${minutes}`;
}

onMounted(() => {
  store.getBoards('board1')
})
</script>

<style scoped>
.board-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #ffd8b8;
  min-height: 100vh;
}

.board-title {
  color: #333333;
  text-align: center;
  margin: 0;
  font-size: 1.8rem;
}

.board-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.2);
}

thead {
  background-color: #fff0e6;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ffe4d0;
}

th {
  font-weight: 600;
  color: #333333;
}

.board-row:hover {
  background-color: #fff5ee;
}

.title-link {
  text-decoration: none;
  color: #333333;
}

.title-link:hover {
  color: #666666;
}

.write-button {
  background-color: #fff0e6;
  color: #333333;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid #ffd8b8;
}

.write-button:hover {
  transform: translateY(-2px);
  background-color: #ffd8b8;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  background-color: #fff0e6;
  color: #333333;
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  border: 1px solid #ffd8b8;
  transition: all 0.2s ease;
}

.back-button:hover {
  background-color: #ffd8b8;
  transform: translateY(-2px);
}

.board-table {
  width: 100%;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.2);
}

.board-table thead {
  background-color: #fff0e6;
}

.board-table th {
  padding: 1rem;
  font-weight: 600;
  color: #333333;
  text-align: left;
}

.board-table td {
  padding: 1rem;
  border-bottom: 1px solid #ffe4d0;
  color: #333333;
}

.board-row:hover {
  background-color: #fff5ee;
}

.board-image {
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 1px 3px rgba(255, 216, 184, 0.2);
}

@media (max-width: 768px) {
  .board-container {
    padding: 1rem;
  }
  
  .board-header {
    flex-direction: column;
    gap: 1rem;
    display: grid;

    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .write-button {
    width: 100%;
    text-align: center;
  }
  
  .board-table {
    display: block;
    overflow-x: auto;
  }
}
</style>