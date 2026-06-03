<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import StatusSelect from '../components/StatusSelect.vue'
import TrackerCardSkeleton from '../components/TrackerCardSkeleton.vue'

const store = useAppStore()
const router = useRouter()
const isLoading = ref(true)

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

const jobsByStatus = (status) => {
  return savedJobs.value.filter(job => job.status === status)
}

const handleStatusChange = (jobId, newStatus) => {
  store.updateJobStatus(jobId, newStatus)
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
              
              <div v-if="col.id === 'Interviews'" style="margin: 0.5rem 0; padding: 0.5rem; background-color: var(--primary-blue-light); border-radius: var(--radius-sm); font-size: 0.85rem;">
                <div style="font-weight: 600; color: var(--primary-blue-dark); margin-bottom: 0.25rem;">📅 Next Interview</div>
                <input type="date" class="form-input" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; width: 100%;" @click.stop @change="(e) => store.updateJobStatus(job.id, job.status, e.target.value)" :value="job.interview_date ? job.interview_date.split('T')[0] : ''" />
              </div>

              <div class="tracker-job-actions">
                <select class="status-select" :value="job.status" @change="(e) => handleStatusChange(job.id, e.target.value)" @click.stop>
                  <option v-for="c in columns" :key="c.id" :value="c.id">{{ c.title }}</option>
                </select>
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
