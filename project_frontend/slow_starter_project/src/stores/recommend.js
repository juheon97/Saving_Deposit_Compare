// stores/recommend.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useRecommendStore = defineStore('recommend', () => {
  // state
  const depositProducts = ref([])
  const savingProducts = ref([])
  const selectedType = ref('deposit')  // 'deposit' 또는 'saving'
  const selectedAgeGroup = ref('20')   // 그래프용 선택된 연령대
  const API_URL = 'http://127.0.0.1:8000'

  // topProducts 구조 초기화
  const topProducts = ref({
    deposit: {
      '20': [], '30': [], '40': [], '50': []
    },
    saving: {
      '20': [], '30': [], '40': [], '50': []
    }
  })

  // actions
  const getProducts = async () => {
    try {
      const [depositRes, savingRes] = await Promise.all([
        axios.get(`${API_URL}/products/get_deposit_products/`),
        axios.get(`${API_URL}/products/get_saving_products/`)
      ])
      // console.log('Deposit Products:', depositRes.data)
      // console.log('Saving Products:', savingRes.data)
      depositProducts.value = depositRes.data
      savingProducts.value = savingRes.data
      calculateTopProducts()
    } catch (err) {
      console.log(err)
    }
  }

  const calculateTopProducts = () => {
    // console.log('Calculating top products...')
    const ageGroups = ['20', '30', '40', '50']
    
    // 예금 상품 계산
    ageGroups.forEach(ageGroup => {
      // 디버깅을 위한 로그 추가
      // console.log(`Calculating for age group ${ageGroup}`)
      // console.log('Sample product:', depositProducts.value[0])
      // console.log('Sample product user_contains:', depositProducts.value[0]?.user_contains)
  
      const depositCounts = depositProducts.value.reduce((acc, product) => {
        if (!product.user_contains) {
          // console.log('No user_contains for product:', product)
          return acc
        }
  
        const usersInAgeGroup = product.user_contains.filter(user => {
          if (!user.age) {
            // console.log('No age for user:', user)
            return false
          }
          const age = user.age
          const ageGroupStart = parseInt(ageGroup)
          return age >= ageGroupStart && age < ageGroupStart + 10
        })
        
        if (usersInAgeGroup.length > 0) {
          acc.push({
            ...product,
            userCount: usersInAgeGroup.length
          })
        }
        return acc
      }, [])
  
      // console.log(`Deposit counts for age group ${ageGroup}:`, depositCounts)
      
      topProducts.value.deposit[ageGroup] = depositCounts
        .sort((a, b) => b.userCount - a.userCount)
        .slice(0, 3)
    })

    // 적금 상품 계산
    ageGroups.forEach(ageGroup => {
      const savingCounts = savingProducts.value.reduce((acc, product) => {
        const usersInAgeGroup = product.user_contains.filter(user => {
          const age = user.age
          const ageGroupStart = parseInt(ageGroup)
          return age >= ageGroupStart && age < ageGroupStart + 10
        })
        
        if (usersInAgeGroup.length > 0) {
          acc.push({
            ...product,
            userCount: usersInAgeGroup.length
          })
        }
        return acc
      }, [])

      topProducts.value.saving[ageGroup] = savingCounts
        .sort((a, b) => b.userCount - a.userCount)
        .slice(0, 3)
    })
    // console.log('Top Products after calculation:', topProducts.value)
  }

  // getters
  const getTopProductsByAge = computed(() => {
    return (ageGroup) => topProducts.value[selectedType.value][ageGroup]
  })

  const getCurrentAgeGroupData = computed(() => {
    return topProducts.value[selectedType.value][selectedAgeGroup.value]
  })

  // type과 ageGroup 변경 함수
  const changeProductType = (type) => {
    selectedType.value = type
  }

  const changeAgeGroup = (ageGroup) => {
    selectedAgeGroup.value = ageGroup
  }

  const toggleProduct = async (productId, productType) => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No token found')
      }
  
      const response = await axios.post(
        `${API_URL}/products/toggle_contain/`, 
        {
          product_id: productId,
          product_type: productType
        },
        {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          }
        }
      )
      
      // 성공하면 상품 목록 다시 불러오기
      await getProducts()
      return response.data
    } catch (err) {
      // console.error('Toggle product error:', err)
      throw err
    }
  }

  return { 
    depositProducts,
    savingProducts,
    selectedType,
    selectedAgeGroup,
    topProducts,
    API_URL,
    getProducts,
    getTopProductsByAge,
    getCurrentAgeGroupData,
    changeProductType,
    changeAgeGroup,
    toggleProduct
  }
}, { persist: true })