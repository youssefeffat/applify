<script setup>
import { computed } from 'vue'
import { useAppStore } from '../store/useAppStore.js'

const props = defineProps({
  job: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const store = useAppStore()

const application = computed(() => store.savedJobs.find(j => j.job_id === props.job.id))
const isSaved = computed(() => !!application.value)
const isApplied = computed(() => application.value?.status === 'Applied')

const scoreColor = computed(() => {
  if (!props.job.score) return 'var(--text-light)'
  if (props.job.score >= 75) return '#10b981' // Green
  if (props.job.score >= 45) return '#f59e0b' // Yellow
  return '#ef4444' // Red
})

const toggleSave = async () => {
  if (isApplied.value) return // Cannot unsave if applied
  
  if (isSaved.value) {
    await store.removeJob(props.job.id)
  } else {
    await store.saveJob(props.job, 'Saved')
  }
}

const toggleApply = async () => {
  if (isApplied.value) return // Cannot un-apply
  await store.markApplied(props.job)
}
</script>

<template>
  <div class="job-card" @click="$emit('click', job)" style="position: relative;">
    <div v-if="job.recommended" style="position: absolute; top: -10px; left: -10px; background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 10;">
      ✨ Recommended
    </div>
    <div v-if="job.score !== undefined" style="position: absolute; top: 1rem; right: 1rem; font-weight: 700; font-size: 0.8rem; padding: 0.25rem 0.6rem; border-radius: 1rem; background: white; border: 2px solid" :style="{ borderColor: scoreColor, color: scoreColor }">
      {{ job.score }}% Match
    </div>
    <div class="job-card-header" style="padding-right: 4.5rem;">
      <h3 class="job-card-title">{{ job.title }}</h3>
      <p class="job-card-company">{{ job.company }}</p>
    </div>
    
    <div class="job-card-location">
      <span>📍</span>
      <span>{{ job.location }}</span>
    </div>
    
    <div class="job-card-tags">
      <span v-if="job.employment_type" class="job-tag" :class="job.employment_type === 'remote' ? 'job-tag-remote' : ''">
        {{ job.employment_type.charAt(0).toUpperCase() + job.employment_type.slice(1) }}
      </span>
      <span v-if="job.contract_type" class="job-tag job-tag-contract">
        {{ job.contract_type.charAt(0).toUpperCase() + job.contract_type.slice(1) }}
      </span>
      <span v-for="(tag, index) in job.tags" :key="index" class="job-tag">
        {{ tag }}
      </span>
    </div>

    <!-- Quick Actions Icons -->
    <div style="position: absolute; bottom: 1.2rem; right: 1.2rem; display: flex; gap: 0.5rem; z-index: 10;">
      <button 
        @click.stop="isApplied ? null : toggleSave()" 
        style="background: white; border: 1px solid var(--border-gray); border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;"
        :style="{ borderColor: isSaved ? '#ef4444' : 'var(--border-gray)', opacity: isApplied ? '0.5' : '1', cursor: isApplied ? 'not-allowed' : 'pointer' }"
        title="Save Job"
      >
        <span v-if="isSaved" style="color: #ef4444; font-size: 1.1rem; line-height: 1;">❤️</span>
        <span v-else style="color: var(--text-light); font-size: 1.1rem; line-height: 1;">🤍</span>
      </button>
      
      <button 
        @click.stop="isApplied ? null : toggleApply()" 
        style="background: white; border: 1px solid var(--border-gray); border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;"
        :style="{ borderColor: isApplied ? '#10b981' : 'var(--border-gray)', cursor: isApplied ? 'not-allowed' : 'pointer' }"
        title="Mark as Applied"
      >
        <span v-if="isApplied" style="color: #10b981; font-size: 1rem; line-height: 1;">✅</span>
        <span v-else style="color: var(--text-light); font-size: 1.1rem; line-height: 1;">📤</span>
      </button>
    </div>
  </div>
</template>
