import { expect, afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/vue'

// Limpiar después de cada prueba
afterEach(() => {
  cleanup()
})

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}

global.localStorage = localStorageMock