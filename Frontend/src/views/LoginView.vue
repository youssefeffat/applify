<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import { useToast } from '../store/useToast.js'

const router = useRouter()
const store = useAppStore()
const { addToast } = useToast()

const isLogin = ref(true)
const email = ref('')
const password = ref('')

const handleSubmit = async () => {
  try {
    if (!isLogin.value) {
      await store.register({ email: email.value, password: password.value })
      router.push('/onboarding')
    } else {
      await store.login({ email: email.value, password: password.value })
      router.push('/jobs')
    }
  } catch (err) {
    const errorMsg = err.response?.data?.detail || err.message
    addToast("Authentication failed: " + errorMsg, 'error')
    console.error(err)
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">Applify</h1>
        <p class="auth-subtitle">
          {{ isLogin ? 'Welcome back! Sign in to continue' : 'Create an account to get started' }}
        </p>
      </div>

      <div class="auth-toggle">
        <button
          class="auth-toggle-btn"
          :class="{ active: isLogin }"
          @click="isLogin = true"
        >
          Log In
        </button>
        <button
          class="auth-toggle-btn"
          :class="{ active: !isLogin }"
          @click="isLogin = false"
        >
          Create Account
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label" for="email">Email Address</label>
          <input
            id="email"
            type="email"
            class="form-input"
            placeholder="you@example.com"
            v-model="email"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="password">Password</label>
          <input
            id="password"
            type="password"
            class="form-input"
            placeholder="••••••••"
            v-model="password"
            required
            minlength="8"
          />
        </div>

        <button type="submit" class="btn btn-primary btn-block btn-lg">
          {{ isLogin ? 'Sign In' : 'Create Account' }}
        </button>
      </form>
    </div>
  </div>
</template>
