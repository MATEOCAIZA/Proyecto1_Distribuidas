<template>
  <div class="admin-dashboard">
    <header class="dashboard-header">
      <div class="container">
        <div class="header-content">
          <div class="header-left">
            <h1 class="dashboard-title">Panel de Administración</h1>
            <p class="dashboard-subtitle">Gestiona tus salas de chat</p>
          </div>
          <button @click="logout" class="btn btn-danger">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M13 3H16C16.5304 3 17.0391 3.21071 17.4142 3.58579C17.7893 3.96086 18 4.46957 18 5V15C18 15.5304 17.7893 16.0391 17.4142 16.4142C17.0391 16.7893 16.5304 17 16 17H13M8 13L12 9M12 9L8 5M12 9H2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Cerrar Sesión
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="container">
        <div class="dashboard-actions">
          <button @click="openCreateModal" class="btn btn-primary btn-lg">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 5V15M5 10H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Nueva Sala
          </button>
          <button @click="fetchRooms" class="btn btn-outline" :disabled="roomStore.loading">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17.6569 17.6569C20.7811 14.5327 20.7811 9.46734 17.6569 6.34315C14.5327 3.21896 9.46734 3.21896 6.34315 6.34315C3.21896 9.46734 3.21896 14.5327 6.34315 17.6569C9.46734 20.7811 14.5327 20.7811 17.6569 17.6569Z" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8L12 12L14.5 14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Actualizar
          </button>
        </div>

        <div v-if="roomStore.error" class="alert alert-error">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/>
            <path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>{{ roomStore.error }}</span>
        </div>

        <div v-if="roomStore.loading && !roomStore.rooms.length" class="loading-state">
          <div class="spinner-large"></div>
          <p>Cargando salas...</p>
        </div>

        <div v-else-if="!roomStore.rooms.length" class="empty-state">
          <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="20" width="50" height="40" rx="4" stroke="#D1D5DB" stroke-width="3"/>
            <path d="M30 35H50M30 45H45" stroke="#D1D5DB" stroke-width="3" stroke-linecap="round"/>
          </svg>
          <h3>No hay salas creadas</h3>
          <p>Crea tu primera sala para comenzar a chatear</p>
          <button @click="openCreateModal" class="btn btn-primary">
            Crear Primera Sala
          </button>
        </div>

        <div v-else class="rooms-grid">
          <div
            v-for="room in roomStore.rooms"
            :key="room._id"
            class="room-card card"
          >
            <div class="card-body">
              <div class="room-header">
                <h3 class="room-name">{{ room.name }}</h3>
                <span
                  class="badge"
                  :class="room.type === 'multimedia' ? 'badge-success' : 'badge-primary'"
                >
                  {{ room.type === 'multimedia' ? 'Multimedia' : 'Texto' }}
                </span>
              </div>

              <div class="room-info">
                <!-- AÑADIDO: Ahora el administrador puede ver el ID de la sala -->
                <div class="info-item">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 4H12V12H4V4Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span><strong>ID:</strong> {{ room._id }}</span>
                </div>

                <div class="info-item">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 8C9.65685 8 11 6.65685 11 5C11 3.34315 9.65685 2 8 2C6.34315 2 5 3.34315 5 5C5 6.65685 6.34315 8 8 8Z" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M2 14C2 11.7909 5.13401 10 8 10C10.866 10 14 11.7909 14 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <span>{{ room.activeUsers || 0 }} usuarios activos</span>
                </div>

                <div class="info-item">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="3" y="3" width="10" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M5 1V3M11 1V3M3 7H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <span>{{ formatDate(room.createdAt) }}</span>
                </div>
              </div>

              <div class="room-actions">
                <div class="pin-display">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="4" y="6" width="8" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M6 6V5C6 3.89543 6.89543 3 8 3C9.10457 3 10 3.89543 10 5V6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <code class="room-pin">{{ room.pin }}</code>
                </div>

                <button
                  @click="copyRoomInfo(room)"
                  class="btn btn-sm btn-outline"
                  title="Copiar información de la sala"
                >
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M3 11H2C1.44772 11 1 10.5523 1 10V2C1 1.44772 1.44772 1 2 1H10C10.5523 1 11 1.44772 11 2V3" stroke="currentColor" stroke-width="1.5"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de creación de sala -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
      <div class="modal-content card" @click.stop>
        <div class="card-header">
          <h2>Crear Nueva Sala</h2>
          <button @click="closeCreateModal" class="close-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="card-body">
          <form @submit.prevent="handleCreateRoom">
            <div class="form-group">
              <label for="room-name" class="label">Nombre de la Sala</label>
              <input
                id="room-name"
                v-model="newRoom.name"
                type="text"
                class="input"
                placeholder="Ej: Sala General, Proyecto X, etc."
                required
              />
            </div>

            <div class="form-group">
              <label for="room-pin" class="label">PIN de Acceso (mínimo 4 dígitos)</label>
              <input
                id="room-pin"
                v-model="newRoom.pin"
                type="text"
                class="input"
                placeholder="Ej: 1234"
                pattern="[0-9]{4,}"
                required
              />
              <small class="input-help">El PIN debe tener al menos 4 dígitos numéricos</small>
            </div>

            <div class="form-group">
              <label class="label">Tipo de Sala</label>
              <div class="radio-group">
                <label class="radio-label">
                  <input
                    v-model="newRoom.type"
                    type="radio"
                    value="text"
                    name="room-type"
                  />
                  <span class="radio-custom"></span>
                  <span class="radio-text">
                    <strong>Solo Texto</strong>
                    <small>Permite únicamente el envío de mensajes de texto</small>
                  </span>
                </label>

                <label class="radio-label">
                  <input
                    v-model="newRoom.type"
                    type="radio"
                    value="multimedia"
                    name="room-type"
                  />
                  <span class="radio-custom"></span>
                  <span class="radio-text">
                    <strong>Multimedia</strong>
                    <small>Permite mensajes de texto y subida de archivos (imágenes, PDFs, etc.)</small>
                  </span>
                </label>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeCreateModal" class="btn btn-outline">
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary" :disabled="roomStore.loading">
                <span v-if="roomStore.loading" class="spinner"></span>
                <span v-else>Crear Sala</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomStore } from '@/stores/room'

const router = useRouter()
const authStore = useAuthStore()
const roomStore = useRoomStore()

const showCreateModal = ref(false)
const newRoom = ref({
  name: '',
  pin: '',
  type: 'text'
})

onMounted(() => {
  fetchRooms()
})

function logout() {
  authStore.logout()
  router.push({ name: 'Home' })
}

async function fetchRooms() {
  await roomStore.fetchRooms()
}

function openCreateModal() {
  showCreateModal.value = true
  newRoom.value = {
    name: '',
    pin: '',
    type: 'text'
  }
}

function closeCreateModal() {
  showCreateModal.value = false
}

async function handleCreateRoom() {
  try {
    await roomStore.createRoom(newRoom.value)
    closeCreateModal()
  } catch (error) {
    console.error('Error al crear sala:', error)
  }
}

function copyRoomInfo(room) {
  // Usamos roomId porque así viene en tu backend
  const id = room.roomId || 'No disponible';
  const name = room.name || 'Sin nombre';
  const type = room.type === 'multimedia' ? 'Multimedia' : 'Solo Texto';

  // NOTA: El PIN será "Privado" porque el backend no lo envía en get_all()
  const info = `Sala: ${name}\nID de la Sala: ${id}\nPIN: (Privado por seguridad)\nTipo: ${type}`;

  if (navigator.clipboard) {
    navigator.clipboard.writeText(info).then(() => {
      alert('Información de la sala copiada (ID: ' + id + ')');
    });
  }
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: var(--bg-secondary);
}

.dashboard-header {
  background: white;
  border-bottom: 1px solid var(--border-color);
  padding: 1.5rem 0;
  box-shadow: var(--shadow-sm);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-left {
  flex: 1;
}

.dashboard-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.dashboard-subtitle {
  color: var(--text-secondary);
  font-size: 0.938rem;
}

.dashboard-main {
  padding: 2rem 0;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

.empty-state svg {
  margin: 0 auto 1.5rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.room-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.room-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.room-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.room-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.info-item svg {
  color: var(--text-light);
  flex-shrink: 0;
}

.room-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.pin-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.room-pin {
  font-family: 'Courier New', monospace;
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary-color);
  background: rgba(79, 70, 229, 0.1);
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-sm);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
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

.modal-content .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-content .card-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.close-button:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
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

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.radio-label {
  display: flex;
  align-items: start;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.radio-label:hover {
  border-color: var(--primary-color);
  background: rgba(79, 70, 229, 0.02);
}

.radio-label input[type="radio"] {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-color);
  border-radius: 50%;
  flex-shrink: 0;
  position: relative;
  transition: all 0.2s ease;
  margin-top: 0.125rem;
}

.radio-label input[type="radio"]:checked + .radio-custom {
  border-color: var(--primary-color);
  background: var(--primary-color);
}

.radio-label input[type="radio"]:checked + .radio-custom::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.radio-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.radio-text strong {
  font-weight: 600;
  color: var(--text-primary);
}

.radio-text small {
  font-size: 0.813rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .dashboard-title {
    font-size: 1.5rem;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .rooms-grid {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions .btn {
    width: 100%;
  }
}
</style>