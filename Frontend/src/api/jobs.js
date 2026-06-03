import apiClient from './client'

/**
 * @typedef {Object} Job
 * @property {number} id
 * @property {string} title
 * @property {string} company
 * @property {string} location
 * @property {string} contract_type
 * @property {string} work_mode
 * @property {string} description
 * @property {string} required_skills
 */

export default {
  /**
   * Fetches jobs with optional filters and cancel signal
   * @param {Object} [params] - Query parameters
   * @param {Object} [config] - Axios request configuration (e.g., signal)
   * @returns {Promise<{data: {items: Job[], total: number} | Job[]}>}
   */
  getJobs(params, config = {}) {
    return apiClient.get('/jobs', { params, ...config })
  },
  
  /**
   * Fetches a single job by ID
   * @param {number|string} jobId 
   * @returns {Promise<{data: Job}>}
   */
  getJobById(jobId) {
    return apiClient.get(`/jobs/${jobId}`)
  }
}
