<template>
  <div class="like-display">
    <span class="heart-icon" :class="{ 'liked': isLiked }">
      {{ isLiked ? '💛' : '🤍' }}
    </span>
    <span class="like-count">{{ likeCount }}</span>
  </div>
</template>

<script setup>
defineProps({
  isLiked: {
    type: Boolean,
    default: false
  },
  likeCount: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.like-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  background: #f8f8f8;
}

.heart-icon {
  font-size: 1.2rem;
}

.like-count {
  font-size: 0.9rem;
  color: #666;
  min-width: 20px;
  text-align: center;
}

.heart-icon.liked {
  transform: scale(1.1);
}
</style>