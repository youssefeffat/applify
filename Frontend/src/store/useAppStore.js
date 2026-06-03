import { reactive } from 'vue'
import authAPI from '../api/auth'
import usersAPI from '../api/users'
import trackerAPI from '../api/tracker'
import jobsAPI from '../api/jobs'

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
      return data
    } catch (err) {
      throw err
    }
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
    try {
      // create application on backend
      const { data } = await trackerAPI.createApplication({ job_id: job.id, status })
      // add to local state
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
      if (interviewDate) payload.interview_date = interviewDate

      const { data } = await trackerAPI.updateApplication(appId, payload)
      const jobIndex = state.savedJobs.findIndex(j => j.id === appId)
      if (jobIndex !== -1) {
        state.savedJobs[jobIndex] = { ...state.savedJobs[jobIndex], ...data }
      }
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  },

  async markApplied(job) {
    const app = state.savedJobs.find(j => j.job_id === job.id)
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
