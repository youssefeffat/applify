<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import StatusSelect from '../components/StatusSelect.vue'
import TrackerCardSkeleton from '../components/TrackerCardSkeleton.vue'

const store = useAppStore()
const router = useRouter()
const isLoading = ref(true)
const dateSaveStatus = ref({}) // { [jobId]: 'saving' | 'saved' | 'error' }

onMounted(async () => {
  isLoading.value = true
  await store.fetchSavedJobs()
  isLoading.value = false
})

const savedJobs = computed(() => store.savedJobs)

const columns = [
  { id: 'Saved', title: 'Saved Jobs' },
  { id: 'Applied', title: 'Applied' },
  { id: 'Interviews', title: 'Interviews' },
  { id: 'Accepted', title: 'Accepted' },
  { id: 'Rejected', title: 'Rejected' }
]

// Returns only statuses that come AFTER the current one (no going back)
const availableStatuses = (currentStatus) => {
  if (currentStatus === 'Accepted' || currentStatus === 'Rejected') return []
  const currentIndex = columns.findIndex(c => c.id === currentStatus)
  if (currentIndex === -1) return columns
  return columns.slice(currentIndex + 1)
}

const jobsByStatus = (status) => {
  return savedJobs.value.filter(job => job.status === status)
}

const handleStatusChange = (jobId, newStatus) => {
  store.updateJobStatus(jobId, newStatus)
}

const handleDateChange = async (jobId, dateValue) => {
  if (!dateValue) return
  dateSaveStatus.value[jobId] = 'saving'
  const ok = await store.updateInterviewDate(jobId, dateValue)
  dateSaveStatus.value[jobId] = ok ? 'saved' : 'error'
  setTimeout(() => { delete dateSaveStatus.value[jobId] }, 2000)
}

const handleViewJob = (job) => {
  router.push(`/jobs/${job.id}`)
}
</script>

<template>
  <div class="page-container-wide">
    <div class="tracker-header">
      <h1 class="tracker-title">Application Tracker</h1>
    </div>
    
    <div class="tracker-columns">
      <div v-for="col in columns" :key="col.id" class="tracker-column">
        <div class="tracker-column-header">
          <h2 class="tracker-column-title">{{ col.title }}</h2>
          <span class="tracker-column-count">{{ jobsByStatus(col.id).length }}</span>
        </div>
        
        <div class="tracker-job-list">
          <template v-if="isLoading">
            <TrackerCardSkeleton v-for="n in 2" :key="n" />
          </template>
          <template v-else>
            <div 
              v-for="job in jobsByStatus(col.id)" 
              :key="job.id" 
              class="tracker-job-card"
              @click="handleViewJob(job)"
              style="cursor: pointer;"
            >
              <div class="tracker-job-title">{{ job.title }}</div>
              <div class="tracker-job-company">{{ job.company }}</div>
              
              <div v-if="col.id === 'Interviews'" style="margin: 0.5rem 0; padding: 0.5rem; background-color: var(--primary-blue-light); border-radius: var(--radius-sm); font-size: 0.85rem;" @click.stop>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                  <span style="font-weight: 600; color: var(--primary-blue-dark);">📅 Next Interview</span>
                  <span v-if="dateSaveStatus[job.id] === 'saving'" style="font-size: 0.75rem; color: var(--text-medium);">Saving...</span>
                  <span v-else-if="dateSaveStatus[job.id] === 'saved'" style="font-size: 0.75rem; color: var(--success-green); font-weight: 600;">✓ Saved</span>
                  <span v-else-if="dateSaveStatus[job.id] === 'error'" style="font-size: 0.75rem; color: var(--danger-red); font-weight: 600;">✗ Error</span>
                </div>
                <input
                  type="date"
                  class="form-input"
                  style="padding: 0.25rem 0.5rem; font-size: 0.8rem; width: 100%;"
                  @click.stop
                  @change="(e) => handleDateChange(job.id, e.target.value)"
                  :value="job.interview_date ? job.interview_date.split('T')[0] : ''"
                />
              </div>

              <div class="tracker-job-actions">
                <select
                  v-if="availableStatuses(job.status).length > 0"
                  class="status-select"
                  :value="job.status"
                  @change="(e) => handleStatusChange(job.id, e.target.value)"
                  @click.stop
                >
                  <option disabled :value="job.status">{{ columns.find(c => c.id === job.status)?.title }} (actuel)</option>
                  <option v-for="c in availableStatuses(job.status)" :key="c.id" :value="c.id">→ {{ c.title }}</option>
                </select>
                <div v-else-if="job.status === 'Accepted'" style="margin-top: 0.5rem; padding: 0.35rem 0.5rem; border-radius: 4px; background-color: rgba(16, 185, 129, 0.1); color: var(--success-green, #10b981); font-weight: 600; font-size: 0.85rem; display: inline-block;">
                  ✓ Accepted
                </div>
                <div v-else-if="job.status === 'Rejected'" style="margin-top: 0.5rem; padding: 0.35rem 0.5rem; border-radius: 4px; background-color: rgba(239, 68, 68, 0.1); color: var(--danger-red, #ef4444); font-weight: 600; font-size: 0.85rem; display: inline-block;">
                  ✗ Rejected
                </div>
                <span v-else class="status-final-badge">✓ Final</span>
              </div>
            </div>
            
            <div v-if="jobsByStatus(col.id).length === 0" style="text-align: center; color: var(--text-light); padding: 2rem 0; font-size: 0.9rem;">
              No jobs in this stage.
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>
