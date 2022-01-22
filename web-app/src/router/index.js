import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from "../store";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/posts',
    name: 'Posts',
    component: () => import('../views/Post.vue')
  },
  {
    path: '/users',
    name: 'User',
    component: () => import('../views/User.vue')
  },
  {
    path: '/post/:id',
    name: "DetailPost",
    component: () => import('../views/DetailPost')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !store.state.auth.isAuthenticated) {
    next({ name: 'Login'})
  } else if(to.name === 'Login' && store.state.auth.isAuthenticated) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
