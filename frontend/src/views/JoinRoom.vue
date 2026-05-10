<template>
  <div class="join-room-page">
    <div class="join-container">
      <div class="join-card card">
        <div class="card-header">
          <router-link to="/" class="back-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 10H5M5 10L9 6M5 10L9 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Volver
          </router-link>
          <h2 class="join-title">Unirse a una Sala</h2>
          <p class="join-subtitle">Ingresa el PIN y tu nickname para acceder</p>
        </div>

        <div class="card-body">
          <div v-if="error" class="alert alert-error">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/>
              <path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ error }}</span>
          </div>

          <form @submit.prevent="handleJoinRoom" class="join-form">
            <div class="form-group">
              <label for="room-id" class="label">ID de la Sala</label>
              <input
                id="room-id"
                v-model="formData.roomId"
                type="text"
                class="input"
                placeholder="Ej: 507f1f77bcf86cd799439011"
                required
              />
              <small class="input-help">El administrador comparte el ID de la sala contigo</small>
            </div>

            <div class="form-group">
              <label for="pin" class="label">PIN de Acceso</label>
              <input
                id="pin"
                v-model="formData.pin"
                type="password"
                class="input"
                placeholder="Ingresa el PIN de 4 dígitos"
                pattern="[0-9]{4,}"
                required
              />
            </div>

            <div class="form-group">
              <label for="nickname" class="label">Tu Nickname</label>
              <input
                id="nickname"
                v-model="formData.nickname"
                type="text"
                class="input"
                placeholder="Ej: Juan, Dev_User, etc."
                maxlength="20"
                required
              />
              <small class="input-help">Máximo 20 caracteres. Este será tu nombre en la sala.</small>
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-full btn-lg"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner"></span>
              <span v-else>Unirse a la Sala</span>
            </button>
          </form>

          <div class="join-tips">
            <h4>💡 Consejos</h4>
            <ul>
              <li>Recuerda que solo puedes estar en una sala a la vez</li>
              <li>El PIN es privado y garantiza la seguridad de la sala</li>
              <li>Tu sesión se cerrará automáticamente si te desconectas por inactividad</li>
              <li>Asegúrate de tener una conexión estable a internet</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoomStore } from '@/stores/room'

const router = useRouter()
const roomStore = useRoomStore()

const loading = ref(false)
const error = ref(null)
const formData = ref({
  roomId: '',
  pin: '',
  nickname: ''
})

async function handleJoinRoom() {
  error.value = null
  loading.value = true

  console.log('📤 Intentando join con roomId:', formData.value.roomId)

  try {
    // Verificar el PIN de la sala
    const success = await roomStore.verifyRoomPin(
      formData.value.roomId,
      formData.value.pin
    )

    console.log('📥 Resultado verifyPin:', success)  // ← AÑADE
    console.log('📥 Error del store:', roomStore.error)  // ← AÑADE

    if (success) {
      // Guardar el nickname en sessionStorage para usarlo en el chat
      sessionStorage.setItem('current_nickname', formData.value.nickname)
      sessionStorage.setItem('current_room_id', formData.value.roomId)
        sessionStorage.setItem('room_pin', formData.value.pin)

      // Navegar a la sala de chat
      router.push({
        name: 'ChatRoom',
        params: { id: formData.value.roomId },
        query: { nickname: formData.value.nickname } 
      })
    } else {
      error.value = 'PIN incorrecto o sala no encontrada'
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al unirse a la sala. Intenta nuevamente.'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.join-room-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.join-container {
  width: 100%;
  max-width: 480px;
}

.join-card {
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  text-align: center;
  position: relative;
}

.back-button {
  position: absolute;
  left: 1.5rem;
  top: 1.25rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.back-button:hover {
  color: var(--primary-color);
}

.join-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.join-subtitle {
  color: var(--text-secondary);
  font-size: 0.938rem;
}

.join-form {
  margin-top: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.input-help {
  display: block;
  margin-top: 0.375rem;
  font-size: 0.813rem;
  color: var(--text-secondary);
}

.join-tips {
  margin-top: 2rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-left: 4px solid var(--primary-color);
  border-radius: var(--radius-md);
}

.join-tips h4 {
  font-size: 0.938rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.join-tips ul {
  list-style: none;
}

.join-tips li {
  font-size: 0.813rem;
  color: var(--text-secondary);
  padding: 0.375rem 0;
  line-height: 1.6;
}

.join-tips li::before {
  content: '✓ ';
  color: var(--secondary-color);
  font-weight: 600;
  margin-right: 0.375rem;
}

@media (max-width: 640px) {
  .join-title {
    font-size: 1.5rem;
  }

  .back-button {
    position: static;
    margin-bottom: 1rem;
    justify-content: center;
  }
}
</style>