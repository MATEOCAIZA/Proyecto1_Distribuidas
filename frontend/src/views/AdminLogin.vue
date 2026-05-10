<template>
  <div class="admin-login-page">
    <div class="login-container">
      <div class="login-card card">
        <div class="card-header">
          <router-link to="/" class="back-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 10H5M5 10L9 6M5 10L9 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Volver
          </router-link>
          <h2 class="login-title">Panel de Administrador</h2>
          <p class="login-subtitle">Ingresa tus credenciales para acceder</p>
        </div>

        <div class="card-body">
          <div v-if="authStore.error" class="alert alert-error">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/>
              <path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ authStore.error }}</span>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="username" class="label">Usuario</label>
              <input
                id="username"
                v-model="username"
                type="text"
                class="input"
                placeholder="Ingresa tu usuario"
                required
                autocomplete="username"
              />
            </div>

            <div class="form-group">
              <label for="password" class="label">Contraseña</label>
              <input
                id="password"
                v-model="password"
                type="password"
                class="input"
                placeholder="Ingresa tu contraseña"
                required
                autocomplete="current-password"
              />
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-full btn-lg"
              :disabled="authStore.loading"
            >
              <span v-if="authStore.loading" class="spinner"></span>
              <span v-else>Iniciar Sesión</span>
            </button>
          </form>

          <div class="login-help">
            <p class="help-text">
              <strong>Credenciales por defecto:</strong><br>
              Usuario: <code>admin</code><br>
              Contraseña: <code>Admin123</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

async function handleLogin() {
  const success = await authStore.login(username.value, password.value)
  if (success) {
    router.push({ name: 'AdminDashboard' })
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  width: 100%;
  max-width: 480px;
}

.login-card {
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

.login-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: var(--text-secondary);
  font-size: 0.938rem;
}

.login-form {
  margin-top: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.login-help {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.help-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

.help-text code {
  background: var(--bg-secondary);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
  color: var(--primary-color);
  font-weight: 600;
}

@media (max-width: 640px) {
  .login-title {
    font-size: 1.5rem;
  }

  .back-button {
    position: static;
    margin-bottom: 1rem;
    justify-content: center;
  }
}
</style>