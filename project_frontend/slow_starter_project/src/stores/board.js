import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useBoardStore = defineStore('board', () => {
  const boards = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getBoards = function (boardType) {
    axios({
      method: 'get',
      url: `${API_URL}/boards/${boardType}/`,
      withCredentials: true 
    })
      .then((res) => {
        boards.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const updateBoardLike = function (boardId, isLiked, likeCount) {
    const board = boards.value.find(b => b.id === boardId)
    if (board) {
      board.is_liked = isLiked
      board.like_count = likeCount
    }
  }
  
  return { boards, API_URL, getBoards, updateBoardLike }
}, { persist: true })
