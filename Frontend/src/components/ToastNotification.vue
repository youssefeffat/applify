<script setup>
import { computed } from 'vue'
const props = defineProps({
  toast: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['close'])

const typeClass = computed(() => {
  switch(props.toast.type) {
    case 'success': return 'toast-success'
    case 'error': return 'toast-error'
    default: return 'toast-info'
  }
})

const icon = computed(() => {
  switch(props.toast.type) {
    case 'success': return '✅'
    case 'error': return '❌'
    default: return 'ℹ️'
  }
})
</script>
<template>
  <div class="toast-notification" :class="typeClass">
    <span class="toast-icon">{{ icon }}</span>
    <span class="toast-message" v-html="toast.message"></span>
    <button class="toast-close" @click="$emit('close', toast.id)">&times;</button>
  </div>
</template>
<style scoped>
.toast-notification {
  display: flex;
  align-items: center;
  padding: 1rem 1.2rem;
  margin-top: 0.75rem;
  background: white;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  min-width: 300px;
  max-width: 450px;
  pointer-events: auto;
  border-left: 4px solid var(--primary-blue);
}
.toast-success { border-left-color: #10b981; }
.toast-error { border-left-color: #ef4444; }
.toast-icon { margin-right: 0.75rem; font-size: 1.25rem; }
.toast-message { flex: 1; font-weight: 500; font-size: 0.95rem; color: var(--text-dark); line-height: 1.4; }
.toast-close { background: none; border: none; font-size: 1.5rem; color: var(--text-light); cursor: pointer; margin-left: 1rem; line-height: 1; padding: 0; transition: color 0.2s; }
.toast-close:hover { color: var(--text-dark); }
</style>
