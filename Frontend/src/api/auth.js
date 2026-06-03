import apiClient from './client'

export default {
  register(data) {
    return apiClient.post('/auth/signup', data)
  },
  login(data) {
    return apiClient.post('/auth/login', data)
  },
  logout() {
    return apiClient.post('/auth/logout')
  }
}
