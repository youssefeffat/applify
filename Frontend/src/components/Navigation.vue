<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'

const route = useRoute()
const store = useAppStore()

</script>

<template>
  <nav class="main-nav">
    <div class="nav-content">
      <router-link to="/jobs" class="nav-logo">Applify</router-link>
      
      <ul class="nav-links">
        <li>
          <router-link 
            to="/jobs" 
            class="nav-link" 
            active-class="active">
            Explore Jobs
          </router-link>
        </li>
        <li>
          <router-link 
            to="/tracker" 
            class="nav-link" 
            active-class="active">
            Tracker
          </router-link>
        </li>
        <li>
          <router-link 
            to="/dashboard" 
            class="nav-link" 
            active-class="active">
            Dashboard
          </router-link>
        </li>
        <li>
          <router-link 
            to="/profile" 
            class="nav-link" 
            active-class="active">
            Profile
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>
