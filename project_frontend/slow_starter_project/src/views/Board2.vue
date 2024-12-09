<template>
  <div class="board-container">
    <div class="board-header">
      <div class="header-left">
        <router-link to="/boards" class="back-button">
          <span>←</span> 뒤로가기
        </router-link>
        <h1 class="board-title">챌린지1</h1>
      </div>
      <RouterLink 
        :to="{ name: 'BoardCreateView', params: { boardType: 'board2' }}" 
        class="write-button"
      >
        게시글 작성하기
      </RouterLink>
    </div>
    
    <div class="card-grid">
      <div v-for="board in store.boards" :key="board.id" class="card">
        <RouterLink 
          :to="{ name: 'BoardDetailView', params: { boardType: 'board2', id: board.id }}" 
          class="card-link"
        >
          <div class="card-image">
            <img v-if="board.image" :src="getImageUrl(board.image)" :alt="board.title">
            <div v-else class="no-image">No Image</div>
          </div>
          <div class="card-content">
            <h2 class="card-title">{{ board.title }}</h2>
            <p class="card-text">{{ truncateContent(board.content) }}</p>
          </div>
          <div class="card-footer">
            <div class="card-meta">
              <div class="dates">
                <span>작성일: {{ formatDate(board.created_at) }}</span>
                <span v-if="board.updated_at !== board.created_at">
                  수정일: {{ formatDate(board.updated_at) }}
                </span>
              </div>
              <ReadOnlyLikeComponent
                :is-liked="board.is_liked"
                :like-count="board.like_count"
              />
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBoardStore } from '@/stores/board'
import { RouterLink } from 'vue-router'
import ReadOnlyLikeComponent from '@/components/ReadOnlyLikeComponent.vue'

const store = useBoardStore()

const getImageUrl = (imageUrl) => {
  if (imageUrl && !imageUrl.startsWith('http')) {
    return `${store.API_URL}${imageUrl}`
  }
  return imageUrl
}

const truncateContent = (content) => {
  return content?.length > 50 ? content.substring(0, 50) + '...' : content
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  
  return `${year}.${month}.${day}`;
}

onMounted(() => {
  store.getBoards('board2')
})
</script>

<style scoped>
.board-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #ffd8b8;
  min-height: 100vh;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
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

.board-title {
  color: #333333;
  margin: 0;
  font-size: 1.8rem;
}

.write-button {
  background-color: #fff0e6;
  color: #333333;
  border: 1px solid #ffd8b8;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.write-button:hover {
  background-color: #ffd8b8;
  transform: translateY(-2px);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  padding: 1rem 0;
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.2);
  transition: transform 0.3s ease;
  height: 100%;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(255, 216, 184, 0.3);
}

.card-image {
  height: 200px;
  overflow: hidden;
  background-color: #fff5ee;
}

.no-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333333;
  background-color: #fff5ee;
}

.card-content {
  padding: 1rem;
  flex-grow: 1;
}

.card-title {
  font-size: 1.2rem;
  color: #333333;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.card-text {
  color: #333333;
  font-size: 0.9rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  padding: 1rem;
  border-top: 1px solid #ffe4d0;
  background-color: #fff5ee;
}

.dates {
  font-size: 0.9rem;
  color: #333333;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 1400px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .board-container {
    padding: 1rem;
  }
  
  .board-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .write-button {
    width: 100%;
    text-align: center;
  }
  
  .card-grid {
    grid-template-columns: 1fr;
  }
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

.board-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
</style>