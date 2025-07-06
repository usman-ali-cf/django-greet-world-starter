<template>
  <div class="configure-panel-view">
    <div class="page-header">
      <h1>Configurazione Quadro Elettrico</h1>
      <router-link 
        :to="`/projects/${projectId}`" 
        class="btn btn-secondary"
      >
        Torna al Progetto
      </router-link>
    </div>
    
    <div class="construction-container">
      <div class="construction-icon">
        🚧
      </div>
      <h2>Pagina in fase di sviluppo</h2>
      <p class="construction-message">
        Stiamo lavorando per offrirti presto un'interfaccia completa di configurazione del quadro elettrico.
      </p>
      <div class="construction-image">
        <img 
          src="@/assets/under_construction.png" 
          alt="In costruzione"
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const projectId = ref(route.params.id);

onMounted(() => {
  // Component mounted logic here
});
</script>

<style scoped>
.configure-panel-view {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}

h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.construction-container {
  text-align: center;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  margin-top: 2rem;
}

.construction-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.construction-message {
  font-size: 1.1rem;
  color: #495057;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

.construction-image {
  margin-top: 2rem;
}

.construction-image img {
  max-width: 300px;
  opacity: 0.8;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
  text-decoration: none;
  white-space: nowrap;
  border: 1px solid transparent;
  border-radius: 0.25rem;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

.btn-secondary {
  color: #fff;
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5c636a;
  border-color: #565e64;
}
</style>
