<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SearchBar from '../components/SearchBar.vue'
import JobCard from '../components/JobCard.vue'
import JobCardSkeleton from '../components/JobCardSkeleton.vue'
import jobsAPI from '../api/jobs'
import { useAppStore } from '../store/useAppStore.js'
import { calculateJobMatch } from '../utils/jobScorer.js'

const router = useRouter()
const store = useAppStore()

const jobs = ref([])
const searchQuery = ref('')
const filterType = ref('')
const filterContract = ref('')
const isLoading = ref(true)
const timeoutId = ref(null)
const abortController = ref(null)

const fetchJobs = async () => {
  if (abortController.value) {
    abortController.value.abort()
  }
  abortController.value = new AbortController()

  isLoading.value = true
  try {
    const params = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (filterType.value) params.mode = filterType.value
    if (filterContract.value) params.contract = filterContract.value
    
    const { data } = await jobsAPI.getJobs(params, { signal: abortController.value.signal })
    const fetchedJobs = data.items || data
    
    // Apply AI scoring based on user profile
    const scoredJobs = fetchedJobs.map(job => {
      const match = calculateJobMatch(job, store.user)
      return {
        ...job,
        score: match.score,
        recommended: match.isRecommended,
        shouldDisplay: match.shouldDisplay
      }
    })
    
    // Filter out jobs that don't match preferences (unless highly recommended) and sort by match score
    jobs.value = scoredJobs
      .filter(j => j.shouldDisplay)
      .sort((a, b) => b.score - a.score)
  } catch (err) {
    if (err.name === 'CanceledError' || err.code === 'ERR_CANCELED') {
      return // Ignore aborted requests
    }
    console.error("Failed to fetch jobs", err)
  } finally {
    if (!abortController.value?.signal.aborted) {
      isLoading.value = false
    }
  }
}

const debouncedFetchJobs = () => {
  if (timeoutId.value) clearTimeout(timeoutId.value)
  timeoutId.value = setTimeout(() => {
    fetchJobs()
  }, 300)
}

watch([searchQuery, filterType, filterContract, () => store.user], () => {
  debouncedFetchJobs()
}, { deep: true })

onMounted(() => {
  fetchJobs()
})

const handleJobClick = (job) => {
  router.push(`/jobs/${job.id}`)
}
</script>

<template>
  <div class="page-container">
    <h1 style="margin-bottom: 2rem; font-size: 2rem; font-weight: 700;">Explore Jobs</h1>
    
    <SearchBar v-model="searchQuery" />
    
    <div class="filters-section">
      <div class="form-group filter-group">
        <label class="form-label">Work Mode</label>
        <select class="form-select" v-model="filterType">
          <option value="">All Modes</option>
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="on-site">On-site</option>
        </select>
      </div>
      <div class="form-group filter-group">
        <label class="form-label">Contract Type</label>
        <select class="form-select" v-model="filterContract">
          <option value="">All Types</option>
          <option value="full-time">Full-time</option>
          <option value="part-time">Part-time</option>
          <option value="contract">Contract</option>
        </select>
      </div>
    </div>
    
    <div class="job-cards-grid">
      <template v-if="isLoading">
        <JobCardSkeleton v-for="n in 6" :key="n" />
      </template>
      <template v-else>
        <JobCard v-for="job in jobs" :key="job.id" :job="job" @click="handleJobClick" />
      </template>
    </div>
    
    <div v-if="!isLoading && jobs.length === 0" style="text-align: center; margin-top: 3rem; color: var(--text-medium);">
      <p>No jobs found matching your criteria.</p>
    </div>
  </div>
</template>
