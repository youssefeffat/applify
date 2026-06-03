<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../store/useAppStore.js'
import ProgressBar from '../components/ProgressBar.vue'
import AiAgentChat from '../components/AiAgentChat.vue'
import aiAPI from '../api/ai'
import { useToast } from '../store/useToast.js'

const router = useRouter()
const store = useAppStore()
const { addToast } = useToast()

const steps = ['Basic Info', 'You', 'Target Roles']
const currentStep = ref(0)

// Step 2 AI Modal state
const showChat = ref(false)

// Data state
const formData = ref({
  firstName: '',
  lastName: '',
  github: '',
  education: '',
  experience: '',
  currentTitle: '',
  skills: '',
  softSkills: '',
  extra: '',
  certificates: '',
  languages: '',
  targetRoles: [],
  location: '',
  employmentTypes: [],
  targetYearsExperience: '',
  experienceLevels: [],
  minimumSalary: ''
})

// Local state for roles
const selectedRoles = ref([]) 
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

// City Search API
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

// Step 3 Inline Chatbot
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

const handleAiData = ({ field, value }) => {
  if (field in formData.value) {
    formData.value[field] += (formData.value[field] ? '\n\n' : '') + value
  }
}

// CV Upload
const cvInput = ref(null)
const handleFileUpload = async (event) => {
  if (event.target.files.length > 0) {
    const file = event.target.files[0]
    addToast('CV Uploaded successfully! Our AI is extracting your details...', 'success')
    
    try {
      const { data } = await aiAPI.parseCV(file)
      if (data) {
        if (data.education) formData.value.education = data.education
        if (data.experience) formData.value.experience = data.experience
        if (data.skills) formData.value.skills = data.skills
        if (data.softSkills) formData.value.softSkills = data.softSkills
        if (data.certificates) formData.value.certificates = data.certificates
        if (data.languages) formData.value.languages = data.languages
      }
    } catch (err) {
      addToast('Failed to parse CV', 'error')
      console.error(err)
    }
  }
}

const handleNext = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const handleBack = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const handleSubmit = async () => {
  if (selectedRoles.value.length === 0) {
    addToast('Please select or add at least one target role.', 'error')
    return
  }
  // Map selectedRoles to string array for compatibility with Profile
  formData.value.targetRoles = selectedRoles.value.map(r => r.title + (r.description ? ` - ${r.description}` : ''))
  
  const payload = {
    first_name: formData.value.firstName,
    last_name: formData.value.lastName,
    current_title: formData.value.currentTitle,
    github_url: formData.value.github,
    location: formData.value.location,
    job_preferences: {
      target_roles: formData.value.targetRoles,
      employment_types: formData.value.employmentTypes,
      experience_levels: formData.value.experienceLevels,
      target_years_experience: formData.value.targetYearsExperience || "0"
    },
    professional_background: {
      education: formData.value.education,
      experience: formData.value.experience,
      skills: formData.value.skills,
      soft_skills: formData.value.softSkills,
      certificates: formData.value.certificates,
      languages: formData.value.languages
    }
  }
  
  await store.updateUser(payload)
  router.push('/jobs')
}
</script>

<template>
  <div class="onboarding-page">
    <div class="onboarding-card">
      <ProgressBar :steps="steps" :currentStep="currentStep" />
      
      <form @submit.prevent="currentStep === steps.length - 1 ? handleSubmit() : handleNext()">
        <div class="onboarding-step-content">
          <!-- Step 1: Basic Info -->
          <div v-if="currentStep === 0">
            <h2 class="onboarding-step-title">Tell us about yourself</h2>
            <div class="form-group">
              <label class="form-label">First Name <span style="color: var(--danger-red);">*</span></label>
              <input type="text" class="form-input" v-model="formData.firstName" required />
            </div>
            <div class="form-group">
              <label class="form-label">Last Name <span style="color: var(--danger-red);">*</span></label>
              <input type="text" class="form-input" v-model="formData.lastName" required />
            </div>
            <div class="form-group">
              <label class="form-label">GitHub URL <span style="color: var(--text-light); font-size: 0.85em;">(Optional)</span></label>
              <input type="url" class="form-input" v-model="formData.github" placeholder="https://github.com/..." />
            </div>
            <div class="form-group">
              <label class="form-label">LinkedIn URL <span style="color: var(--text-light); font-size: 0.85em;">(Optional)</span></label>
              <input type="url" class="form-input" placeholder="https://linkedin.com/in/..." />
            </div>
          </div>

          <!-- Step 2: You -->
          <div v-if="currentStep === 1">
            <h2 class="onboarding-step-title">You</h2>
            
            <div class="cv-upload-section" style="margin-bottom: 2rem; padding: 1.5rem;" @click="cvInput.click()">
              <div class="cv-upload-icon">📄</div>
              <div class="cv-upload-text" style="font-weight: 600;">Upload CV (Recommended)</div>
              <div class="cv-upload-subtext">Click to upload your resume. Our AI will automatically analyze and reformulate your career details.</div>
              <input type="file" ref="cvInput" style="display: none;" accept=".pdf,.doc,.docx" @change="handleFileUpload" />
            </div>

            <div style="background-color: var(--primary-blue-light); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 2rem;">
              <p style="color: var(--primary-blue-dark); font-size: 0.95rem; margin: 0; line-height: 1.5;">
                <strong>Don't have a CV ready?</strong> Manually describe your career below. 
                What you write will be dynamically analyzed and reformulated by our AI to customize your CV when applying to jobs.
              </p>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <h3 style="margin: 0; font-size: 1.1rem; color: var(--text-dark);">Manual Entry</h3>
              <button type="button" class="btn btn-outline btn-sm" style="color: var(--primary-blue); border-color: var(--primary-blue);" @click="showChat = true">
                ✨ Use AI Council
              </button>
            </div>
            <p style="color: var(--text-medium); font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.4;">
              If you prefer not to write, launch the <strong>AI Council</strong>. It will ask profound questions regarding your career to build your profile automatically!
            </p>
            
            <div class="form-group">
              <label class="form-label">Education</label>
              <textarea class="form-textarea" style="min-height: 80px;" v-model="formData.education" placeholder="E.g. BSc in Computer Science..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Prior Experiences</label>
              <textarea class="form-textarea" style="min-height: 80px;" v-model="formData.experience" placeholder="Describe your past work experience in detail..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Technical Skills</label>
              <textarea class="form-textarea" style="min-height: 80px;" v-model="formData.skills" placeholder="E.g. React, Vue, Python, AWS..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Soft Skills</label>
              <textarea class="form-textarea" style="min-height: 80px;" v-model="formData.softSkills" placeholder="E.g. Leadership, Communication, Problem Solving..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Certificates / Courses</label>
              <textarea class="form-textarea" style="min-height: 80px;" v-model="formData.certificates" placeholder="E.g. AWS Certified Solutions Architect, Coursera ML..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Languages</label>
              <input type="text" class="form-input" v-model="formData.languages" placeholder="E.g. English (Native), Spanish (Fluent)..." />
            </div>
          </div>

          <!-- Step 3: Target Roles -->
          <div v-if="currentStep === 2">
            <h2 class="onboarding-step-title">Your Job Preferences</h2>
            
            <div class="form-group" style="position: relative;">
              <label class="form-label">Where do you want to work? <span style="color: var(--danger-red);">*</span></label>
              <input type="text" class="form-input" v-model="formData.location" @input="handleCitySearch" placeholder="Type a city (e.g. Paris)..." required autocomplete="off" />
              <div v-if="citySuggestions.length > 0" style="position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid var(--border-gray); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); z-index: 20; max-height: 200px; overflow-y: auto;">
                <div v-for="city in citySuggestions" :key="city" @click="selectCity(city)" style="padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid var(--border-gray); font-size: 0.9rem;">
                  📍 {{ city }}
                </div>
              </div>
            </div>

            <div class="form-group" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
              <div>
                <label class="form-label">Employment Type <span style="color: var(--danger-red);">*</span></label>
                <div class="form-checkbox-group" style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label class="form-checkbox-item" v-for="type in ['Full-Time', 'Part-Time', 'Contract', 'Freelance', 'Internship']" :key="type">
                    <input type="checkbox" class="form-checkbox" :value="type" v-model="formData.employmentTypes" />
                    <span class="form-checkbox-label">{{ type }}</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label class="form-label">Experience Level(s) to search for <span style="color: var(--danger-red);">*</span></label>
                <div class="form-checkbox-group" style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label class="form-checkbox-item" v-for="level in ['Entry', 'Mid', 'Senior', 'Executive']" :key="level">
                    <input type="checkbox" class="form-checkbox" :value="level" v-model="formData.experienceLevels" />
                    <span class="form-checkbox-label">{{ level }}</span>
                  </label>
                </div>
              </div>
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

          </div>
        </div>

        <div class="onboarding-actions">
          <button type="button" class="btn btn-outline" @click="handleBack" :disabled="currentStep === 0">
            Back
          </button>
          <button type="submit" class="btn btn-primary" style="flex: 1;">
            {{ currentStep === steps.length - 1 ? 'Complete Setup' : 'Continue' }}
          </button>
        </div>
      </form>
    </div>
    
    <AiAgentChat v-if="showChat" @close="showChat = false" @update-data="handleAiData" />
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
