<template>
  <div class="chat-room-page">
    <header class="chat-header">
      <div class="header-content">
        <div class="header-left">
          <button @click="handleLeaveRoom" class="back-button" title="Salir de la sala">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 10H5M5 10L9 6M5 10L9 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="room-info-header">
            <h1 class="room-title">{{ currentRoomData?.name || 'Cargando...' }}</h1>
            <div class="room-status">
              <span class="status-badge" :class="chatStore.connected ? 'connected' : 'disconnected'">
                {{ chatStore.connected ? '🟢 Conectado' : '🔴 Desconectado' }}
              </span>
              <span class="badge badge-primary">
                {{ currentRoomData?.type === 'multimedia' ? '📁 Multimedia' : '💬 Texto' }}
              </span>
            </div>
          </div>
        </div>

        <div class="header-right">
          <div class="users-count">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 11C12.2091 11 14 9.20914 14 7C14 4.79086 12.2091 3 10 3C7.79086 3 6 4.79086 6 7C6 9.20914 7.79086 11 10 11Z" stroke="currentColor" stroke-width="2"/>
              <path d="M3 18C3 14.134 6.13401 11 10 11C13.866 11 17 14.134 17 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ chatStore.users.length }}</span>
          </div>
          <button @click="toggleUserList" class="btn-icon" title="Ver usuarios en la sala">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 7C1.89543 7 1 7.89543 1 9V17C1 18.1046 1.89543 19 3 19H17C18.1046 19 19 18.1046 19 17V9C19 7.89543 18.1046 7 17 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M3 7V5C3 3.89543 3.89543 3 5 3H15C16.1046 3 17 3.89543 17 5V7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M7 11H13M7 15H11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <div class="chat-container">
      <!-- Sidebar de usuarios (responsivo) -->
      <aside v-if="showUserList" class="users-sidebar" :class="{ mobile: isMobile }">
        <div class="sidebar-header">
          <h3>Usuarios en la Sala</h3>
          <button v-if="isMobile" @click="toggleUserList" class="close-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="users-list">
          <div
            v-for="user in chatStore.users"
            :key="user"
            class="user-item"
            :class="{ 'current-user': user === chatStore.currentUser?.nickname }"
          >
            <div class="user-avatar">{{ user.charAt(0).toUpperCase() }}</div>
            <div class="user-details">
              <span class="user-name">{{ user }}</span>
              <span v-if="user === chatStore.currentUser?.nickname" class="user-badge">Tú</span>
            </div>
          </div>

          <div v-if="!chatStore.users.length" class="empty-users">
            <p>No hay usuarios conectados</p>
          </div>
        </div>
      </aside>

      <!-- Área principal de chat -->
      <main class="chat-main">
        <!-- Mensajes -->
        <div class="messages-container" ref="messagesContainer">
          <div v-if="!chatStore.messages.length" class="empty-messages">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="32" cy="32" r="30" stroke="#E5E7EB" stroke-width="2"/>
              <path d="M32 18V32M28 28H36" stroke="#E5E7EB" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>Sé el primero en enviar un mensaje</p>
          </div>

          <div
            v-for="(message, index) in chatStore.messages"
            :key="index"
            class="message-group"
            :class="[
              message.type === 'system' ? 'message-system' : 'message-user',
              message.nickname === chatStore.currentUser?.nickname ? 'message-own' : ''
            ]"
          >
            <!-- Mensajes de sistema -->
            <div v-if="message.type === 'system'" class="system-message">
              <span>{{ message.content }}</span>
            </div>

            <!-- Mensajes de texto -->
            <div v-else-if="message.type === 'text' || !message.type" class="message-bubble">
              <div class="message-header">
                <strong class="message-author">{{ message.nickname }}</strong>
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
              </div>
              <p class="message-content">{{ message.content }}</p>
            </div>

            <!-- Mensajes con archivo -->
            <div v-else-if="message.type === 'file'" class="message-bubble message-file">
              <div class="message-header">
                <strong class="message-author">{{ message.nickname }}</strong>
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
              </div>
              <div class="file-preview">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V9L13 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                  <path d="M13 2V9H20" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                </svg>
                <div class="file-info">
                  <p class="file-name">{{ message.file?.name }}</p>
                  <p class="file-size">{{ formatFileSize(message.file?.size) }}</p>
                </div>
              </div>
              <a v-if="message.file?.url" :href="message.file.url" target="_blank" class="btn btn-sm btn-primary">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 1V11M12 7L8 11L4 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M2 13H14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                Descargar
              </a>
            </div>
          </div>

          <!-- Indicador de escritura -->
          <div v-if="isOtherUserTyping" class="typing-indicator">
            <p><strong>{{ typingUser }}</strong> está escribiendo</p>
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>

        <!-- Input de mensaje -->
        <div class="message-input-section">
          <div v-if="error" class="alert alert-error alert-sm">
            {{ error }}
          </div>

          <div class="input-group">
            <textarea
              v-model="newMessage"
              @keydown.enter.ctrl="sendMessage"
              @keydown.enter.meta="sendMessage"
              class="message-input"
              placeholder="Escribe un mensaje... (Ctrl+Enter para enviar)"
              rows="3"
            ></textarea>

            <div class="input-actions">
              <button
                v-if="currentRoomData?.type === 'multimedia'"
                @click="triggerFileInput"
                class="btn btn-icon"
                title="Compartir archivo"
                :disabled="loading"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 5V15M5 10H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>

              <input
                ref="fileInput"
                type="file"
                accept="image/*,.pdf"
                @change="handleFileSelect"
                style="display: none"
              />

              <button
                @click="sendMessage"
                class="btn btn-primary"
                :disabled="!newMessage.trim() || loading"
              >
                <span v-if="loading" class="spinner"></span>
                <svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 3L3 11V17H9L17 9M11 3L14 0L22 8L19 11M11 3L19 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          <p class="input-hint">Presiona <kbd>Ctrl+Enter</kbd> o <kbd>Cmd+Enter</kbd> para enviar</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useRoomStore } from '@/stores/room'
import { uploadService } from '@/services/api'

const router = useRouter()
const route = useRoute()
const chatStore = useChatStore()
const roomStore = useRoomStore()

const messagesContainer = ref(null)
const fileInput = ref(null)
const newMessage = ref('')
const showUserList = ref(true)
const isMobile = ref(false)
const loading = ref(false)
const error = ref(null)
const typingUser = ref(null)
const isOtherUserTyping = ref(false)

const currentRoomData = computed(() => roomStore.currentRoom || {})

onMounted(async () => {
  isMobile.value = window.innerWidth < 768
  window.addEventListener('resize', handleResize)

  const roomId = route.params.id
  const nickname = route.query.nickname || sessionStorage.getItem('current_nickname')
  const pin = sessionStorage.getItem('room_pin')

  if (!nickname || !roomId || !pin) {
    router.push({ name: 'JoinRoom' })
    return
  }

  chatStore.initializeSocket()
  chatStore.joinRoom(roomId, pin, nickname)

  roomStore.fetchRooms().then(() => {
    const room = roomStore.rooms.find(
      r => r._id === roomId || r.id === roomId || r.roomId === roomId
    )
    if (room) roomStore.setCurrentRoom(room)
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

function handleResize() {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) showUserList.value = true
}

function toggleUserList() {
  if (isMobile.value) showUserList.value = !showUserList.value
}

function handleLeaveRoom() {
  if (confirm('¿Estás seguro de que deseas salir de la sala?')) {
    sessionStorage.removeItem('room_pin')
    sessionStorage.removeItem('current_nickname')
    sessionStorage.removeItem('current_room_id')
    chatStore.leaveRoom()
    router.push({ name: 'Home' })
  }
}

function sendMessage() {
  if (!newMessage.value.trim()) return
  error.value = null
  chatStore.sendMessage(newMessage.value)
  newMessage.value = ''
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function triggerFileInput() {
  fileInput.value?.click()
}

async function handleFileSelect(event) {
  const file = event.target.files?.[0]
  if (!file) return

  const maxSize = 10 * 1024 * 1024
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']

  if (!allowedTypes.includes(file.type)) {
    error.value = 'Tipo de archivo no permitido. Solo JPG, PNG, GIF o PDF.'
    return
  }

  if (file.size > maxSize) {
    error.value = 'El archivo es demasiado grande. Máximo 10MB.'
    return
  }

  loading.value = true
  error.value = null

  try {
    const result = await uploadService.uploadFile(
      route.params.id,
      file,
      chatStore.currentUser?.nickname
    )
    chatStore.addFileMessage({
      name: file.name,
      size: file.size,
      url: uploadService.getFileUrl(result.filename)
    })
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al subir el archivo'
  } finally {
    loading.value = false
    event.target.value = ''
  }
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>

<style scoped>
.chat-room-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
}

/* Header */
.chat-header {
  background: white;
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 1.5rem;
  box-shadow: var(--shadow-sm);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

.back-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.back-button:hover {
  background: var(--bg-secondary);
  color: var(--primary-color);
}

.room-info-header {
  min-width: 0;
}

.room-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.room-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-badge {
  font-size: 0.813rem;
  font-weight: 500;
  white-space: nowrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.users-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.938rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.btn-icon {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: var(--bg-secondary);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

/* Chat Container */
.chat-container {
  flex: 1;
  display: flex;
  min-height: 0;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Usuarios Sidebar */
.users-sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.sidebar-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: var(--bg-secondary);
  color: var(--primary-color);
}

.users-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  transition: background 0.2s ease;
  margin-bottom: 0.5rem;
}

.user-item.current-user {
  background: rgba(79, 70, 229, 0.1);
}

.user-item:hover {
  background: var(--bg-secondary);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.938rem;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  display: block;
  font-size: 0.938rem;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  background: var(--primary-color);
  color: white;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  margin-top: 0.125rem;
}

.empty-users {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* Chat Main */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
  text-align: center;
}

.empty-messages svg {
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Mensajes */
.message-group {
  display: flex;
  animation: slideUp 0.3s ease;
}

.message-group.message-own {
  justify-content: flex-end;
}

.system-message {
  align-self: center;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  background: var(--bg-secondary);
  border-radius: 999px;
  margin: 0.5rem 0;
  width: auto;
  max-width: 600px;
}

.message-bubble {
  background: white;
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  box-shadow: var(--shadow-sm);
  max-width: 400px;
  word-wrap: break-word;
}

.message-group.message-own .message-bubble {
  background: var(--primary-color);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.375rem;
  gap: 0.75rem;
}

.message-author {
  font-weight: 600;
  font-size: 0.875rem;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
}

.message-content {
  font-size: 0.938rem;
  line-height: 1.5;
  margin: 0;
}

.message-file {
  min-width: 280px;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin: 0.5rem 0;
}

.message-group.message-own .file-preview {
  background: rgba(0, 0, 0, 0.1);
}

.file-preview svg {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  font-size: 0.938rem;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 0.813rem;
  opacity: 0.7;
  margin: 0.25rem 0 0;
}

.message-file .btn {
  margin-top: 0.75rem;
}

/* Indicador de escritura */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  width: fit-content;
  font-size: 0.875rem;
}

.typing-indicator p {
  margin: 0;
}

.typing-dots {
  display: flex;
  gap: 0.375rem;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-color);
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.5;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-8px);
  }
}

/* Input Section */
.message-input-section {
  padding: 1.5rem;
  background: white;
  border-top: 1px solid var(--border-color);
}

.alert-sm {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  font-size: 0.938rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: inherit;
  resize: none;
  transition: all 0.2s ease;
  max-height: 200px;
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-actions {
  display: flex;
  gap: 0.5rem;
}

.input-hint {
  font-size: 0.75rem;
  color: var(--text-light);
  margin-top: 0.5rem;
}

kbd {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 0.25rem;
  padding: 0.125rem 0.375rem;
  font-family: monospace;
  font-size: 0.75rem;
}

/* Responsivo */
@media (max-width: 768px) {
  .users-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    max-width: 100%;
    z-index: 100;
    border-right: none;
    border-bottom: none;
  }

  .users-sidebar.mobile {
    animation: slideInLeft 0.3s ease;
  }

  @keyframes slideInLeft {
    from {
      transform: translateX(-100%);
    }
    to {
      transform: translateX(0);
    }
  }

  .messages-container {
    padding: 1rem;
  }

  .message-bubble {
    max-width: 85%;
  }

  .message-input-section {
    padding: 1rem;
  }

  .input-group {
    gap: 0.5rem;
  }

  .btn-icon {
    padding: 0.375rem;
  }

  .room-title {
    font-size: 1rem;
  }

  .header-content {
    padding: 0;
  }

  .users-count {
    display: none;
  }

  .room-status {
    flex-direction: column;
    gap: 0.375rem;
  }
}

@media (max-width: 480px) {
  .message-bubble {
    max-width: 95%;
  }

  .room-status {
    display: none;
  }

  .input-hint {
    display: none;
  }
}
</style>