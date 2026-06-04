<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import jobsAPI from '../api/jobs'
import aiAPI from '../api/ai'
import { useToast } from '../store/useToast.js'

const route = useRoute()
const router = useRouter()
const store = useAppStore()
const { addToast } = useToast()

const job = ref(null)
const isLoading = ref(true)

// Match score — computed from store cache once job is loaded
const matchResult = computed(() => job.value ? store.getJobScore(job.value) : null)
const matchScore = computed(() => matchResult.value?.score ?? null)
const matchColor = computed(() => {
  if (!matchScore.value) return 'var(--text-light)'
  if (matchScore.value >= 75) return '#10b981'
  if (matchScore.value >= 45) return '#f59e0b'
  return '#ef4444'
})

onMounted(async () => {
  const jobId = route.params.id
  isLoading.value = true
  try {
    const { data } = await jobsAPI.getJobById(jobId)
    job.value = data
  } catch (err) {
    console.error("Failed to fetch job", err)
    addToast("Job not found!", 'error')
    router.push('/jobs')
  } finally {
    isLoading.value = false
  }
})

const application = computed(() => store.savedJobs.find(j => j.job_id === job.value?.id))
const isSaved = computed(() => !!application.value)
const isApplied = computed(() => application.value?.status === 'Applied')

const handleSaveJob = async () => {
  if (isApplied.value) return // cannot change save status if applied
  
  if (isSaved.value) {
    const success = await store.removeJob(job.value.id)
    if (success) {
      addToast(`${job.value.title} removed from your tracker.`, 'info')
    } else {
      addToast('Failed to remove job.', 'error')
    }
  } else {
    const success = await store.saveJob(job.value)
    if (success) {
      addToast(`${job.value.title} has been saved to your tracker!`, 'success')
    } else {
      addToast('Failed to save job.', 'error')
    }
  }
}

const handleDirectApply = async () => {
  if (isApplied.value) return
  await store.markApplied(job.value)
  addToast(`Application submitted successfully for ${job.value.title}!`, 'success')
}
const isGeneratingCV = ref(false)

const handleGenerateCV = async () => {
  if (isGeneratingCV.value) return
  isGeneratingCV.value = true

  try {
    // Ensure user profile is loaded
    if (!store.user) await store.fetchUser()
    const user = store.user || {}
    const bg = user.professional_background || {}
    const prefs = user.job_preferences || {}

    const payload = {
      jobInfo: {
        title: job.value.title,
        company: job.value.company,
        location: job.value.location || null,
        description: job.value.description || null,
        tags: job.value.tags || [],
        contract_type: job.value.contract_type || null,
        employment_type: job.value.employment_type || null
      },
      userProfile: {
        first_name: user.first_name || null,
        last_name: user.last_name || null,
        current_title: user.current_title || null,
        github_url: user.github_url || null,
        location: user.location || null,
        education: bg.education || null,
        experience: bg.experience || null,
        skills: bg.skills || null,
        soft_skills: bg.soft_skills || null,
        certificates: bg.certificates || null,
        languages: bg.languages || null,
        long_resume: user.long_resume || null
      }
    }

    const { data } = await aiAPI.generateCustomCV(payload)

    // Trigger HTML download
    const blob = new Blob([data.cvContent], { type: 'text/html;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = data.filename || `CV_${job.value.company}.html`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    addToast('✨ CV generated and downloaded! Open it in your browser then Print → Save as PDF.', 'success')
  } catch (err) {
    console.error('CV generation failed', err)
    addToast('Failed to generate CV. Please try again.', 'error')
  } finally {
    isGeneratingCV.value = false
  }
}
</script>

<template>
  <div class="page-container job-detail-page">
    <button class="btn btn-outline" style="margin-bottom: 1.5rem;" @click="router.back()">
      ← Back to Jobs
    </button>
    
    <div v-if="isLoading">
      <!-- Skeleton layout for Job Details -->
      <div style="margin-bottom: 2rem;">
        <div style="height: 2.5rem; width: 60%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1rem;" class="pulse"></div>
        <div style="height: 1.5rem; width: 30%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1.5rem;" class="pulse"></div>
        <div style="display: flex; gap: 1rem;">
          <div style="height: 30px; width: 100px; background: #e2e8f0; border-radius: 15px;" class="pulse"></div>
          <div style="height: 30px; width: 100px; background: #e2e8f0; border-radius: 15px;" class="pulse"></div>
        </div>
      </div>
      
      <div style="margin-bottom: 2rem;">
        <div style="height: 1.5rem; width: 40%; background: #e2e8f0; border-radius: 4px; margin-bottom: 1rem;" class="pulse"></div>
        <div style="height: 1rem; width: 100%; background: #e2e8f0; border-radius: 4px; margin-bottom: 0.5rem;" class="pulse"></div>
        <div style="height: 1rem; width: 95%; background: #e2e8f0; border-radius: 4px; margin-bottom: 0.5rem;" class="pulse"></div>
        <div style="height: 1rem; width: 85%; background: #e2e8f0; border-radius: 4px;" class="pulse"></div>
      </div>
    </div>
    
    <template v-else-if="job">
      <div class="job-detail-header">
        <h1 class="job-detail-title">{{ job.title }}</h1>
        <div class="job-detail-company">{{ job.company }}</div>
        
        <div class="job-detail-meta">
          <div class="job-detail-meta-item">📍 {{ job.location }}</div>
          <div v-if="job.contract_type" class="job-detail-meta-item">💼 {{ job.contract_type }}</div>
          <div v-if="job.employment_type" class="job-detail-meta-item">🏠 {{ job.employment_type }}</div>
        </div>
        
        <div class="job-card-tags">
          <span v-for="tag in job.tags" :key="tag" class="job-tag">{{ tag }}</span>
        </div>
      </div>
      
      <!-- Match score panel -->
      <div v-if="matchScore !== null" :style="{
        marginBottom:'1.5rem',
        padding:'1.25rem 1.5rem',
        borderRadius:'12px',
        border:'1px solid',
        borderColor: matchResult.isRecommended ? '#bfdbfe' : 'var(--border-gray)',
        background: matchResult.isRecommended ? 'linear-gradient(135deg,#eff6ff,#f0fdf4)' : '#f8fafc'
      }">
        <!-- Row 1: Score + badges + breakdown -->
        <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem">
          <div>
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-light);margin-bottom:4px">
              Profile Match
              <span v-if="!matchResult.hasRealData" style="background:#fef9c3;color:#92400e;border-radius:4px;padding:1px 6px;font-size:0.65rem;margin-left:6px">Estimated</span>
              <span v-else style="background:#dcfce7;color:#166534;border-radius:4px;padding:1px 6px;font-size:0.65rem;margin-left:6px">Based on your profile</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
              <span :style="{fontSize:'2.2rem',fontWeight:900,color:matchColor,lineHeight:1}">{{ matchScore }}%</span>
              <div style="display:flex;flex-direction:column;gap:4px">
                <span v-if="matchResult.isRecommended" style="background:#fef3c7;color:#b45309;border:1px solid #fde68a;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700">✨ Recommended for you</span>
                <span :style="{fontSize:'0.8rem',color:matchColor,fontWeight:600}">
                  {{ matchScore >= 80 ? 'Excellent match' : matchScore >= 65 ? 'Good match' : matchScore >= 50 ? 'Moderate match' : 'Low match' }}
                </span>
              </div>
            </div>
            <!-- Progress bar -->
            <div style="margin-top:10px;height:8px;background:#e2e8f0;border-radius:4px;width:220px;overflow:hidden">
              <div :style="{height:'100%',width:matchScore+'%',background:matchColor,borderRadius:'4px',transition:'width 0.6s ease'}" />
            </div>
          </div>

          <!-- Score breakdown by dimension -->
          <div v-if="matchResult.matchDetails && Object.keys(matchResult.matchDetails).length" style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end">
            <div v-for="(val, key) in matchResult.matchDetails" :key="key"
              style="text-align:center;background:white;border:1px solid #e2e8f0;border-radius:10px;padding:8px 12px;min-width:64px">
              <div :style="{fontSize:'1.15rem',fontWeight:800,color:matchColor}">
                {{ val }}<span style="font-size:0.65rem;opacity:0.6">/{{ key==='skills'?40:key==='role'?30:15 }}</span>
              </div>
              <div style="font-size:0.65rem;text-transform:capitalize;color:var(--text-light);margin-top:2px">{{ key }}</div>
            </div>
          </div>
        </div>

        <!-- Matched skills chips -->
        <div v-if="matchResult.matchedSkills?.length" style="margin-top:12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center">
          <span style="font-size:0.7rem;color:var(--text-light);font-weight:600">✅ Matched skills:</span>
          <span v-for="skill in matchResult.matchedSkills" :key="skill"
            style="background:#ecfdf5;color:#059669;border:1px solid #a7f3d0;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:600"
          >{{ skill }}</span>
        </div>

        <!-- CTA to complete profile -->
        <div v-if="!matchResult.hasRealData" style="margin-top:12px;padding:10px 14px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap">
          <span style="font-size:0.82rem;color:#92400e">💡 Complete your profile to get a precise match score</span>
          <a href="/preferences" style="font-size:0.8rem;color:#2563eb;font-weight:600;text-decoration:none">Update preferences →</a>
        </div>
      </div>

      <div class="job-detail-content">
        <div class="job-detail-section">
          <h3>About the Role</h3>
          <p>{{ job.description }}</p>
          <p v-if="!job.description">No detailed description provided for this position.</p>
        </div>
        <div class="job-detail-section">
          <h3>Requirements</h3>
          <ul>
            <li>3+ years of relevant experience</li>
            <li>Strong communication skills</li>
            <li>Ability to work independently</li>
          </ul>
        </div>
      </div>
      
      <div class="sticky-action-bar">
        <div class="sticky-action-content">
          <button class="btn" :class="isSaved && !isApplied ? 'btn-secondary' : 'btn-primary'" @click="handleSaveJob" :disabled="isApplied" :style="{ opacity: isApplied ? '0.5' : '1', cursor: isApplied ? 'not-allowed' : 'pointer' }">
            {{ isApplied ? 'Saved (Applied)' : (isSaved ? 'Unsave Job' : 'Save Job') }}
          </button>
          <button class="btn" :class="isApplied ? 'btn-success' : 'btn-success'" @click="handleDirectApply" :disabled="isApplied" :style="{ opacity: isApplied ? '0.7' : '1', cursor: isApplied ? 'not-allowed' : 'pointer' }">
            {{ isApplied ? '✅ Applied' : '✅ Apply' }}
          </button>
          <button
            class="btn btn-primary"
            @click="handleGenerateCV"
            :disabled="isGeneratingCV"
            :style="{ opacity: isGeneratingCV ? '0.7' : '1', cursor: isGeneratingCV ? 'not-allowed' : 'pointer' }"
          >
            <span v-if="isGeneratingCV">⏳ Generating...</span>
            <span v-else>✨ Generate Customized CV</span>
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<style>
.pulse {
  animation: pulse 1.5s infinite ease-in-out;
}
@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 0.3; }
  100% { opacity: 0.7; }
}
</style>
