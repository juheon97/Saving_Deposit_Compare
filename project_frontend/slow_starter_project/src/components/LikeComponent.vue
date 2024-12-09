<template>
  <div class="like-container">
    <button @click="toggleLike" class="like-button">
      <span class="heart-icon" :class="{ 'liked': localIsLiked }">
        {{ localIsLiked ? '💛' : '🤍' }}
      </span>
      <span class="like-count">{{ localLikeCount }}</span>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useBoardStore } from '@/stores/board'

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  boardId: {
    type: [Number, String],
    required: true
  },
  boardType: {
    type: String,
    required: true
  },
  commentId: {
    type: [Number, String],
    default: null
  },
  isLiked: {
    type: Boolean,
    required: true
  },
  likeCount: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['like-updated'])
const store = useBoardStore()

const localIsLiked = ref(props.isLiked)
const localLikeCount = ref(props.likeCount)

// props가 변경될 때 로컬 상태 업데이트
watch(() => props.isLiked, (newVal) => {
  localIsLiked.value = newVal
})

watch(() => props.likeCount, (newVal) => {
  localLikeCount.value = newVal
})

const toggleLike = async () => {
  try {
    const url = props.type === 'board'
      ? `${store.API_URL}/boards/${props.boardType}/${props.boardId}/like/`
      : `${store.API_URL}/boards/${props.boardType}/${props.boardId}/comments/${props.commentId}/like/`

    const response = await axios({
      method: 'post',
      url: url,
      withCredentials: true
    })

    if (response.data) {
      localIsLiked.value = response.data.is_liked
      localLikeCount.value = response.data.like_count
      emit('like-updated', {
        is_liked: response.data.is_liked,
        like_count: response.data.like_count
      })
    }
  } catch (err) {
    if (err.response?.status === 401) {
      alert('로그인이 필요한 기능입니다.')
    } else {
      console.error('Like error:', err)
    }
  }
}
</script>

<style scoped>
.like-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.like-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-button:hover {
  background-color: #f8f8f8;
  transform: scale(1.05);
}

.heart-icon {
  font-size: 1.2rem;
  transition: transform 0.2s ease;
}

.heart-icon.liked {
  transform: scale(1.1);
}

.like-count {
  font-size: 0.9rem;
  color: #666;
  min-width: 20px;
  text-align: center;
}
</style>