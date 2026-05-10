import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomePage.vue')
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLogin.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/join',
    name: 'JoinRoom',
    component: () => import('@/views/JoinRoom.vue')
  },
  {
    path: '/room/:id',
    name: 'ChatRoom',
    component: () => import('@/views/ChatRoom.vue'),
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para rutas protegidas
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'AdminLogin' })
  } else if (to.name === 'AdminLogin' && authStore.isAuthenticated) {
    next({ name: 'AdminDashboard' })
  } else {
    next()
  }
})

export default router