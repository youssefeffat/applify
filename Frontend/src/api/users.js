import apiClient from './client'

export default {
  getMe() {
    return apiClient.get('/users/me')
  },
  updateMe(data) {
    return apiClient.put('/users/me', data)
  }
}
