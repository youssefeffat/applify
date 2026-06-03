import apiClient from './client'

export default {
  getJobs(params) {
    return apiClient.get('/jobs', { params })
  },
  getJobById(jobId) {
    return apiClient.get(`/jobs/${jobId}`)
  }
}
