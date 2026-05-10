<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="logo">
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="60" height="60" rx="12" fill="#4F46E5"/>
              <path d="M20 25C20 22.2386 22.2386 20 25 20H35C37.7614 20 40 22.2386 40 25V35C40 37.7614 37.7614 40 35 40H25C22.2386 40 20 37.7614 20 35V25Z" fill="white"/>
              <circle cx="27" cy="28" r="2" fill="#4F46E5"/>
              <circle cx="33" cy="28" r="2" fill="#4F46E5"/>
              <path d="M26 33C26 33 27.5 35 30 35C32.5 35 34 33 34 33" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="hero-title">ChatApp</h1>
          <p class="hero-subtitle">Sistema de Chat en Tiempo Real con Salas Seguras</p>
          
          <div class="cta-buttons">
            <router-link to="/join" class="btn btn-primary btn-lg">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2Z" stroke="currentColor" stroke-width="2"/>
                <path d="M10 6V10L13 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Unirse a una Sala
            </router-link>
            <router-link to="/admin/login" class="btn btn-outline btn-lg">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 11C12.2091 11 14 9.20914 14 7C14 4.79086 12.2091 3 10 3C7.79086 3 6 4.79086 6 7C6 9.20914 7.79086 11 10 11Z" stroke="currentColor" stroke-width="2"/>
                <path d="M3 18C3 14.134 6.13401 11 10 11C13.866 11 17 14.134 17 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Panel Administrador
            </router-link>
          </div>
        </div>

        <div class="features">
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 28C22.6274 28 28 22.6274 28 16C28 9.37258 22.6274 4 16 4C9.37258 4 4 9.37258 4 16C4 22.6274 9.37258 28 16 28Z" stroke="#4F46E5" stroke-width="2"/>
                <path d="M12 16L15 19L20 13" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Seguro</h3>
            <p>Acceso controlado mediante PINs encriptados y sesiones únicas</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 12L16 8L24 12M8 12L16 16M8 12V20L16 24M24 12L16 16M24 12V20L16 24M16 16V24" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>Tiempo Real</h3>
            <p>Comunicación instantánea con WebSockets y latencia menor a 1 segundo</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 10H26M6 16H26M6 22H26" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
                <circle cx="10" cy="10" r="2" fill="#F59E0B"/>
                <circle cx="10" cy="16" r="2" fill="#F59E0B"/>
                <circle cx="10" cy="22" r="2" fill="#F59E0B"/>
              </svg>
            </div>
            <h3>Multimedia</h3>
            <p>Comparte archivos, imágenes y documentos en salas multimedia</p>
          </div>
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="container">
        <p>&copy; 2026 ChatApp - Universidad de las Fuerzas Armadas ESPE</p>
        <p class="footer-text">Proyecto de Aplicaciones Distribuidas</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero-section {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 3rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero-content {
  text-align: center;
  padding: 2rem 0;
}

.logo {
  display: inline-block;
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.95;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-xl);
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1.5rem;
  background: white;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.feature-card p {
  opacity: 0.9;
  line-height: 1.6;
}

.footer {
  background: var(--bg-dark);
  color: white;
  padding: 2rem 0;
  text-align: center;
  margin-top: auto;
}

.footer-text {
  opacity: 0.7;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .features {
    grid-template-columns: 1fr;
  }
}
</style>