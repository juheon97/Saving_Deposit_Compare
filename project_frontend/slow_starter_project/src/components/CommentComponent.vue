<template>
  <div class="comments-section">  
    <!-- 댓글 작성 폼 -->
    <div class="comment-form">
      <textarea 
        v-model="newComment" 
        placeholder="댓글을 입력하세요"
        rows="3"
      ></textarea>
      <button @click="createComment">댓글 작성</button>
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div v-if="editingCommentId === comment.id">
          <!-- 댓글 수정 폼 -->
          <textarea 
            v-model="editingCommentContent" 
            rows="3"
          ></textarea>
          <div class="comment-actions">
            <button @click="updateComment(comment.id)">수정 완료</button>
            <button @click="cancelEditComment">취소</button>
          </div>
        </div>
        <div v-else>
          <!-- 댓글 내용 -->
          <p>{{ comment.content }}</p>
          <p class="comment-date">
            작성일: {{ comment.created_at }}
            <span v-if="comment.updated_at !== comment.created_at">
              (수정됨: {{ comment.updated_at }})
            </span>
          </p>

          <LikeComponent
              type="comment"
              :board-id="boardId"
              :comment-id="comment.id"
              :is-liked="comment.is_liked"
              :like-count="comment.like_count"
              @like-updated="updateComment"
              :board-type="props.boardType"
          />
          <div class="comment-actions">
            <button @click="startEditComment(comment)">수정</button>
            <button @click="deleteComment(comment.id)">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LikeComponent from '@/components/LikeComponent.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useBoardStore } from '@/stores/board'

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

const props = defineProps({
  boardId: {
    type: [Number, String],
    required: true
  },
  boardType: {
    type: String,
    required: true
  }
})

const store = useBoardStore()
const comments = ref([])
const newComment = ref('')
const editingCommentId = ref(null)
const editingCommentContent = ref('')

// 댓글 불러오기
const loadComments = () => {
  axios({
    method: 'get',
    url:  `${store.API_URL}/boards/${props.boardType}/${props.boardId}/comments/`
  })
    .then((res) => {
      comments.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 작성
const createComment = () => {
if (!newComment.value.trim()) return

axios({
  method: 'post',
  url:`${store.API_URL}/boards/${props.boardType}/${props.boardId}/comments/`,
  data: {
    content: newComment.value
  },
  withCredentials: true
})
  .then(() => {
    newComment.value = ''
    loadComments()
  })
  .catch((err) => {
    if (err.response?.status === 401) {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('Comment error:', err.response?.data)
      alert('댓글 작성에 실패했습니다.')
    }
  })
}

// 댓글 수정 시작
const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editingCommentContent.value = comment.content
}

// 댓글 수정 취소
const cancelEditComment = () => {
  editingCommentId.value = null
  editingCommentContent.value = ''
}

// 댓글 수정 완료
const updateComment = (commentId) => {
  if (!editingCommentContent.value.trim()) return

  axios({
    method: 'put',
    url:  `${store.API_URL}/boards/${props.boardType}/${props.boardId}/comments/${commentId}/`,
    data: {
      content: editingCommentContent.value
    }
  })
    .then(() => {
      editingCommentId.value = null
      loadComments()
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 삭제
const deleteComment = (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return

  axios({
    method: 'delete',
    url:  `${store.API_URL}/boards/${props.boardType}/${props.boardId}/comments/${commentId}/`
  })
    .then(() => {
      loadComments()
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>

.comments-section {
  margin-top: 3rem;
  padding: 2rem;
  background-color: white;
  border-radius: 16px;  /* 전체 댓글 섹션 모서리 더 둥글게 */
}

.comments-section h3 {
 font-size: 1.5rem;
 color: #2c3e50;
 margin-bottom: 1.5rem;
 padding-bottom: 1rem;
 border-bottom: 2px solid #e9ecef;  /* 제목 아래 구분선 추가 */
}

.comment-form {
 margin-bottom: 2rem;
 background-color: white;  /* 흰색 배경으로 입력폼 강조 */
 padding: 1.5rem;
 border-radius: 6px;
 box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.comment-form textarea {
 width: 100%;
 padding: 0.75rem;
 border: 1px solid #ddd;
 border-radius: 4px;
 margin-bottom: 1rem;
 font-size: 0.95rem;
 resize: vertical;
}

.comment-form textarea:focus {
 outline: none;
 border-color: #4A90E2;
}

.comment-form button
{
 background-color:  #f8f9fa ;
 color: #666;
 border: 1px solid #e0e0e0;
 padding: 0.5rem 1rem;
 border-radius: 6px;
 cursor: pointer;
 transition: all 0.2s ease;
}
.comment-actions button {
  background-color:  #f8f9fa;
 color: #666;
 border: 1px solid #e0e0e0;
 padding: 0.5rem 1rem;
 border-radius: 6px;
 cursor: pointer;
 transition: all 0.2s ease;
}

.comment-form button:hover {
  background-color: #fff5d4;
}
.comment-actions button:hover {
background-color: #fff5d4;
}

.comments-list {
 margin-top: 2rem;
}

.comment {
 padding: 1.5rem;
 border-bottom: 1px solid #e9ecef;
 margin-bottom: 1rem;
 background-color: white;  /* 댓글 배경을 흰색으로 */
 border-radius: 6px;
 box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.comment:last-child {
 border-bottom: none;
 margin-bottom: 0;
}

.comment p {
 font-size: 1rem;
 line-height: 1.6;
 color: #34495e;
 margin-bottom: 0.5rem;
}

.comment-date {
 font-size: 0.85rem !important;
 color: #868e96 !important;  /* 날짜 색상 약간 더 연하게 */
 margin-bottom: 1rem !important;
}

.comment textarea {
 width: 100%;
 padding: 0.75rem;
 border: 1px solid #ddd;
 border-radius: 4px;
 margin-bottom: 1rem;
 font-size: 0.95rem;
 resize: vertical;
 background-color: #fff;  /* 수정 폼 배경색 명시 */
}

.comment textarea:focus {
 outline: none;
 border-color: #4A90E2;
}

.comment-actions {
 display: flex;
 gap: 0.5rem;
 margin-top: 1rem;
}

.comment-actions button {
 font-size: 0.85rem;
 padding: 0.4rem 0.8rem;
}
</style>