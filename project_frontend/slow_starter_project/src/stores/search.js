// store/search.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useSearchStore = defineStore("search", () => {
 const depositProducts = ref([]);
 const savingProducts = ref([]);
 const selectedItems = ref([]);
 const depositOptions = ref([]);
 const savingOptions = ref([]);

 // 예금상품 정보와 옵션 가져오기
 // store/search.js 수정
 const get_deposit_products_info = async function () {
  try {
    const [productsResponse, optionsResponse] = await Promise.all([
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/products/get_deposit_products/",
      }),
      axios({
        method: "get",  
        url: "http://127.0.0.1:8000/products/get_deposit_options/",
      })
    ]);

    depositProducts.value = productsResponse.data;
    depositOptions.value = optionsResponse.data;

    if (localStorage.getItem('token')) {
      const userData = JSON.parse(localStorage.getItem('user'));
      const userId = userData.userInfo.id;  // userInfo 안의 id를 가져옴

      depositProducts.value.forEach(product => {
        if (Array.isArray(product.user_contains)) {
          isContained.value[product.id] = product.user_contains.some(
            user => user.id === userId
          );
        }
      });
    }

  } catch (error) {
    console.error('예금상품 정보 로딩 실패:', error);
    throw error;
  }
};

const get_saving_products_info = async function () {
  try {
    const [productsResponse, optionsResponse] = await Promise.all([
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/products/get_saving_products/",
      }),
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/products/get_saving_options/",
      })
    ]);

    savingProducts.value = productsResponse.data;
    savingOptions.value = optionsResponse.data;

    if (localStorage.getItem('token')) {
      const userData = JSON.parse(localStorage.getItem('user'));
      const userId = userData.userInfo.id;  // userInfo 안의 id를 가져옴

      savingProducts.value.forEach(product => {
        if (Array.isArray(product.user_contains)) {
          isContained.value[product.id] = product.user_contains.some(
            user => user.id === userId
          );
        }
      });
    }

  } catch (error) {
    console.error('적금상품 정보 로딩 실패:', error);
    throw error;
  }
};
 const isCompareButtonActive = computed(() => selectedItems.value.length >= 2);

 const toggleItemSelection = (product) => {
  const uniqueId = getUniqueProductId(product);
  const index = selectedItems.value.findIndex((item) => item.uniqueId === uniqueId);

  if (index === -1) {
    if (selectedItems.value.length >= 4) {
      alert("최대 4개까지만 선택할 수 있습니다!");
      return false;
    }
    selectedItems.value.push({
      uniqueId,
      productId: product.id,
      type: product.Deposit_code === 1 ? 'deposit' : 'saving',
      kor_co_nm: product.kor_co_nm,
      fin_prdt_nm: product.fin_prdt_nm,
      Deposit_code: product.Deposit_code,
      product: product  // 전체 상품 정보를 저장
    });
  } else {
    selectedItems.value.splice(index, 1);
  }
  return true;
};

const removeSelectedItem = (uniqueId) => {
  const index = selectedItems.value.findIndex((item) => item.uniqueId === uniqueId);
  if (index !== -1) {
    selectedItems.value.splice(index, 1);
  }
};

 // getSelectedProductsDetails 추가
 const getSelectedProductsDetails = computed(() => {
  return selectedItems.value.map((item) => {
    const product = item.product;
    if (!product) return null;

    const options = product.Deposit_code === 1
      ? depositOptions.value.filter(opt => opt.deposit_product === product.id)
      : savingOptions.value.filter(opt => opt.saving_product === product.id);

    return {
      ...product,
      options
    };
  }).filter(item => item !== null);
});

 const isContained = ref({});

 const getUniqueProductId = (product) => {
  const type = product.Deposit_code === 1 ? 'deposit' : 'saving';
  return `${type}_${product.id}`;
};
 

const fetchContainedProducts = async () => {
    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/products/contained_products/',
        {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`
          }
        }
      );
      
      // 서버에서 받은 담은 상품 목록으로 상태 초기화
      isContained.value = {};
      response.data.products.forEach(product => {
        const uniqueId = `${product.type}_${product.id}`;
        isContained.value[uniqueId] = true;
      });

      localStorage.setItem('isContained', JSON.stringify(isContained.value));
    } catch (error) {
      console.error('담은 상품 목록 가져오기 실패:', error);
      if (error.response?.status === 401) {
        alert('로그인이 필요합니다.');
      }
    }
  };
  const toggleContainer = async (product) => {
    const productType = product.Deposit_code === 1 ? 'deposit' : 'saving';
    const uniqueId = getUniqueProductId(product);

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/products/toggle_contain/',
        {
          product_id: product.id,
          product_type: productType
        },
        {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`
          }
        }
      );

      isContained.value[uniqueId] = response.data.is_contained;
      localStorage.setItem('isContained', JSON.stringify(isContained.value));
      
      alert(response.data.message);
    } catch (error) {
      if (error.response?.status === 401) {
        alert('로그인이 필요합니다.');
      } else {
        alert('오류가 발생했습니다.');
      }
    }
  };

  const isItemSelected = (product) => {
    const uniqueId = getUniqueProductId(product);
    return selectedItems.value.some((item) => item.uniqueId === uniqueId);
  };

 const clearContainedState = () => {
   isContained.value = {};
   localStorage.removeItem('isContained');
 };

 



 return {
   depositProducts,
   savingProducts,
   depositOptions,
   savingOptions,
   get_deposit_products_info,
   get_saving_products_info,
   selectedItems,
   isCompareButtonActive,
   toggleItemSelection,
   removeSelectedItem,
   getSelectedProductsDetails,
   toggleContainer,
   isContained,
   fetchContainedProducts,
   clearContainedState,
   isItemSelected,
   getUniqueProductId,

 };
});