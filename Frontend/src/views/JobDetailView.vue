<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import jobsAPI from '../api/jobs'
import { useToast } from '../store/useToast.js'

const route = useRoute()
const router = useRouter()
const store = useAppStore()
const { addToast } = useToast()

const job = ref(null)
const isLoading = ref(true)

onMounted(async () => {
  const jobId = route.params.id
  isLoading.value = true
  try {
    const { data } = await jobsAPI.getJobById(jobId)
    job.value = data
  } catch (err) {
    console.error("Failed to fetch job", err)
    addToast("Job not found!", 'error')
    router.push('/jobs')
  } finally {
    isLoading.value = false
  }
})

const application = computed(() => store.savedJobs.find(j => j.job_id === job.value?.id))
const isSaved = computed(() => !!application.value)
const isApplied = computed(() => application.value?.status === 'Applied')

const handleSaveJob = async () => {
  if (isApplied.value) return // cannot change save status if applied
  
  if (isSaved.value) {
    const success = await store.removeJob(job.value.id)
    if (success) {
      addToast(`${job.value.title} removed from your tracker.`, 'info')
    } else {
      addToast('Failed to remove job.', 'error')
    }
  } else {
    const success = await store.saveJob(job.value)
    if (success) {
      addToast(`${job.value.title} has been saved to your tracker!`, 'success')
    } else {
      addToast('Failed to save job.', 'error')
    }
  }
}

const handleDirectApply = async () => {
  if (isApplied.value) return
  await store.markApplied(job.value)
  addToast(`Application submitted successfully for ${job.value.title}!`, 'success')
}
</script>

<template>
  <div class="page-container job-detail-page">
    <button class="btn btn-outline" style="margin-bottom: 1.5rem;" @click="router.back()">
      ← Back to Jobs
    </button>
    
    <div v-if="isLoading">
      <!-- Skeleton layout for Job Details -->
      <div style="margin-bottom: 2rem;">
        <div style="height: 2.5rem; width: 60%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1rem;" class="pulse"></div>
        <div style="height: 1.5rem; width: 30%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1.5rem;" class="pulse"></div>
        <div style="display: flex; gap: 1rem;">
          <div style="height: 30px; width: 100px; background: #e2e8f0; border-radius: 15px;" class="pulse"></div>
          <div style="height: 30px; width: 100px; background: #e2e8f0; border-radius: 15px;" class="pulse"></div>
        </div>
      </div>
      
      <div style="margin-bottom: 2rem;">
        <div style="height: 1.5rem; width: 40%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1rem;" class="pulse"></div>
        <div style="height: 1rem; width: 100%; background: #e2e8f0; border-radius: 4px; margin-bottom: 0.5rem;" class="pulse"></div>
        <div style="height: 1rem; width: 95%; background: #e2e8f0; border-radius: 4px; margin-bottom: 0.5rem;" class="pulse"></div>
        <div style="height: 1rem; width: 85%; background: #e2e8f0; border-radius: 4px;" class="pulse"></div>
      </div>
    </div>
    
    <template v-else-if="job">
      <div class="job-detail-header">
        <h1 class="job-detail-title">{{ job.title }}</h1>
        <div class="job-detail-company">{{ job.company }}</div>
        
        <div class="job-detail-meta">
          <div class="job-detail-meta-item">📍 {{ job.location }}</div>
          <div v-if="job.contract_type" class="job-detail-meta-item">💼 {{ job.contract_type }}</div>
          <div v-if="job.employment_type" class="job-detail-meta-item">🏠 {{ job.employment_type }}</div>
        </div>
        
        <div class="job-card-tags">
          <span v-for="tag in job.tags" :key="tag" class="job-tag">{{ tag }}</span>
        </div>
      </div>
      
      <div class="job-detail-content">
        <div class="job-detail-section">
          <h3>About the Role</h3>
          <p>{{ job.description }}</p>
          <p v-if="!job.description">No detailed description provided for this position.</p>
        </div>
        <div class="job-detail-section">
          <h3>Requirements</h3>
          <ul>
            <li>3+ years of relevant experience</li>
            <li>Strong communication skills</li>
            <li>Ability to work independently</li>
          </ul>
        </div>
      </div>
      
      <div class="sticky-action-bar">
        <div class="sticky-action-content">
          <button class="btn" :class="isSaved && !isApplied ? 'btn-secondary' : 'btn-primary'" @click="handleSaveJob" :disabled="isApplied" :style="{ opacity: isApplied ? '0.5' : '1', cursor: isApplied ? 'not-allowed' : 'pointer' }">
            {{ isApplied ? 'Saved (Applied)' : (isSaved ? 'Unsave Job' : 'Save Job') }}
          </button>
          <button class="btn" :class="isApplied ? 'btn-success' : 'btn-success'" @click="handleDirectApply" :disabled="isApplied" :style="{ opacity: isApplied ? '0.7' : '1', cursor: isApplied ? 'not-allowed' : 'pointer' }">
            {{ isApplied ? '✅ Applied' : '✅ Apply' }}
          </button>
          <button class="btn btn-primary" @click="handleGenerateCV">✨ Generate Customized CV</button>
        </div>
      </div>
    </template>
  </div>
</template>

<style>
.pulse {
  animation: pulse 1.5s infinite ease-in-out;
}
@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 0.3; }
  100% { opacity: 0.7; }
}
</style>
