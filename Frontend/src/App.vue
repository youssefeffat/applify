<script setup>
import { useRoute } from 'vue-router'
import Navigation from './components/Navigation.vue'
import ToastContainer from './components/ToastContainer.vue'

const route = useRoute()
</script>

<template>
  <div class="app-container">
    <Navigation v-if="route.name !== 'login' && route.name !== 'onboarding'" />
    <RouterView />
    <ToastContainer />
  </div>
</template>
