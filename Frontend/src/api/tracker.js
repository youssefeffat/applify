import apiClient from './client'

export default {
  getApplications() {
    return apiClient.get('/applications')
  },
  createApplication(data) {
    return apiClient.post('/applications', data)
  },
  updateApplication(appId, data) {
    return apiClient.patch(`/applications/${appId}`, data)
  },
  deleteApplication(appId) {
    return apiClient.delete(`/applications/${appId}`)
  }
}
