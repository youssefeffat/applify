<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import aiAPI from '../api/ai'
import { useToast } from '../store/useToast.js'

const store = useAppStore()
const router = useRouter()
const { addToast } = useToast()

// Get user preferences or fallback to empty object
const user = computed(() => store.user || {})
const prefs = computed(() => user.value.job_preferences || {})

// Initialize custom roles parsing from saved strings ("Title - Description")
const initialRoles = (prefs.value.target_roles || []).map(str => {
  const parts = str.split(' - ')
  return { title: parts[0], description: parts.slice(1).join(' - ') || '' }
})
const selectedRoles = ref(initialRoles)

const formData = ref({
  employment_types: [...(prefs.value.employment_types || [])],
  experience_levels: [...(prefs.value.experience_levels || [])],
  target_years_experience: prefs.value.target_years_experience || '',
  location: user.value.location || ''
})

const employmentOptions = ['remote', 'hybrid', 'on-site', 'Full-Time', 'Part-Time', 'Contract']
const levelOptions = ['Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Executive']

// Role Search and Custom Roles
const roleSearchQuery = ref('')
const predefinedRoles = [
  'Frontend Developer', 'Backend Developer', 'Full-Stack Developer', 
  'DevOps Engineer', 'Mobile Developer', 'Data Scientist', 
  'Product Manager', 'UX/UI Designer', 'Machine Learning Engineer'
]

const filteredRoles = computed(() => {
  if (!roleSearchQuery.value) return []
  const query = roleSearchQuery.value.toLowerCase()
  return predefinedRoles.filter(role => role.toLowerCase().includes(query))
})

const showCustomRoleForm = ref(false)
const customRoleTitle = ref('')
const customRoleDesc = ref('')

const addRole = (title, description = '') => {
  if (!selectedRoles.value.some(r => r.title === title)) {
    selectedRoles.value.push({ title, description })
  }
  roleSearchQuery.value = ''
  showCustomRoleForm.value = false
  customRoleTitle.value = ''
  customRoleDesc.value = ''
}

const removeRole = (index) => {
  selectedRoles.value.splice(index, 1)
}

// AI Role Suggester
const step3Messages = ref([
  { role: 'ai', text: 'Not sure what role fits you best? Describe what you love doing, and I will suggest some roles!' }
])
const step3Input = ref('')

const handleStep3Chat = async () => {
  if (!step3Input.value.trim()) return
  step3Messages.value.push({ role: 'user', text: step3Input.value })
  const userText = step3Input.value
  step3Input.value = ''
  
  try {
    const { data } = await aiAPI.suggestRoles({ description: userText })
    if (data && data.suggestedRoles && data.suggestedRoles.length > 0) {
      step3Messages.value.push({ role: 'ai', text: `Based on that, you might enjoy being a **${data.suggestedRoles[0]}**. Feel free to add it to your custom roles!` })
    }
  } catch (err) {
    console.error("AI Role Suggestion failed", err)
  }
}

// City Search
let citySearchTimeout = null
const citySuggestions = ref([])

const handleCitySearch = () => {
  clearTimeout(citySearchTimeout)
  if (!formData.value.location || formData.value.location.length < 2) {
    citySuggestions.value = []
    return
  }
  
  citySearchTimeout = setTimeout(async () => {
    try {
      const res = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(formData.value.location)}&count=5&language=en&format=json`)
      const data = await res.json()
      if (data.results) {
        citySuggestions.value = data.results.map(r => `${r.name}, ${r.admin1 || r.country}`)
      } else {
        citySuggestions.value = []
      }
    } catch (e) {
      console.error(e)
    }
  }, 300)
}

const selectCity = (city) => {
  formData.value.location = city
  citySuggestions.value = []
}

const handleSave = async () => {
  try {
    const payload = {
      location: formData.value.location,
      job_preferences: {
        target_roles: selectedRoles.value.map(r => r.title + (r.description ? ` - ${r.description}` : '')),
        employment_types: formData.value.employment_types,
        experience_levels: formData.value.experience_levels,
        target_years_experience: formData.value.target_years_experience
      }
    }
    
    await store.updateUser(payload)
    addToast('Job preferences updated successfully!', 'success')
    router.push('/jobs')
  } catch (err) {
    addToast('Failed to save preferences. Please try again.', 'error')
    console.error(err)
  }
}
</script>

<template>
  <div class="page-container-wide">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
      <h1 style="font-size: 2rem; font-weight: 700;">Job Preferences</h1>
      <button class="btn btn-outline" @click="router.back()">Cancel</button>
    </div>

    <div class="profile-card" style="max-width: 800px; margin: 0 auto;">
      <p class="text-light mb-2">We use these preferences to match and recommend the best jobs for you. Jobs fitting these criteria will be shown in your Job Explorer.</p>
      
      <div class="form-group" style="position: relative; margin-top: 1.5rem;">
        <label class="form-label">Preferred Location</label>
        <input type="text" class="form-input" v-model="formData.location" @input="handleCitySearch" placeholder="Type a city (e.g. Paris)..." autocomplete="off" />
        <div v-if="citySuggestions.length > 0" style="position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid var(--border-gray); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); z-index: 20; max-height: 200px; overflow-y: auto;">
          <div v-for="city in citySuggestions" :key="city" @click="selectCity(city)" style="padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid var(--border-gray); font-size: 0.9rem;">
            📍 {{ city }}
          </div>
        </div>
      </div>
      
      <div class="form-group" style="margin-top: 1.5rem;">
        <label class="form-label">Employment Types</label>
        <div class="form-checkbox-group" style="display: flex; flex-wrap: wrap; gap: 1rem;">
          <label class="form-checkbox-item" v-for="type in employmentOptions" :key="type">
            <input type="checkbox" class="form-checkbox" :value="type" v-model="formData.employment_types" />
            <span class="form-checkbox-label" style="text-transform: capitalize;">{{ type }}</span>
          </label>
        </div>
      </div>
      
      <div class="form-group" style="margin-top: 1.5rem;">
        <label class="form-label">Target Experience Levels</label>
        <div class="form-checkbox-group" style="display: flex; flex-wrap: wrap; gap: 1rem;">
          <label class="form-checkbox-item" v-for="level in levelOptions" :key="level">
            <input type="checkbox" class="form-checkbox" :value="level" v-model="formData.experience_levels" />
            <span class="form-checkbox-label">{{ level }}</span>
          </label>
        </div>
      </div>
      
      <div class="form-group" style="margin-top: 1.5rem;">
        <label class="form-label">Years of Experience</label>
        <select class="form-select" v-model="formData.target_years_experience">
          <option value="">Select...</option>
          <option value="0-1">0-1 Years</option>
          <option value="1-3">1-3 Years</option>
          <option value="3-5">3-5 Years</option>
          <option value="5-10">5-10 Years</option>
          <option value="10+">10+ Years</option>
        </select>
      </div>

      <hr style="border: 0; border-top: 1px solid var(--border-gray); margin: 2rem 0;" />

      <h3 style="margin-bottom: 1rem; color: var(--text-dark);">What specific roles are you looking for?</h3>
      
      <div class="selected-roles" style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
        <div v-for="(role, index) in selectedRoles" :key="index" style="background-color: var(--primary-blue); color: white; padding: 0.5rem 1rem; border-radius: 2rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem;">
          <span style="font-weight: 600;">{{ role.title }}</span>
          <button type="button" @click="removeRole(index)" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.1rem; line-height: 1;">&times;</button>
        </div>
      </div>

      <div class="form-group" style="position: relative;">
        <input type="text" class="form-input" v-model="roleSearchQuery" placeholder="Search for standard roles (e.g. Frontend)..." />
        <div v-if="filteredRoles.length > 0" style="position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid var(--border-gray); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); z-index: 10; max-height: 150px; overflow-y: auto;">
          <div v-for="role in filteredRoles" :key="role" @click="addRole(role)" style="padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid var(--border-gray);">
            {{ role }}
          </div>
        </div>
      </div>

      <div style="text-align: center; margin: 1.5rem 0;">
        <button type="button" class="btn btn-outline btn-sm" @click="showCustomRoleForm = !showCustomRoleForm">
          {{ showCustomRoleForm ? 'Cancel Custom Role' : '+ Add Custom Role' }}
        </button>
      </div>

      <div v-if="showCustomRoleForm" style="background-color: var(--bg-light-gray); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 2rem;">
        <div class="form-group">
          <label class="form-label">Custom Role Title</label>
          <input type="text" class="form-input" v-model="customRoleTitle" placeholder="e.g. Developer Evangelist" />
        </div>
        <div class="form-group">
          <label class="form-label">Role Description</label>
          <textarea class="form-textarea" v-model="customRoleDesc" placeholder="Describe the responsibilities and focus of this role..." style="min-height: 80px;"></textarea>
        </div>
        <button type="button" class="btn btn-primary btn-sm" @click="addRole(customRoleTitle, customRoleDesc)" :disabled="!customRoleTitle.trim()">Add Custom Role</button>
      </div>

      <div class="ai-role-suggester" style="border: 1px solid var(--border-gray); border-radius: var(--radius-lg); overflow: hidden;">
        <div style="background-color: var(--primary-blue); padding: 1rem; color: white; font-weight: 600; display: flex; align-items: center; gap: 0.5rem;">
          <span>🤖</span> AI Role Suggester
        </div>
        <div style="padding: 1.5rem; background-color: #f8fafc; display: flex; flex-direction: column; gap: 1rem; max-height: 250px; overflow-y: auto;">
          <div v-for="(msg, idx) in step3Messages" :key="idx" :style="{ alignSelf: msg.role === 'ai' ? 'flex-start' : 'flex-end', backgroundColor: msg.role === 'ai' ? 'white' : 'var(--primary-blue)', color: msg.role === 'ai' ? 'var(--text-dark)' : 'white', padding: '0.75rem 1rem', borderRadius: '1rem', borderBottomLeftRadius: msg.role === 'ai' ? '0' : '1rem', borderBottomRightRadius: msg.role === 'user' ? '0' : '1rem', border: msg.role === 'ai' ? '1px solid var(--border-gray)' : 'none', maxWidth: '85%', fontSize: '0.9rem', lineHeight: '1.4' }">
            <span v-html="msg.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')"></span>
          </div>
        </div>
        <div style="padding: 1rem; border-top: 1px solid var(--border-gray); background: white; display: flex; gap: 0.5rem;">
          <input type="text" v-model="step3Input" @keyup.enter="handleStep3Chat" placeholder="I love designing user interfaces..." style="flex: 1; padding: 0.75rem 1rem; border: 1px solid var(--border-gray); border-radius: 2rem; font-size: 0.9rem;" />
          <button type="button" @click="handleStep3Chat" style="background-color: var(--primary-blue); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer;">➤</button>
        </div>
      </div>

      <div style="margin-top: 2rem; display: flex; justify-content: flex-end;">
        <button class="btn btn-primary" @click="handleSave">Save Preferences</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-gray);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
}
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px var(--primary-blue-light);
}
</style>
