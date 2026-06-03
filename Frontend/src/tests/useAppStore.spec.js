import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAppStore } from '../store/useAppStore'
import authAPI from '../api/auth'
import usersAPI from '../api/users'

// Mock API modules
vi.mock('../api/auth', () => ({
  default: {
    login: vi.fn(),
    logout: vi.fn(),
    register: vi.fn()
  }
}))

vi.mock('../api/users', () => ({
  default: {
    getMe: vi.fn()
  }
}))

describe('useAppStore', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    const store = useAppStore()
    store.isAuthenticated = false
    store.user = null
    store.savedJobs = []
  })

  it('initializes correctly', () => {
    const store = useAppStore()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBe(null)
    expect(store.savedJobs).toEqual([])
  })

  it('logs in successfully and fetches user', async () => {
    const store = useAppStore()
    authAPI.login.mockResolvedValueOnce({ data: { access_token: 'fake-token' } })
    usersAPI.getMe.mockResolvedValueOnce({ data: { id: 1, name: 'John Doe' } })

    const result = await store.login({ email: 'test@test.com', password: 'password' })

    expect(result).toBe(true)
    expect(localStorage.getItem('token')).toBe('fake-token')
    expect(store.isAuthenticated).toBe(true)
    expect(store.user).toEqual({ id: 1, name: 'John Doe' })
    expect(authAPI.login).toHaveBeenCalledTimes(1)
    expect(usersAPI.getMe).toHaveBeenCalledTimes(1)
  })

  it('logs out and clears state', async () => {
    const store = useAppStore()
    localStorage.setItem('token', 'fake-token')
    store.isAuthenticated = true
    store.user = { id: 1 }
    store.savedJobs = [{ id: 1 }]
    
    authAPI.logout.mockResolvedValueOnce({})

    await store.logout()

    expect(localStorage.getItem('token')).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
    expect(store.savedJobs).toEqual([])
  })
})
