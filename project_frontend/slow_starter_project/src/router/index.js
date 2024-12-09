import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MapView from '@/views/MapView.vue'
import ProfileView from '@/views/ProfileView.vue'
import RecommendView from '@/views/RecommendView.vue'
import SearchView from '@/views/SearchView.vue'
import BoardDetailView from '@/views/BoardDetailView.vue'
import BoardCreateView from '@/views/BoardCreateView.vue'
import Password from '@/views/Password.vue'
import FindPassword from '@/views/FindPassword.vue'
import MainBoard from '@/views/MainBoard.vue'
import Board1 from '@/views/Board1.vue'
import Board2 from '@/views/Board2.vue'
import Board3 from '@/views/Board3.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    {
      path: '/exchange',
      name: 'ExchangeView',
      component: ExchangeView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/map',
      name: 'MapView',
      component: MapView
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView
    },
    {
      path: '/recommend',
      name: 'RecommendView',
      component: RecommendView,
      meta: { 
        requiresAuth: true  // 인증 필요 표시
      }
    },
    {
      path: '/search',
      name: 'SearchView',
      component: SearchView
    },
    {
      path: '/password',
      name: 'PasswordView',
      component: Password
    },
    {
      path: '/find_password',
      name: 'find_password',
      component: FindPassword
    },
    {
      path: '/boards',
      name: 'MainBoard',
      component: MainBoard
    },
    {
      path: '/boards/board1',
      name: 'Board1',
      component: Board1
    },
    {
      path: '/boards/board2',
      name: 'Board2',
      component: Board2
    },
    {
      path: '/boards/board3',
      name: 'Board3',
      component: Board3
    },
    {
      path: '/boards/:boardType/create',
      name: 'BoardCreateView',
      component: BoardCreateView,
      props: { mode: 'create' }  // create 모드로 설정
    },
    {
      path: '/boards/:boardType/:id/edit',  // 수정 경로 추가
      name: 'BoardEditView',
      component: BoardCreateView,  // 같은 컴포넌트 사용
      props: { mode: 'edit' }      // edit 모드로 설정
    },
    {
      path: '/boards/:boardType/:id',
      name: 'BoardDetailView',
      component: BoardDetailView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({
        name: 'LogInView',  // 로그인 페이지의 name
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
 })

// router.beforeEach((to, from) => {
//   const store = useCounterStore()
//   // 만약 이동하는 목적지가 메인 페이지이면서
//   // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
//   if (to.name === 'ArticleView' && !store.isLogin) {
//     window.alert('로그인이 필요합니다.')
//     return { name: 'LogInView' }
//   }

//   // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
//   // 메인 페이지로 보냄
//   if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
//     window.alert('이미 로그인 되어있습니다.')
//     return { name: 'ArticleView' }
//   }
// })

export default router
