<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import { useToast } from '../store/useToast.js'

const store = useAppStore()
const router = useRouter()
const { addToast } = useToast()
const user = computed(() => store.user || {})

const isEditMode = ref(false)

// Provide defaults for all possible fields
const formData = ref({
  firstName: user.value.firstName || '',
  lastName: user.value.lastName || '',
  currentTitle: user.value.currentTitle || '',
  github: user.value.github || '',
  targetRoles: user.value.job_preferences?.target_roles || [],
  education: user.value.education || '',
  experience: user.value.experience || '',
  skills: user.value.skills || '',
  softSkills: user.value.softSkills || '',
  longResume: user.value.longResume || ''
})

const handleSave = () => {
  store.saveUser({ ...formData.value })
  isEditMode.value = false
  addToast('Profile updated successfully!', 'success')
}

const handleLogout = () => {
  store.logout()
  router.push('/login')
}

const getInitials = () => {
  const first = formData.value.firstName ? formData.value.firstName.charAt(0) : ''
  const last = formData.value.lastName ? formData.value.lastName.charAt(0) : ''
  return (first + last).toUpperCase() || 'U'
}
</script>

<template>
  <div class="page-container-wide">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
      <h1 style="font-size: 2rem; font-weight: 700;">Profile Dashboard</h1>
      <div style="display: flex; gap: 1rem;">
        <button class="btn btn-outline" @click="router.push('/preferences')">
          ⚙️ Edit Job Preferences
        </button>
        <button 
          class="btn" 
          :class="isEditMode ? 'btn-success' : 'btn-outline'"
          @click="isEditMode ? handleSave() : isEditMode = true"
        >
          {{ isEditMode ? 'Save Changes' : 'Edit Profile' }}
        </button>
        <button class="btn btn-outline" style="color: var(--danger-red); border-color: var(--danger-red);" @click="handleLogout">
          Logout
        </button>
      </div>
    </div>

    <div class="profile-layout-grid">
      <!-- Left Column: Summary & Quick Info -->
      <div class="profile-sidebar">
        <!-- User Card -->
        <div class="profile-card user-summary-card">
          <div class="user-summary-header"></div>
          <div class="user-avatar">{{ getInitials() }}</div>
          
          <div v-if="isEditMode" class="form-group" style="padding: 0 1.5rem;">
            <input type="text" class="form-input mb-1" v-model="formData.firstName" placeholder="First Name" />
            <input type="text" class="form-input mb-1" v-model="formData.lastName" placeholder="Last Name" />
            <input type="text" class="form-input mb-1" v-model="formData.currentTitle" placeholder="Current Title" />
            <input type="url" class="form-input" v-model="formData.github" placeholder="GitHub URL" />
          </div>
          <div v-else class="user-summary-info">
            <h2>{{ formData.firstName }} {{ formData.lastName }}</h2>
            <p class="user-title">{{ formData.currentTitle || 'No Title Set' }}</p>
            <a v-if="formData.github" :href="formData.github" target="_blank" class="user-github">
              🔗 {{ formData.github.replace('https://', '') }}
            </a>
          </div>
        </div>

        <!-- Target Roles -->
        <div class="profile-card">
          <h3 class="profile-card-title">Target Roles</h3>
          <div v-if="isEditMode" class="form-checkbox-group" style="display: flex; flex-direction: column; gap: 0.5rem;">
            <label class="form-checkbox-item" v-for="role in ['Frontend', 'Backend', 'Full-Stack', 'DevOps', 'Mobile', 'Data']" :key="role">
              <input type="checkbox" class="form-checkbox" :value="role" v-model="formData.targetRoles" />
              <span class="form-checkbox-label">{{ role }}</span>
            </label>
          </div>
          <div v-else class="job-card-tags">
            <span v-for="role in formData.targetRoles" :key="role" class="job-tag">{{ role }}</span>
            <span v-if="!formData.targetRoles?.length" class="text-light">No roles selected.</span>
          </div>
        </div>

      </div>

      <!-- Right Column: Detailed Background -->
      <div class="profile-main">
        <div class="profile-card">
          <h3 class="profile-card-title">Background & Experience</h3>
          
          <div class="profile-section">
            <h4>Education</h4>
            <textarea v-if="isEditMode" class="form-textarea" v-model="formData.education" placeholder="Add your educational background..."></textarea>
            <div v-else class="formatted-text">{{ formData.education || 'No education added.' }}</div>
          </div>

          <div class="profile-section">
            <h4>Prior Experiences</h4>
            <textarea v-if="isEditMode" class="form-textarea" v-model="formData.experience" placeholder="Detail your past work experience..."></textarea>
            <div v-else class="formatted-text">{{ formData.experience || 'No prior experiences added.' }}</div>
          </div>
        </div>

        <div class="profile-card" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
          <div class="profile-section" style="margin-bottom: 0;">
            <h4>Technical Skills</h4>
            <textarea v-if="isEditMode" class="form-textarea" v-model="formData.skills" placeholder="List your technical skills..."></textarea>
            <div v-else class="formatted-text">{{ formData.skills || 'No skills added.' }}</div>
          </div>

          <div class="profile-section" style="margin-bottom: 0;">
            <h4>Soft Skills</h4>
            <textarea v-if="isEditMode" class="form-textarea" v-model="formData.softSkills" placeholder="List your soft skills..."></textarea>
            <div v-else class="formatted-text">{{ formData.softSkills || 'No soft skills added.' }}</div>
          </div>
        </div>

        <div class="profile-card">
          <h3 class="profile-card-title">Detailed Resume</h3>
          <p class="text-light mb-2">A comprehensive overview of your professional journey.</p>
          <textarea v-if="isEditMode" class="form-textarea" style="min-height: 250px;" v-model="formData.longResume" placeholder="Paste your full detailed resume here..."></textarea>
          <div v-else class="formatted-text" style="min-height: 200px;">{{ formData.longResume || 'No detailed resume added.' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
