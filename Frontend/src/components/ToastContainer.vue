<script setup>
import { useToast } from '../store/useToast'
import ToastNotification from './ToastNotification.vue'

const { state, removeToast } = useToast()
</script>
<template>
  <div class="toast-container">
    <TransitionGroup name="toast-list">
      <ToastNotification 
        v-for="toast in state.toasts" 
        :key="toast.id" 
        :toast="toast"
        @close="removeToast"
      />
    </TransitionGroup>
  </div>
</template>
<style scoped>
.toast-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  pointer-events: none;
}
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
