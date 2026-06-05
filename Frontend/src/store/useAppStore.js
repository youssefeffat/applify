import { reactive } from 'vue'
import authAPI from '../api/auth'
import usersAPI from '../api/users'
import trackerAPI from '../api/tracker'
import jobsAPI from '../api/jobs'
import { calculateJobMatch } from '../utils/jobScorer.js'

/**
 * @typedef {Object} AppState
 * @property {boolean} isAuthenticated
 * @property {Object|null} user
 * @property {Array<import('../api/jobs').Job & {job_id?: number, status?: string}>} savedJobs
 */

/** @type {import('vue').UnwrapNestedRefs<AppState>} */
const state = reactive({
  isAuthenticated: !!localStorage.getItem('token'),
  user: null,
  savedJobs: [],
  /** @type {Map<string, {score:number,isRecommended:boolean,matchedSkills:string[],matchDetails:Object}>} */
  scoreCache: new Map(),
  
  // Actions
  async login(credentials) {
    try {
      const { data } = await authAPI.login(credentials)
      localStorage.setItem('token', data.access_token)
      state.isAuthenticated = true
      await this.fetchUser()
      return true
    } catch (err) {
      throw err
    }
  },

  async register(credentials) {
    try {
      await authAPI.register(credentials)
      return await this.login(credentials) // auto-login after register
    } catch (err) {
      throw err
    }
  },
  
  async logout() {
    try {
      await authAPI.logout()
    } catch (err) {}
    localStorage.removeItem('token')
    state.isAuthenticated = false
    state.user = null
    state.savedJobs = []
  },
  
  async fetchUser() {
    if (!state.isAuthenticated) return null
    try {
      const { data } = await usersAPI.getMe()
      state.user = data
      return data
    } catch (err) {
      console.error(err)
      return null
    }
  },

  async updateUser(userData) {
    try {
      const { data } = await usersAPI.updateMe(userData)
      state.user = data
      // Invalidate score cache when profile changes
      state.scoreCache.clear()
      return data
    } catch (err) {
      throw err
    }
  },

  /**
   * Get a cached match score for a job, computing it if needed.
   * Guarantees the same score is shown everywhere for the same job.
   */
  getJobScore(job) {
    if (!job?.id) return { score: 50, isRecommended: false, matchedSkills: [], matchDetails: {} }
    if (state.scoreCache.has(job.id)) return state.scoreCache.get(job.id)
    const result = calculateJobMatch(job, state.user)
    state.scoreCache.set(job.id, result)
    return result
  },

  /** Clear all cached scores (e.g. after profile update) */
  clearScoreCache() {
    state.scoreCache.clear()
  },

  async fetchSavedJobs() {
    try {
      const { data } = await trackerAPI.getApplications()
      const detailedApps = await Promise.all(data.map(async (app) => {
        try {
          const { data: jobDetails } = await jobsAPI.getJobById(app.job_id)
          return { ...app, title: jobDetails.title, company: jobDetails.company }
        } catch (e) {
          return { ...app, title: 'Unknown Job', company: 'Unknown Company' }
        }
      }))
      state.savedJobs = detailedApps
    } catch (err) {
      console.error(err)
    }
  },

  async removeJob(jobId) {
    const app = state.savedJobs.find(j => j.job_id === jobId)
    if (!app) return false
    try {
      await trackerAPI.deleteApplication(app.id)
      state.savedJobs = state.savedJobs.filter(j => j.id !== app.id)
      return true
    } catch (err) {
      return false
    }
  },
  
  async saveJob(job, status = 'Saved') {
    const LOCKED = ['applied', 'interviewed', 'accepted', 'rejected']
    // Safety: never create a new application if one already exists in a locked status
    const existing = state.savedJobs.find(j => j.job_id === job.id)
    if (existing && LOCKED.includes((existing.status || '').toLowerCase())) return false
    try {
      const { data } = await trackerAPI.createApplication({ job_id: job.id, status })
      if (!state.savedJobs.find(j => j.id === data.id)) {
        state.savedJobs.push({ ...data, title: job.title, company: job.company, jobDetails: job })
      }
      return true
    } catch (err) {
      return false
    }
  },
  
  async updateJobStatus(appId, newStatus, interviewDate = null) {
    try {
      const payload = { status: newStatus }
      if (interviewDate) payload.interview_date = interviewDate + 'T00:00:00'

      const { data } = await trackerAPI.updateApplication(appId, payload)
      const jobIndex = state.savedJobs.findIndex(j => j.id === appId)
      if (jobIndex !== -1) {
        // Explicitly force status to newStatus — don't rely on backend response
        // (backend may return partial data without status field)
        state.savedJobs[jobIndex] = { ...state.savedJobs[jobIndex], ...data, status: newStatus }
      }
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  },

  async updateInterviewDate(appId, dateString) {
    try {
      // Send full ISO datetime string so Pydantic parses it correctly
      const payload = { interview_date: dateString + 'T00:00:00' }
      const { data } = await trackerAPI.updateApplication(appId, payload)
      const jobIndex = state.savedJobs.findIndex(j => j.id === appId)
      if (jobIndex !== -1) {
        state.savedJobs[jobIndex] = { ...state.savedJobs[jobIndex], ...data }
      }
      return true
    } catch (err) {
      console.error('Failed to save interview date:', err)
      return false
    }
  },

  async markApplied(job) {
    const LOCKED = ['applied', 'interviewed', 'accepted', 'rejected']
    const app = state.savedJobs.find(j => j.job_id === job.id)
    // Safety guard: never downgrade a locked status (case-insensitive)
    if (app && LOCKED.includes((app.status || '').toLowerCase())) return false
    if (app) {
      return await this.updateJobStatus(app.id, 'Applied')
    } else {
      return await this.saveJob(job, 'Applied')
    }
  }
})

export function useAppStore() {
  return state
}
