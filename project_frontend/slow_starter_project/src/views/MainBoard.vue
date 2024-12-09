<template>
  <div class="board-container">
    <div class="board-header">
      <h1 class="board-title">🌟우리들의 이야기를 담은 곳🌟</h1>
    </div>
    <div class="board-links">
      <RouterLink to="/boards/board1" class="board-link">
        <div class="board-item-container">
          <h2>게시판</h2>
          <p>#일상 #질문 #나눔 ...</p>
        </div>
      </RouterLink>
      
      <RouterLink to="/boards/board2" class="board-link">
        <div class="board-item-container">
          <h2>저축 챌린지</h2>
          <p>#목돈만들기 #저축습관만들기...</p>
        </div>
      </RouterLink>
      
      <RouterLink to="/boards/board3" class="board-link">
        <div class="board-item-container">
          <h2>갓성비 챌린지</h2>
          <p>#듀플챌린지 #무지출챌린지 ...</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.board-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.board-header {
  text-align: center;
  margin-bottom: 3rem;
}

.board-title {
  color: #4d4d4d;
  font-size: 2rem;
}

.board-links {
  display: flex;
  flex-direction: column;  /* 세로로 배치 */
  gap: 1.5rem;  /* 간격 조정 */
}

.board-link {
  text-decoration: none;
  color: inherit;
  width: 100%;  /* 전체 너비 사용 */
}

.board-item-container {
  background: #faebda;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  display: flex;  /* 가로로 내용 배치 */
  align-items: center;  /* 세로 중앙 정렬 */
  justify-content: space-between;  /* 제목과 설명 사이 간격 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  height: 100px;  /* 높이 고정 */
}

.board-item-container h2 {
  color: #4d4d4d;
  font-size: 1.5rem;
  margin: 0;  /* 마진 제거 */
  flex: 0 0 auto;  /* 크기 고정 */
  width: 200px;  /* 제목 영역 너비 고정 */
}

.board-item-container p {
  color: #666;
  font-size: 1.1rem;
  margin: 0;  /* 마진 제거 */
  flex: 1;  /* 남은 공간 차지 */
  text-align: right;  /* 오른쪽 정렬 */
}

/* 호버 효과 */
.board-item-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #fbe9da 0%, #ffffff 100%);
}

/* 클릭 효과 */
.board-item-container:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .board-item-container {
    flex-direction: column;  /* 모바일에서는 세로로 배치 */
    height: auto;
    text-align: center;
    padding: 1.5rem;
  }

  .board-item-container h2 {
    width: auto;
    margin-bottom: 0.5rem;
  }

  .board-item-container p {
    text-align: center;
  }
}


</style>