import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(authService.isAuthenticated())
  const loading = ref(false)
  const error = ref(null)

  async function login(username, password) {
    loading.value = true
    error.value = null
    try {
      await authService.login(username, password)
      isAuthenticated.value = true
      return true
    } catch (err) {
      error.value = err.response?.data?.error || 'Error al iniciar sesión'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    authService.logout()
    isAuthenticated.value = false
  }

  return {
    isAuthenticated,
    loading,
    error,
    login,
    logout
  }
})