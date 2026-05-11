import { io } from 'socket.io-client'

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:3001'

class SocketService {
  constructor() {
    this.socket = null
    this.connected = false
    this.pendingListeners = [] // ✅ guarda listeners registrados antes de connect()
  }

  connect() {
    if (this.socket?.connected) {
      return this.socket
    }

    // Si hay un socket desconectado colgado, límpialo
    if (this.socket) {
      this.socket.removeAllListeners()
      this.socket = null
    }

    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    })

    this.socket.on('connect', () => {
      console.log('✅ Socket conectado:', this.socket.id)
      this.connected = true
    })

    this.socket.on('disconnect', () => {
      console.log('❌ Socket desconectado')
      this.connected = false
    })

    this.socket.on('connect_error', (error) => {
      console.error('Error de conexión:', error)
    })

    // ✅ Aplica listeners que se registraron antes de connect()
    this.pendingListeners.forEach(({ event, callback }) => {
      this.socket.on(event, callback)
    })
    this.pendingListeners = []

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.removeAllListeners()
      this.socket.disconnect()
      this.socket = null
      this.connected = false
    }
  }

  emit(event, data) {
    if (this.socket?.connected) {
      this.socket.emit(event, data)
    } else {
      console.warn('Socket no conectado al emitir:', event)
    }
  }

  on(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback)
    } else {
      // ✅ Si el socket aún no existe, guarda para aplicar después del connect()
      this.pendingListeners.push({ event, callback })
    }
  }

  off(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback)
    }
    // Limpia también de pendientes
    this.pendingListeners = this.pendingListeners.filter(
      l => !(l.event === event && l.callback === callback)
    )
  }

  removeAllListeners() {
    if (this.socket) {
      // Remueve solo los listeners de negocio, no los internos
      ['room_joined', 'new_message', 'user_joined', 'user_left', 'user_list', 'error']
        .forEach(event => this.socket.removeAllListeners(event))
    }
    this.pendingListeners = []
  }

  joinRoom(roomId, pin, nickname) {
    // ✅ Espera a que el socket esté conectado antes de emitir
    if (this.socket?.connected) {
      this.socket.emit('join_room', { roomId, pin, nickname })
    } else if (this.socket) {
      this.socket.once('connect', () => {
        this.socket.emit('join_room', { roomId, pin, nickname })
      })
    }
  }

  sendMessage(content) {
    this.emit('send_message', { content })
  }

  sendFileMessage({ path, type, file_name }) {
  this.socket.emit('send_file_message', { path, type, file_name })
}

  leaveRoom() {
    // ✅ Emite el evento al servidor antes de desconectar
    this.emit('leave_room', {})
  }

  onRoomJoined(callback) { this.on('room_joined', callback) }
  onNewMessage(callback) { this.on('new_message', callback) }
  onUserJoined(callback) { this.on('user_joined', callback) }
  onUserLeft(callback) { this.on('user_left', callback) }
  onUserList(callback) { this.on('user_list', callback) }
  onError(callback) { this.on('error', callback) }

  isConnected() {
    return this.connected && this.socket?.connected
  }
}

export default new SocketService()