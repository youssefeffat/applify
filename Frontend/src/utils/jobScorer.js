/**
 * Hybrid job matching engine.
 *
 * Strategy:
 *   - When profile data EXISTS for a dimension → real weighted calculation
 *   - When profile data is MISSING → deterministic per-job value (hash-based)
 *     so each job always shows the same unique score without real data.
 *
 * Score breakdown (100 pts total):
 *   Skills  : 0–40 (job tags vs user skills)
 *   Role    : 0–30 (job title vs target_roles)
 *   Type    : 0–15 (employment/contract type vs preferences)
 *   Location: 0–15 (job location vs user location)
 *
 * Final output clamped to [42, 97] so scores always feel realistic.
 */

// ─── Utilities ────────────────────────────────────────────────────────────────

/** Fast deterministic 32-bit hash of any string */
function hash32(str) {
  let h = 2166136261 >>> 0
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i)
    h = Math.imul(h, 16777619) >>> 0
  }
  return h
}

/**
 * Deterministic float [0, 1) from a seed + offset combo.
 * Different offsets give independent pseudo-random streams.
 */
function detFloat(seed, offset) {
  const v = Math.sin(seed * 127.1 + offset * 311.7) * 43758.5453
  return Math.abs(v - Math.floor(v))
}

/** Deterministic integer in [min, max] */
function detInt(seed, offset, min, max) {
  return min + Math.floor(detFloat(seed, offset) * (max - min + 1))
}

const normalize = (s) => (s || '').toLowerCase().replace(/[^a-z0-9\s+#]/g, '').trim()
const tokenize = (s) => normalize(s).split(/[\s,;/]+/).filter(Boolean)
const anyOverlap = (a, b) => a.some((x) => b.some((y) => y.includes(x) || x.includes(y)))

// ─── Main export ──────────────────────────────────────────────────────────────

/**
 * @param {Object} job
 * @param {Object|null} user
 * @returns {{ score: number, isRecommended: boolean, shouldDisplay: boolean,
 *             matchedSkills: string[], matchDetails: Object, hasRealData: boolean }}
 */
export function calculateJobMatch(job, user) {
  const jobSeed = hash32(String(job?.id ?? ''))

  // ── No job object ────────────────────────────────────────────────────────────
  if (!job) return { score: 50, isRecommended: false, shouldDisplay: true, matchedSkills: [], matchDetails: {}, hasRealData: false }

  // ── No user yet ─────────────────────────────────────────────────────────────
  if (!user) {
    const score = detInt(jobSeed, 0, 52, 91)
    return {
      score,
      isRecommended: score >= 72,
      shouldDisplay: true,
      matchedSkills: [],
      matchDetails: {},
      hasRealData: false
    }
  }

  const jobPrefs = user.job_preferences || {}
  const profBg   = user.professional_background || {}

  // ── Detect which profile dimensions are actually filled ──────────────────────
  const userSkillsRaw   = (profBg.skills || '') + ' ' + (profBg.soft_skills || '')
  const userSkillTokens = tokenize(userSkillsRaw)
  const hasSkills       = userSkillTokens.length > 0

  const targetRoles     = (jobPrefs.target_roles || []).map(normalize)
  const hasRoles        = targetRoles.length > 0

  const preferredTypes  = (jobPrefs.employment_types || []).map(normalize)
  const hasTypes        = preferredTypes.length > 0

  const userLocationNorm = normalize(user.location || '')
  const hasLocation      = userLocationNorm.length > 2

  // ── Job data ─────────────────────────────────────────────────────────────────
  const jobTags         = (job.tags || []).map(normalize)
  const jobTitleNorm    = normalize(job.title || '')
  const jobTitleTokens  = tokenize(job.title || '')
  const jobEmpType      = normalize(job.employment_type || '')
  const jobContractType = normalize(job.contract_type || '')
  const jobLocationNorm = normalize(job.location || '')
  const jobIsRemote     = jobEmpType.includes('remote') || jobLocationNorm.includes('remote')

  const hasRealData = hasSkills || hasRoles || hasTypes || hasLocation

  // ─── DIMENSION 1: SKILLS (0–40) ──────────────────────────────────────────────
  let skillScore
  const matchedSkillsRaw = []

  if (hasSkills && jobTags.length > 0) {
    let hits = 0
    for (const tag of jobTags) {
      const tagToks = tokenize(tag)
      if (anyOverlap(tagToks, userSkillTokens) || anyOverlap(userSkillTokens, tagToks)) {
        hits++
        matchedSkillsRaw.push(tag)
      }
    }
    skillScore = (hits / jobTags.length) * 40
  } else if (!hasSkills) {
    // Vary by job: more tags → higher base (richer posting)
    const tagBonus = Math.min(jobTags.length * 2, 12)
    skillScore = detInt(jobSeed, 1, 10, 28) + tagBonus
  } else {
    skillScore = 20 // no tags on job
  }

  // ─── DIMENSION 2: ROLE (0–30) ────────────────────────────────────────────────
  let roleScore

  if (hasRoles) {
    roleScore = 0
    for (const role of targetRoles) {
      const roleToks = tokenize(role)
      const overlap  = roleToks.filter((t) => jobTitleTokens.includes(t))
      if (overlap.length > 0) {
        roleScore = Math.max(roleScore, (overlap.length / Math.max(roleToks.length, jobTitleTokens.length)) * 30)
      }
      if (anyOverlap(roleToks, jobTags)) roleScore = Math.max(roleScore, 14)
      if (roleToks.some((t) => jobTitleNorm.includes(t))) roleScore = Math.max(roleScore, 20)
    }
  } else {
    roleScore = detInt(jobSeed, 2, 8, 26)
  }

  // ─── DIMENSION 3: EMPLOYMENT TYPE (0–15) ────────────────────────────────────
  let typeScore

  if (hasTypes) {
    const jobTypeStr = [jobEmpType, jobContractType].join(' ')
    typeScore = preferredTypes.some((t) => jobTypeStr.includes(t) || t.includes(jobTypeStr)) ? 15 : 2
  } else {
    // Remote jobs get a slight bump (globally desirable)
    typeScore = jobIsRemote ? detInt(jobSeed, 3, 9, 15) : detInt(jobSeed, 3, 5, 13)
  }

  // ─── DIMENSION 4: LOCATION (0–15) ────────────────────────────────────────────
  let locationScore

  if (hasLocation) {
    if (jobIsRemote) {
      const userWantsRemote = preferredTypes.some((t) => t.includes('remote'))
      locationScore = userWantsRemote ? 15 : 11
    } else {
      const userCity = userLocationNorm.split(',')[0].trim()
      const jobCity  = jobLocationNorm.split(',')[0].trim()
      locationScore  =
        userCity.length > 2 && (jobLocationNorm.includes(userCity) || userLocationNorm.includes(jobCity))
          ? 15
          : 4
    }
  } else {
    locationScore = jobIsRemote ? detInt(jobSeed, 4, 10, 15) : detInt(jobSeed, 4, 4, 12)
  }

  // ─── Final score ─────────────────────────────────────────────────────────────
  const rawScore = skillScore + roleScore + typeScore + locationScore

  // Clamp to [42, 97] — feel realistic, avoid extremes
  const score = Math.round(Math.min(97, Math.max(42, rawScore)))

  return {
    score,
    isRecommended: score >= 72,
    shouldDisplay: true,
    matchedSkills: matchedSkillsRaw,
    matchDetails: {
      skills:   Math.round(skillScore),
      role:     Math.round(roleScore),
      type:     Math.round(typeScore),
      location: Math.round(locationScore)
    },
    hasRealData
  }
}
