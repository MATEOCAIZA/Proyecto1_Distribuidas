import { defineStore } from 'pinia'
import { ref } from 'vue'
import { roomService } from '@/services/api'

export const useRoomStore = defineStore('room', () => {
  const rooms = ref([])
  const currentRoom = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchRooms() {
  loading.value = true
  error.value = null
  try {
    const data = await roomService.getRooms()
    // Si data es un array, úsalo. Si tiene la propiedad .rooms, usa esa.
    rooms.value = Array.isArray(data) ? data : (data.rooms || [])
    return true
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al cargar salas'
    return false
  } finally {
    loading.value = false
  }
}

async function createRoom(roomData) {
  loading.value = true
  error.value = null
  try {
    const data = await roomService.createRoom(roomData)
    // Si data tiene .room úsalo, si no, usa data directamente
    const newRoom = data.room || data 
    
    rooms.value.unshift(newRoom)
    return newRoom
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al crear sala'
    throw err
  } finally {
    loading.value = false
  }
}

 async function verifyRoomPin(roomId, pin) {
  loading.value = true
  error.value = null
  try {
    // Usamos el roomId (ej: 7C99BB02) ya que el _id no llega del back
    console.log('🔍 Llamando verifyPin con roomId:', roomId)  // ← AÑADE
    const data = await roomService.verifyPin(roomId, pin)
     console.log('🔍 Respuesta verifyPin:', data)  // ← AÑADE
    if (data) {
      currentRoom.value = data
      return true
    }
    return false
  } catch (err) {
    error.value = err.response?.data?.error || 'PIN incorrecto'
    return false
  } finally {
    loading.value = false
  }
}

  function setCurrentRoom(room) {
    currentRoom.value = room
  }

  function clearCurrentRoom() {
    currentRoom.value = null
  }

  return {
    rooms,
    currentRoom,
    loading,
    error,
    fetchRooms,
    createRoom,
    verifyRoomPin,
    setCurrentRoom,
    clearCurrentRoom
  }
})