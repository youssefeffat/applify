import apiClient from './client'

export default {
  parseCV(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/ai/parse-cv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  councilChat(data) {
    return apiClient.post('/ai/council-chat', data)
  },
  suggestRoles(data) {
    return apiClient.post('/ai/suggest-roles', data)
  },
  generateCustomCV(data) {
    return apiClient.post('/ai/generate-custom-cv', data)
  }
}
