import { reactive } from 'vue'

const state = reactive({
  toasts: []
})

let toastId = 0

export function useToast() {
  const addToast = (message, type = 'info', duration = 3500) => {
    // Basic deduplication
    if (state.toasts.some(t => t.message === message)) return;

    const id = toastId++
    state.toasts.push({ id, message, type })
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
  }

  const removeToast = (id) => {
    const index = state.toasts.findIndex(t => t.id === id)
    if (index !== -1) {
      state.toasts.splice(index, 1)
    }
  }

  return {
    state,
    addToast,
    removeToast
  }
}
