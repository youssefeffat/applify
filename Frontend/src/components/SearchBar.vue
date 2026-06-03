<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Search jobs, companies, or keywords...'
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="search-bar">
    <input 
      type="text" 
      class="search-input" 
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    >
    <span class="search-icon">🔍</span>
  </div>
</template>
