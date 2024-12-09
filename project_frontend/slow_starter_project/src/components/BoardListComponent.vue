<template>
  <div class="board-list">
    <BoardListItemComponent 
      v-for="board in store.boards"
      :key="board.id"
      :board="board"
      class="board-item"
    />
  </div>
</template>

<script setup>
import BoardListItemComponent from '@/components/BoardListItemComponent.vue'
import { useBoardStore } from '@/stores/board'

const store = useBoardStore()
</script>

<style scoped>
.board-list {
max-width: 1200px;
margin: 0 auto;
}

.board-item {
margin-bottom: 1rem;
}

</style>