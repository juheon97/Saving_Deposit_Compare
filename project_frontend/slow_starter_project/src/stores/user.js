import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export const useUserStore = defineStore(
 "user",
 () => {
   const API_URL = "http://127.0.0.1:8000";
   const router = useRouter();
   const token = ref(null);
   const userInfo = ref(null);
   const isLogin = computed(() => token.value !== null);

    const signUp = async (payload) => {
      try {
        const response = await axios.post(`${API_URL}/accounts/signup/`, payload);
        // 회원가입 후 바로 로그인하는 부분 수정
        if (response.data) {
          const loginPayload = {
            username: payload.username,
            password: payload.password1, // password1을 password로 변경
          };
          await logIn(loginPayload);
          // alert('로그인되었습니다.');
        }
      } catch (err) {
        console.error("회원가입 에러:", err.response?.data || err.message);
        alert(
          Object.values(err.response?.data || {})
            .flat()
            .join("\n") || "회원가입에 실패했습니다."
        );
      }
    };

   const logIn = async (payload) => {
     try {
       const response = await axios.post(`${API_URL}/accounts/login/`, payload);
       setToken(response.data.key);
       // 로그인 성공 후 사용자 정보 가져오기
       await getUserInfo();
       router.push('/profile');
       alert('로그인이 완료되었습니다.');
     } catch (err) {
       console.error('로그인 에러:', err.response?.data || err.message);
       alert(err.response?.data?.non_field_errors?.[0] || '로그인에 실패했습니다.');
     }
   };

   const logOut = async () => {
     try {
       await axios.post(
         `${API_URL}/accounts/logout/`,
         {},
         {
           headers: {
             Authorization: `Token ${token.value}`
           }
         }
       );
       clearToken();
       router.push('/login');
       alert('로그아웃이 완료되었습니다.');
     } catch (err) {
       console.error('로그아웃 에러:', err.response?.data || err.message);
       clearToken();
       router.push('/');
       alert('다음에 또 만나요~!');
     }
   };
    const findPassword = async (payload) => {
      try {
        const response = await axios.post(`${API_URL}/accounts/find_password/`, payload);
        return {
          success: true,
          tempPassword: response.data.temp_password,
          message: '임시 비밀번호가 생성되었습니다.'
        };
      } catch (err) {
        console.error("비밀번호 찾기 에러:", err.response?.data || err.message);
        return {
          success: false,
          message: err.response?.data?.message || "사용자 정보를 찾을 수 없습니다."
        };
      }
    };
    
    const setToken = (newToken) => {
      token.value = newToken;
      localStorage.setItem('token', newToken);
     // axios 기본 헤더 설정
      axios.defaults.headers.common['Authorization'] = `Token ${newToken}`;
   };
   
   const clearToken = () => {
     token.value = null;
     userInfo.value = null;
     localStorage.removeItem('token');
     localStorage.removeItem('userId');
     delete axios.defaults.headers.common['Authorization'];
   };

      const getUserInfo = async () => {
     try {
       const storedToken = localStorage.getItem('token');
       if (storedToken) {
         setToken(storedToken);
         const response = await axios.get(`${API_URL}/accounts/user/`, {
           headers: {
             Authorization: `Token ${storedToken}`
           }
         });
         userInfo.value = response.data;
         localStorage.setItem('userId', response.data.id.toString());
        return response.data;  // 데이터 반환 추가
       }
     } catch (err) {
       console.error('사용자 정보 가져오기 에러:', err.response?.data || err.message);
       clearToken();
     }
   };

   // 초기화 시 토큰 및 사용자 정보 복구
   const initializeAuth = async () => {
     const storedToken = localStorage.getItem('token');
     if (storedToken) {
       await getUserInfo();
     }
   };

   const isAuthenticated = computed(() => !!token.value);

    return { API_URL, signUp, logIn, logOut, token, isLogin, findPassword, setToken, clearToken, getUserInfo, initializeAuth, isAuthenticated, userInfo };
  },
  { persist: true });

