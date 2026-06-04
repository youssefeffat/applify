<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Navigation from './components/Navigation.vue'
import ToastContainer from './components/ToastContainer.vue'
import { useAppStore } from './store/useAppStore.js'

const route = useRoute()
const store = useAppStore()

// Fetch user on app startup so store.user is always populated after page refresh
onMounted(async () => {
  if (store.isAuthenticated) {
    await store.fetchUser()
  }
})
</script>

<template>
  <div class="app-container">
    <Navigation v-if="route.name !== 'login' && route.name !== 'onboarding'" />
    <RouterView />
    <ToastContainer />
  </div>
</template>
