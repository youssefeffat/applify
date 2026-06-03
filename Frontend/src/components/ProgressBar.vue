<script setup>
defineProps({
  steps: {
    type: Array,
    required: true
  },
  currentStep: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <div class="progress-bar-container">
    <div class="progress-bar-steps">
      <div 
        v-for="(step, index) in steps" 
        :key="index"
        class="progress-bar-step"
        :class="{
          'active': index === currentStep,
          'completed': index < currentStep
        }"
      >
        <div class="progress-bar-circle">
          <span v-if="index < currentStep">✓</span>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <span class="progress-bar-label">{{ step }}</span>
      </div>
    </div>
  </div>
</template>
