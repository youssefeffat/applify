<script setup>
import { ref, onMounted, nextTick } from 'vue'
import aiAPI from '../api/ai'
import { useToast } from '../store/useToast.js'

const emit = defineEmits(['close', 'update-data'])
const { addToast } = useToast()

const messages = ref([
  { id: 1, role: 'ai', text: 'Hello! I am the AI Council. Let\'s dive deep into your career. To start, what was the most complex technical challenge you\'ve solved recently, and what specific technologies did you use?' }
])
const inputMessage = ref('')
const currentField = ref('challenge') // state machine: challenge -> conflict -> goals -> done

const messagesContainer = ref(null)
const isListening = ref(false)
let recognition = null

onMounted(() => {
  // Initialize speech recognition if supported
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (SpeechRecognition) {
    recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = true
    
    recognition.onstart = () => {
      isListening.value = true
    }
    
    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        transcript += event.results[i][0].transcript
      }
      inputMessage.value = transcript
    }
    
    recognition.onend = () => {
      isListening.value = false
    }
    
    recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error)
      isListening.value = false
      addToast('Speech recognition failed. Please try again.', 'error')
    }
  }
})

const toggleVoice = () => {
  if (!recognition) {
    addToast("Speech recognition is not supported in your browser (try Chrome/Edge).", 'error')
    return
  }
  
  if (isListening.value) {
    recognition.stop()
  } else {
    inputMessage.value = ''
    recognition.start()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSend = async () => {
  if (!inputMessage.value.trim()) return

  // 1. Add user message
  const userText = inputMessage.value
  messages.value.push({ id: Date.now(), role: 'user', text: userText })
  inputMessage.value = ''
  scrollToBottom()

  // 2. Real AI processing and extraction
  try {
    const { data } = await aiAPI.councilChat({ currentField: currentField.value, userMessage: userText })
    
    if (currentField.value === 'challenge') {
      emit('update-data', { field: 'experience', value: `Technical Challenge Solved: ${userText}` })
      emit('update-data', { field: 'skills', value: data.extractedData?.keywords?.join(', ') || userText }) 
      currentField.value = 'conflict'
    } else if (currentField.value === 'conflict') {
      emit('update-data', { field: 'softSkills', value: `Conflict Resolution: ${userText}` })
      currentField.value = 'goals'
    } else if (currentField.value === 'goals') {
      emit('update-data', { field: 'extra', value: `Goals & Extras: ${userText}` })
      currentField.value = 'done'
    }
    
    messages.value.push({ id: Date.now(), role: 'ai', text: data.nextQuestion })
    scrollToBottom()
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div class="chat-modal-overlay" @click.self="$emit('close')">
    <div class="chat-modal-content">
      <div class="chat-header">
        <div class="chat-title">
          <span>✨</span> AI Voice Agent
        </div>
        <button class="chat-close-btn" @click="$emit('close')">×</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="msg in messages" 
          :key="msg.id"
          class="chat-bubble"
          :class="msg.role === 'ai' ? 'chat-bubble-ai' : 'chat-bubble-user'"
        >
          {{ msg.text }}
        </div>
      </div>

      <div class="chat-input-area">
        <form class="chat-input-form" @submit.prevent="handleSend">
          <button 
            type="button" 
            class="chat-mic-btn" 
            :class="{ 'is-listening': isListening }"
            @click="toggleVoice"
            :disabled="currentField === 'done'"
            title="Talk to AI"
          >
            🎤
          </button>
          <input 
            type="text" 
            class="chat-input" 
            v-model="inputMessage" 
            placeholder="Type your response..."
            :disabled="currentField === 'done'"
          />
          <button type="submit" class="chat-send-btn" :disabled="currentField === 'done' || !inputMessage.trim()">
            ➤
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
