<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1 class="error-title">Pagina non trovata</h1>
      <p class="error-message">
        La pagina che stai cercando non esiste o è stata spostata.
      </p>
      <div class="action-buttons">
        <router-link to="/" class="btn btn-primary">
          <i class="bi bi-house-door"></i> Torna alla Home
        </router-link>
        <button @click="goBack" class="btn btn-outline-secondary ms-2">
          <i class="bi bi-arrow-left"></i> Torna indietro
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
  text-align: center;
}

.not-found-content {
  max-width: 600px;
  padding: 2rem;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.error-code {
  font-size: 6rem;
  font-weight: 700;
  color: #e63946;
  line-height: 1;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 2rem;
  color: #2b2d42;
  margin-bottom: 1rem;
}

.error-message {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn i {
  font-size: 1.1em;
}

.btn-primary {
  background-color: #0d6efd;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(13, 110, 253, 0.2);
}

.btn-outline-secondary {
  border: 1px solid #6c757d;
  color: #6c757d;
  background-color: transparent;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .action-buttons {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .error-code {
    font-size: 4.5rem;
  }
  
  .error-title {
    font-size: 1.75rem;
  }
}
</style>
