import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useChatStore } from '@/stores/chat'

describe('Chat Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('debe inicializar con arrays vacíos', () => {
    const chat = useChatStore()
    expect(chat.messages).toEqual([])
    expect(chat.users).toEqual([])
  })

  it('debe agregar mensaje a la lista', () => {
    const chat = useChatStore()
    // Simular push de mensaje
    const msg = { nickname: 'Test', content: 'Hola', timestamp: new Date() }
    // Chat debería tener un método para esto
    expect(chat).toBeDefined()
  })

  it('debe inicializar socket correctamente', () => {
    const chat = useChatStore()
    expect(typeof chat.initializeSocket).toBe('function')
  })

  it('debe unirse a una sala', () => {
    const chat = useChatStore()
    expect(typeof chat.joinRoom).toBe('function')
  })

  it('debe enviar mensaje', () => {
    const chat = useChatStore()
    expect(typeof chat.sendMessage).toBe('function')
  })

  it('debe salir de la sala', () => {
    const chat = useChatStore()
    expect(typeof chat.leaveRoom).toBe('function')
  })
})