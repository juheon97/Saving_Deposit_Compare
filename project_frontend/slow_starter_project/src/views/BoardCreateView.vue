<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBoardStore } from '@/stores/board'
import axios from 'axios'

// props 정의
const props = defineProps({
  mode: {
    type: String,
    default: 'create'
  }
})

const store = useBoardStore()
const route = useRoute()
const router = useRouter()

// form data
const title = ref('')
const content = ref('')
const image = ref(null)

// 이미지 처리 함수
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    image.value = file
  }
}

// 게시글 생성
const createBoard = async () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  try {
    await axios({
      method: 'post',
      url: `${store.API_URL}/boards/${route.params.boardType}/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      withCredentials: true
    })
    router.push({ name: `Board${route.params.boardType.slice(-1)}` })
  } catch (error) {
    console.error('Error creating board:', error)
  }
}

// 취소 처리
const handleCancel = () => {
  router.push({ name: `Board${route.params.boardType.slice(-1)}` })
}
</script>

<template>
  <div class="board-create-container">
    <div class="board-header">
      <router-link :to="{ name: `Board${route.params.boardType.slice(-1)}` }" class="back-button">
        <span>←</span> 뒤로가기
      </router-link>
      <h1 class="board-title">게시글 작성</h1>
    </div>

    <div class="board-form">
      <form @submit.prevent="createBoard">
        <div class="form-group">
          <label for="title" class="form-label">제목:</label>
          <input 
            type="text" 
            id="title" 
            v-model="title" 
            required 
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="content" class="form-label">내용:</label>
          <textarea 
            id="content" 
            v-model="content" 
            required 
            class="form-textarea"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="image" class="form-label">이미지:</label>
          <input 
            type="file" 
            id="image" 
            @change="handleImageChange" 
            accept="image/*" 
            class="form-input"
          >
        </div>

        <div class="button-group">
          <button type="submit" class="btn btn-primary">작성</button>
          <button type="button" @click="handleCancel" class="btn btn-secondary">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.board-create-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.board-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #666;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
}

.board-title {
  margin: 0;
  color: #2c5282;
  font-size: 1.5rem;
}

.board-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c5282;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.form-textarea {
  min-height: 200px;
  resize: vertical;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
  border: none;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #e0e0e0;
}

.btn:hover {
  transform: translateY(-2px);
}
</style>