import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useRoomStore } from '@/stores/room'

describe('Room Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('debe inicializar con rooms vacío', () => {
    const room = useRoomStore()
    expect(room.rooms).toEqual([])
  })

  it('debe tener currentRoom en null', () => {
    const room = useRoomStore()
    expect(room.currentRoom).toBeNull()
  })

  it('debe tener método fetchRooms', () => {
    const room = useRoomStore()
    expect(typeof room.fetchRooms).toBe('function')
  })

  it('debe tener método createRoom', () => {
    const room = useRoomStore()
    expect(typeof room.createRoom).toBe('function')
  })

  it('debe tener método verifyRoomPin', () => {
    const room = useRoomStore()
    expect(typeof room.verifyRoomPin).toBe('function')
  })

  it('debe establecer sala actual', () => {
    const room = useRoomStore()
    const mockRoom = { _id: '123', name: 'Test' }
    room.setCurrentRoom(mockRoom)
    expect(room.currentRoom).toEqual(mockRoom)
  })

  it('debe limpiar sala actual', () => {
    const room = useRoomStore()
    room.clearCurrentRoom()
    expect(room.currentRoom).toBeNull()
  })
})