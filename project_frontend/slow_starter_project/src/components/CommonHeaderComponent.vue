<template>
  <v-card color="sky">
    <v-card-title class="text-center justify-center py-6" style="padding:0  !important; padding-top: 0 !important; padding-bottom: 0 !important; ">
  <img 
    src="@/assets/logos/logo.png" 
    alt="Slow Starter Logo" 
    class="cursor-pointer" 
    @click="handleTabClick('/')"
    height="100"
    width="250"
  />
</v-card-title>

    <v-tabs
      v-model="tab"
      bg-color="transparent"
      color="sky"
      grow
    >
      <v-tab
        v-for="item in items"
        :key="item.text"
        :text="item.text"
        :value="item.text"
        @click="handleTabClick(item.route)"
      >
      <v-img
          :src="item.icon"
          width="25"
          height="25"
          class="mb-2 "
        ></v-img>
        {{ item.text }}
      </v-tab>
          <div class="d-flex align-center">
        <template v-if="!isLogin">
          <v-btn
            variant="text"
            color="sky"
            class="mx-2"
            @click="handleTabClick('/login')"
          >
          로그인
      </v-btn>
      <v-btn
        variant="text"
        color="sky"
        class="mx-2"
        @click="handleTabClick('/signup')"
      >
        회원가입
      </v-btn>
    </template>
    
    <template v-else>
      <v-btn
        variant="text"
        color="sky"
        class="mx-2"
        @click="handleTabClick('/profile')"
      >
        프로필
      </v-btn>
      <v-btn
        variant="text"
        color="sky"
        class="mx-2"
        @click=logOut()
      >
        로그아웃
      </v-btn>
    </template>
  </div>
</v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item
        v-for="item in items"
        :key="item.text"
        :value="item.text"
      >
        <v-card
          color="sky"
          flat
        >
          <v-card-text style="padding: 0; margin: 0;">{{ text }}</v-card-text>
        </v-card>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-card>
</template>

<script>
import { useRouter} from 'vue-router';
// 이미지 import
import glassIcon from '@/assets/navbar/glass.png'
import bestProductIcon from '@/assets/navbar/best-product.png'
import mapIcon from '@/assets/navbar/map.png'
import dollarIcon from '@/assets/navbar/dollar.png'
import groupIcon from '@/assets/navbar/group.png'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

      export default {
        setup() {
          const store = useUserStore()
          const router = useRouter();
          const isLogin = computed(() => store.isLogin)
          
    
          return {
            router,
            isLogin,// setup에서 반환하여 템플릿에서 사용 가능하게 함
          }
          
        },
        

    data () {
      return {
        tab: '조회',
        items: [
          {
          text: '조회',
          icon: glassIcon,   // 이미지 크기 키우고, 글씨 위로 올리도록! 
          route: '/search'//라우트 임포넌트로 이동
          },
          {
            text: '상품추천',
            icon: bestProductIcon,
            route: '/recommend'
          },
          {
            text: '지도',
            icon: mapIcon,
            route: '/map'
          },
          {
            text: '환전',
            icon: dollarIcon,
            route: '/exchange'
          },
          {
            text: '커뮤니티',
            icon: groupIcon,
            route: '/boards'
          }
        ],
        // text: 'slow starter!' // 각 버튼마다 나오는게 다르도록!
      }
    },
    
    methods: {
      handleTabClick(route) {
        this.router.push(route)
      },
      logOut() {
      const store = useUserStore()
      store.logOut()
      this.router.push('/')
    }
    }
  }



</script>

<style>
/* Helper classes */
.cursor-pointer {
  cursor: pointer;
}
.bg-sky {
  background-color: #FFFFFD !important;
}
.text-sky {
  color: #333333  !important;
}
.custom-btn {
  background-color: #ffd8b8 !important;
}
.custom-btn:hover {
  background-color: #ffc9a0 !important;
}
.custom-text {
  color: #333333 !important;
}
.custom-peach {
  color: #ffd8b8 !important;
}
</style>