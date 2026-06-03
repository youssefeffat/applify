import { describe, it, expect } from 'vitest'
import { calculateJobMatch } from '../utils/jobScorer'

describe('calculateJobMatch', () => {
  it('returns a score of 0 when user or job is null', () => {
    const result1 = calculateJobMatch(null, {})
    const result2 = calculateJobMatch({}, null)
    const result3 = calculateJobMatch(null, null)

    expect(result1.score).toBe(0)
    expect(result2.score).toBe(0)
    expect(result3.score).toBe(0)
    expect(result1.fitsPreferences).toBe(false)
    expect(result1.isRecommended).toBe(false)
    expect(result1.shouldDisplay).toBe(true)
  })

  it('returns a score between 40 and 98 when valid inputs are provided', () => {
    const job = { id: 1, title: 'Developer' }
    const user = { job_preferences: {}, professional_background: {} }
    
    const result = calculateJobMatch(job, user)
    
    expect(result.score).toBeGreaterThanOrEqual(40)
    expect(result.score).toBeLessThanOrEqual(98)
    expect(result.fitsPreferences).toBe(true)
    expect(result.shouldDisplay).toBe(true)
  })
})
