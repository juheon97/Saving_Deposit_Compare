<!-- RecommendItemList.vue -->
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRecommendStore } from '@/stores/recommend'
import { useRouter } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  products: {
    type: Array,
    default: () => []
  }
})

const store = useRecommendStore()
const router = useRouter()
const loading = ref(false)

const isContained = (product) => {
  const userId = Number(localStorage.getItem('userId'))
  // console.log('Product:', product.id, 'User contains:', product.user_contains, 'UserId:', userId)
  
  if (!userId) {
    // console.warn('No userId found in localStorage')
    return false
  }

  return product.user_contains?.some(user => user.id === userId) || false
}

const handleToggle = async (product) => {
  if (!localStorage.getItem('token')) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }

  try {
    loading.value = true
    await store.toggleProduct(
      product.id,
      store.selectedType
    )
    // 성공 후 products 다시 로드
    await store.getProducts()
  } catch (error) {
    // console.error('Error toggling product:', error)
    alert('처리 중 오류가 발생했습니다.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-carousel
      show-arrows="hover"
      height="300"
      hide-delimiter-background
    >
      <template v-if="!products || products.length === 0">
        <v-carousel-item>
          <v-sheet height="100%" class="d-flex align-center justify-center">
            <span class="text-h6">아직 추천 상품이 없습니다.</span>
          </v-sheet>
        </v-carousel-item>
      </template>
      
      <template v-else>
        <v-carousel-item
          v-for="product in products"
          :key="product.fin_prdt_cd"
        >
          <v-sheet height="100%" class="pa-4">
            <v-card flat>
              <v-card-title class="text-h6">{{ product.kor_co_nm }}</v-card-title>
              <v-card-subtitle>{{ product.fin_prdt_nm }}</v-card-subtitle>
              <v-card-text>
                <v-row align="center" justify="center">
                  <v-col cols="12">
                    <div>가입 방법: {{ product.join_way }}</div>
                    <div>가입 대상: {{ product.join_member }}</div>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions class="justify-center">
                <v-btn
                  :color="isContained(product) ? 'error' : 'primary'"
                  @click="handleToggle(product)"
                  :loading="loading"
                >
                  {{ isContained(product) ? '담기 취소' : '담기' }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-sheet>
        </v-carousel-item>
      </template>
    </v-carousel>
  </v-card>
</template>