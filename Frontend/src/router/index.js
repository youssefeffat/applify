import { createRouter, createWebHistory } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'

import LoginView from '../views/LoginView.vue'
import OnboardingView from '../views/OnboardingView.vue'
import JobExplorerView from '../views/JobExplorerView.vue'
import JobDetailView from '../views/JobDetailView.vue'
import ApplicationTrackerView from '../views/ApplicationTrackerView.vue'
import DashboardView from '../views/DashboardView.vue'
import ProfileView from '../views/ProfileView.vue'
import JobPreferencesView from '../views/JobPreferencesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView,
      meta: { requiresAuth: true }
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: JobExplorerView,
      meta: { requiresAuth: true }
    },
    {
      path: '/jobs/:id',
      name: 'job-detail',
      component: JobDetailView,
      meta: { requiresAuth: true }
    },
    {
      path: '/tracker',
      name: 'tracker',
      component: ApplicationTrackerView,
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/preferences',
      name: 'preferences',
      component: JobPreferencesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/',
      redirect: '/jobs'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const store = useAppStore()
  if (to.meta.requiresAuth && !store.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && store.isAuthenticated) {
    next({ name: 'jobs' })
  } else {
    next()
  }
})

export default router
