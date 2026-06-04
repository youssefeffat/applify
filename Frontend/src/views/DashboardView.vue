<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '../store/useAppStore.js'

const store = useAppStore()
const savedJobs = computed(() => store.savedJobs)

onMounted(async () => {
  await store.fetchSavedJobs()
})

const SENT_STATUSES = ['Applied', 'Interviews', 'Accepted', 'Rejected']
const totalApplications = computed(() => savedJobs.value.filter(j => SENT_STATUSES.includes(j.status)).length)
const totalSaved = computed(() => savedJobs.value.length)
const totalInterviews = computed(() => savedJobs.value.filter(j => j.status === 'Interviews').length)

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return 'Just now'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}
</script>

<template>
  <div class="page-container">
    <h1 style="margin-bottom: 2rem; font-size: 2rem; font-weight: 700;">Your Dashboard</h1>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-card-label">Total Saved</div>
        <div class="stat-card-value">{{ totalSaved }}</div>
      </div>
      <div class="stat-card stat-card-secondary">
        <div class="stat-card-label">Applications Sent</div>
        <div class="stat-card-value">{{ totalApplications }}</div>
      </div>
      <div class="stat-card stat-card-tertiary">
        <div class="stat-card-label">Interviews</div>
        <div class="stat-card-value">{{ totalInterviews }}</div>
      </div>
    </div>
    
    <div class="application-history-section" style="margin-top: 3rem;">
      <h2 style="font-size: 1.5rem; margin-bottom: 1rem; color: var(--text-dark);">Application History</h2>
      
      <div class="table-container" style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-gray); overflow: hidden; box-shadow: var(--shadow-sm);">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
          <thead style="background-color: var(--bg-light-gray); border-bottom: 2px solid var(--border-gray);">
            <tr>
              <th style="padding: 1rem; font-weight: 600; color: var(--text-medium);">Role</th>
              <th style="padding: 1rem; font-weight: 600; color: var(--text-medium);">Company</th>
              <th style="padding: 1rem; font-weight: 600; color: var(--text-medium);">Status</th>
              <th style="padding: 1rem; font-weight: 600; color: var(--text-medium);">Date Added</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in savedJobs" :key="job.id" style="border-bottom: 1px solid var(--border-gray); transition: background 0.2s;">
              <td style="padding: 1rem; font-weight: 500; color: var(--text-dark);">{{ job.title }}</td>
              <td style="padding: 1rem; color: var(--text-medium);">{{ job.company }}</td>
              <td style="padding: 1rem;">
                <span style="display: inline-block; padding: 0.25rem 0.75rem; border-radius: 2rem; font-size: 0.85rem; font-weight: 500; background-color: var(--primary-blue-light); color: var(--primary-blue-dark);">
                  {{ job.status }}
                </span>
              </td>
              <td style="padding: 1rem; color: var(--text-medium);">{{ formatDate(job.dateAdded) }}</td>
            </tr>
            <tr v-if="savedJobs.length === 0">
              <td colspan="4" style="padding: 2rem; text-align: center; color: var(--text-light);">No applications tracked yet. Start exploring jobs!</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
