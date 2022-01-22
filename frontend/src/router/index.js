import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from '@/store/index.js'
import { authorization, refreshToken } from "@/api/index.js";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/ResultList.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/userprofile',
    name: 'userprofile',
    component: () => import('../views/UserProfile.vue')
  },
  {
    path: '/activate',
    name: 'activate',
    component: () => import('../views/activate.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
// 注册全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 动态设置title
  // to.meta && setTitle(to.meta.title)
  // 获取token
  console.log()
  const access = store.state.Jwt.access || ''
  const refresh = store.state.Jwt.refresh || ''

  if (access) { // 已登录
    console.log("已经登录:", access)
    // 调用接口判断access是否失效
    let res = await authorization(access).then((data) => data).catch((err) => err)
    let code = res.status || ''
    if (code == 200) {
      if (to.name === 'login') next({ name: 'Home' })
      else next()
    } else {
      // 失效就使用刷新token
      console.log("使用刷新token")
      let res = await refreshToken(refresh).then((data) => data).catch((err) => err)
      let code = res.status || ''
      if (code == 200) {
        console.log("刷新成功...")
        store.commit('SetJwt', { "access": res.data.access, "refresh": refresh })
      } else {
        store.commit('SetJwt', '')
        next({ name: 'login' })
      }
    }
  } else { // 未登录
    // 如果去的页面是登陆页，直接跳到登陆页
    if (to.name != 'userprofile') next()
    // 如果不是登陆页，强行跳转到登陆页
    else next({ name: 'login' })
  }
})

export default router
