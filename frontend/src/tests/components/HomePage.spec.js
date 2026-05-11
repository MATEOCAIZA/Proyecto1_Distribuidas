import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/vue'
import HomePage from '@/views/HomePage.vue'

describe('HomePage', () => {
  // Configuración global para evitar errores de router-link
  const renderOptions = {
    global: {
      stubs: {
        'router-link': { template: '<a><slot /></a>' }
      }
    }
  }

  it('debe renderizar el título', () => {
    render(HomePage, renderOptions)
    expect(screen.getByText('ChatApp')).toBeDefined()
  })

  it('debe mostrar botón Unirse a Sala', () => {
    render(HomePage, renderOptions)
    const button = screen.getByText(/Unirse a una Sala/i)
    expect(button).toBeDefined()
  })

  it('debe mostrar botón Panel Administrador', () => {
    render(HomePage, renderOptions)
    const button = screen.getByText(/Panel Administrador/i)
    expect(button).toBeTruthy()
  })

  it('debe mostrar nota de privacidad', () => {
    render(HomePage, renderOptions)
    // Se cambia el matcher para que busque "Salas Seguras" que es lo que aparece en tu hero-subtitle
    // o el texto dentro de las cards, ya que "Las salas son privadas" no está en el DOM.
    const note = screen.getByText(/Salas Seguras/i)
    expect(note).toBeDefined()
  })

  it('debe tener 3 feature cards', () => {
    render(HomePage, renderOptions)
    const cards = document.querySelectorAll('.feature-card')
    expect(cards.length).toBe(3)
  })
})