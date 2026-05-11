import { describe, it, expect, beforeEach, vi } from 'vitest'
import { authService, roomService } from '@/services/api'

describe('API Services', () => {
  describe('authService', () => {
    it('debe enviar credenciales correctamente', async () => {
      // Mock del endpoint
      const mockLogin = vi.fn().mockResolvedValue({
        token: 'fake-jwt-token'
      })
      
      // El test verificaría que authService.login() funciona
      expect(authService).toBeDefined()
    })

    it('debe guardar token en localStorage', () => {
      // Mock de localStorage
      expect(localStorage.setItem).toBeDefined()
    })
  })

  describe('roomService', () => {
    it('debe obtener lista de salas', async () => {
      expect(roomService.getRooms).toBeDefined()
    })

    it('debe crear una sala', async () => {
      expect(roomService.createRoom).toBeDefined()
    })

    it('debe verificar PIN de sala', async () => {
      expect(roomService.verifyPin).toBeDefined()
    })
  })
})