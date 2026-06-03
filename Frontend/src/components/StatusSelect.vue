<script setup>
defineProps({
  modelValue: {
    type: String,
    required: true
  },
  jobId: {
    type: String,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <select 
    class="status-select"
    :value="modelValue"
    @change="$emit('update:modelValue', $event.target.value)"
    @click.stop
  >
    <option value="Saved">Saved</option>
    <option value="Generated CV">Generated CV</option>
    <option value="Applied">Applied</option>
  </select>
</template>
