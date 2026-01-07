import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/devices',
      name: 'devices',
      component: () => import('../views/DeviceSelectionView.vue'),
    },
    {
      path: '/device/:codename',
      name: 'device',
      component: () => import('../views/DeviceView.vue'),
    },
    {
      path: '/device/:codename/:system',
      name: 'system',
      component: () => import('../views/SystemView.vue'),
    },
    {
      path: '/device/:codename/:system/:version',
      name: 'changelog',
      component: () => import('../views/ChangelogView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

export default router
