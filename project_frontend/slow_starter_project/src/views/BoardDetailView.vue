<template>
  <div class="board-detail-container">
    <div class="board-header">
      <router-link :to="{ name: `Board${route.params.boardType.slice(-1)}` }" class="back-button">
        <span>←</span> 뒤로가기
      </router-link>
    </div>
    <div v-if="board" class="board-content-wrapper">
        <div v-if="isEditing" class="edit-form">
          <form @submit.prevent="updateBoard">
            <div class="form-group">
              <label for="title" class="form-label">제목 : </label>
              <input type="text" id="title" v-model="editTitle" class="form-input">
              <label for="content" class="form-label">내용 : </label>
              <textarea id="content" v-model="editContent" class="form-textarea"></textarea>
                <!-- 이미지 업로드 부분 추가 -->
                <div class="image-upload">
                <label for="image" class="form-label">이미지 : </label>
                <input 
                  type="file" 
                  id="image" 
                  @change="handleImageChange" 
                  accept="image/*"
                  class="form-input"
                >
                <!-- 기존 이미지 표시 -->
                <div v-if="board.image" class="current-image">
                  <img :src="getImageUrl(board.image)" alt="Current image">
                  <button @click.prevent="clearImage" class="btn btn-clear">이미지 삭제</button>
                </div>
              </div>
            </div>
            <div class="button-group">
              <button type="submit" class="btn btn-primary">수정 완료</button>
              <button @click="cancelEdit" class="btn btn-secondary">취소</button>
            </div>
          </form>
      </div>
      <div v-else class="board-view">
        <div class="content-block">
          <p class="board-info"><span class="label">게시글 번호 :</span> {{ board.id }}</p>
          <div class="content-block">
            <p class="board-info"><span class="label">제목 :</span> {{ board.title }}</p>
            <p class="board-info"><span class="label">내용 :</span> {{ board.content }}</p>
            <div class="board-meta">
              <LikeComponent
                type="board"
                :board-id="route.params.id"
                :board-type="route.params.boardType"
                :is-liked="board.is_liked"
                :like-count="board.like_count"
                @like-updated="handleLikeUpdate"
              />
              <div class="date-info">
                <p>작성일: {{ formatDate(board.created_at) }}</p>
                <p>수정일: {{ formatDate(board.updated_at) }}</p>
              </div>
            </div>
            <!-- 이미지 표시 -->
            <div v-if="board.image" class="board-image">
              <img :src="getImageUrl(board.image)" :alt="board.title">
            </div>
          </div>
        </div>
        <div class="button-group">
          <button @click="startEditing" class="btn btn-edit">수정</button>
          <button @click="deleteBoard" class="btn btn-delete">삭제</button>
        </div>
      </div>
      <div class="comment-section">
        <CommentComponent 
          :board-id="board.id"
          :board-type="route.params.boardType"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import LikeComponent from '@/components/LikeComponent.vue'
import CommentComponent from '@/components/CommentComponent.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/board'
import { useRoute, useRouter } from 'vue-router'

const newImage = ref(null)
const imageToDelete = ref(false)
const store = useBoardStore()
const route = useRoute()
const router = useRouter()
const board = ref(null)
const isEditing = ref(false)
const editTitle = ref('')
const editContent = ref('')

// 이미지 변경 핸들러 추가
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    newImage.value = file
    imageToDelete.value = false
  }
}

// 이미지 삭제 핸들러 추가
const clearImage = () => {
  newImage.value = null
  imageToDelete.value = true
}

// 게시글 로드 함수
const loadBoard = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/boards/${route.params.boardType}/${route.params.id}/`,
      withCredentials: true
    })
    board.value = response.data
    editTitle.value = response.data.title
    editContent.value = response.data.content
  } catch (error) {
    console.error('Error loading board:', error)
    router.push({ name: `Board${route.params.boardType.slice(-1)}` })
  }
}

// 이미지 URL 처리
const getImageUrl = (imageUrl) => {
  if (imageUrl && !imageUrl.startsWith('http')) {
    return `${store.API_URL}${imageUrl}`
  }
  return imageUrl
}

// 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 좋아요 업데이트 핸들러
const handleLikeUpdate = (event) => {
  board.value.is_liked = event.is_liked
  board.value.like_count = event.like_count

  // 게시글 목록 상태도 업데이트
  const boardIndex = store.boards.findIndex(b => b.id === Number(route.params.id))
  if (boardIndex !== -1) {
    store.boards[boardIndex].is_liked = event.is_liked
    store.boards[boardIndex].like_count = event.like_count
  }
}

// 수정 시작
const startEditing = () => {
  isEditing.value = true
}

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false
  editTitle.value = board.value.title
  editContent.value = board.value.content
}

// 게시글 수정
  const updateBoard = async () => {
  const formData = new FormData()
  formData.append('title', editTitle.value)
  formData.append('content', editContent.value)
  
  // 이미지 처리
  if (newImage.value) {
      formData.append('image', newImage.value)
    } else if (imageToDelete.value) {
      formData.append('image_clear', 'true')
    }

    try {
      const response = await axios({
        method: 'put',
        url: `${store.API_URL}/boards/${route.params.boardType}/${route.params.id}/`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
      })
    
    board.value = response.data
    isEditing.value = false
    newImage.value = null
    imageToDelete.value = false
  } catch (error) {
    console.error('Error updating board:', error)
  }


  axios({
    method: 'put',
    url: `${store.API_URL}/boards/${route.params.boardType}/${route.params.id}/`,
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
    .then((res) => {
      board.value = res.data
      isEditing.value = false
    })
    .catch((err) => {
      console.log(err)
    })
}

// 게시글 삭제
const deleteBoard = () => {
  if (confirm('정말로 삭제하시겠습니까?')) {
    axios({
      method: 'delete',
      url: `${store.API_URL}/boards/${route.params.boardType}/${route.params.id}/`
    })
      .then(() => {
        router.push({ name: `Board${route.params.boardType.slice(-1)}` })
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

onMounted(() => {
  loadBoard()
})
</script>

<style scoped>
.board-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff1e6; 
  min-height: 100vh;
}

.board-content-wrapper {
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(144, 205, 244, 0.2);
  margin-top: 2rem;
}

.content-block {
  margin-bottom: 2rem;
}

.board-info {
  margin: 0.5rem 0;
  color: #333333;
}

.label {
  font-weight: 500;
  color: #333333;
  margin-right: 0.5rem;
}

.board-meta {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-info {
  color: #333333;
  font-size: 0.9rem;
}

.board-image {
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  max-height: 500px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.board-image img {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffe4d1;
  color: #333333;
  border: 1px solid #e0e0e0;
  font-size: 0.95rem;
}

.btn:hover {
  background-color: #ffe9d9;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(144, 205, 244, 0.3);
}

.btn-delete:hover {
  background-color: #ffe9d9;
}

.comment-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  background-color: #ffe4d1;
  color: #333333;
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  border: 1px solid #e0e0e0;
  transition: all 0.2s ease;
}

.back-button:hover {
  background-color: #ffe9d9;
  transform: translateY(-2px);
}

/* 미디어 쿼리 */
@media (max-width: 768px) {
  .board-image {
    max-width: 100%;
  }
  
  .button-group {
    flex-direction: row;
    gap: 0.5rem;
  }
  
  .btn {
    flex: 1;
  }
}

.image-upload {
  margin-top: 1rem;
}

.current-image {
  margin: 1rem 0;
  position: relative;
}

.current-image img {
  max-width: 200px;
  height: auto;
  border-radius: 4px;
}

.btn-clear {
  margin-top: 0.5rem;
  background-color: #ffe4d1;
  color: #333333;
}

.btn-clear:hover {
  background-color: #ffe9d9;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 500;
  color: #333333;
}

.form-input {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  width: 100%;
}

.form-textarea {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  width: 100%;
  min-height: 150px;
  resize: vertical;
}
</style>