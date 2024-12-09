import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useProfileStore = defineStore("profile", () => {
  const user_info = ref(null);
  const error = ref(null);
  const userProducts = ref(null)
  const selectedRates = ref({
    deposit: null,
    saving: null
  });

  const getUser = function () {
    const token = localStorage.getItem("token");

    axios({
      method: "get",
      url: "http://127.0.0.1:8000/accounts/get_user_info/",
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then((response) => {
      console.log(response.data);
      user_info.value = response.data;
    });
  };
  const updateProfileImage = async function (imageFile) {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("image", imageFile);
    
    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/accounts/update_profile_image/",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "multipart/form-data",
        },
        data: formData,
      });
      
      console.log('Image update response:', response);
      
      // 이미지 캐시 방지를 위한 타임스탬프 추가
      if (user_info.value) {
        user_info.value = {
          ...user_info.value,
          image: `${user_info.value.image}?t=${new Date().getTime()}`
        };
      }
      
      // 유저 정보 다시 불러오기
      await getUser();
      
      return response.data;
    } catch (err) {
      console.error("Error updating image:", err.response || err);
      error.value = err.response?.data?.error || err.message;
      throw err;
    }
  };

  const updateBasicInfo = function (userData) {
    const token = localStorage.getItem("token");
    
    // 빈 값은 제외하고 보내기
    const data = {};
    if (userData.first_name) data.first_name = userData.first_name;
    if (userData.email) data.email = userData.email;
    if (userData.gender) data.gender = userData.gender;
    if (userData.age) data.age = parseInt(userData.age);
    
    // balance 정보 추가 - 소수점 2자리까지 변환
    if (userData.balance_deposit) {
        data.balance_deposit = parseFloat(userData.balance_deposit).toFixed(2);
    }
    if (userData.balance_saving) {
        data.balance_saving = parseFloat(userData.balance_saving).toFixed(2);
    }

    return axios({
      method: "patch",
      url: "http://127.0.0.1:8000/accounts/get_user_info/",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      data: data,
    })
      .then((response) => {
        getUser();
        error.value = null;
      })
      .catch((err) => {
        console.error("Error updating user info:", err.response || err);
        error.value = err.response?.data?.error || err.message;
      });
  };

  const getUserProducts = function() {
    const token = localStorage.getItem('token')
    
    axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/accounts/get_user_products/',  // Django에서 새로 만들 API 엔드포인트
        headers: {
            'Authorization': `Token ${token}`,
        }
    })
    .then(response => {
        userProducts.value = response.data
        error.value = null
    })
    .catch(err => {
        console.error('Error fetching user products:', err.response || err)
        error.value = err.response?.data?.error || err.message
    })
}
const deleteUserProduct = function(type, productId) {
  const token = localStorage.getItem('token')
  
  axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/accounts/delete_user_product/${type}/${productId}/`,
      headers: {
          'Authorization': `Token ${token}`,
      }
  })
  .then(() => {
      getUserProducts()  // 목록 다시 불러오기
  })
  .catch(err => {
      console.error('Error deleting product:', err.response || err)
      error.value = err.response?.data?.error || err.message
  })
}

const changePassword = function(oldPassword, newPassword1, newPassword2) {
  const token = localStorage.getItem('token')
  
  return axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/accounts/change_password/',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    },
    data: {
      old_password: oldPassword,
      new_password1: newPassword1,
      new_password2: newPassword2
    }
  })
  .then(response => {
    error.value = null
    // 비밀번호 변경 성공 후 토큰 제거
    localStorage.removeItem('token')
    return {
      success: true,
      message: response.data.message
    }
  })
  .catch(err => {
    console.error('Error changing password:', err.response || err)
    error.value = err.response?.data?.message || '비밀번호 변경 중 오류가 발생했습니다.'
    return {
      success: false,
      message: error.value
    }
  })
}

const setSelectedRates = function({ deposit, saving }) {
  // deposit이 전달된 경우에만 deposit을 업데이트
  if (deposit !== undefined) {
    selectedRates.value = {
      ...selectedRates.value,
      deposit: deposit
    };
  }
  
  // saving이 전달된 경우에만 saving을 업데이트
  if (saving !== undefined) {
    selectedRates.value = {
      ...selectedRates.value,
      saving: saving
    };
  }
};


  return { user_info, getUser, updateProfileImage, updateBasicInfo, error, userProducts, getUserProducts, deleteUserProduct, changePassword,
    selectedRates, setSelectedRates
  };

  
});
