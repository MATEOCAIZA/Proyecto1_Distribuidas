import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login', { username, password })
    if (response.data.token) {
      localStorage.setItem('admin_token', response.data.token)
    }
    return response.data
  },

  logout() {
    localStorage.removeItem('admin_token')
  },

  isAuthenticated() {
    return !!localStorage.getItem('admin_token')
  },

  getToken() {
    return localStorage.getItem('admin_token')
  }
}

export const roomService = {
  async createRoom(roomData) {
    const response = await api.post('/rooms/', roomData)
    return response.data
  },

  async getRooms() {
    const response = await api.get('/rooms/')
    return response.data
  },

  async verifyPin(roomId, pin) {
    const response = await api.post(`/rooms/${roomId}/verify`, { pin })
    return response.data
  }
}

export const uploadService = {
  async uploadFile(roomId, file, nickname) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('nickname', nickname)

    const response = await axios.post(
      `${API_URL}/upload/${roomId}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  },

  getFileUrl(filename) {
    return `${API_URL}/upload/files/${filename}`
  }
}

export default api