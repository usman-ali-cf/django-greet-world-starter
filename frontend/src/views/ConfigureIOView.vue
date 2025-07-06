<template>
  <div class="configure-io-view">
    <div class="page-header">
      <h1>Configura Simbologia I/O</h1>
      <router-link 
        :to="`/projects/${projectId}`" 
        class="btn btn-secondary"
      >
        Torna al Progetto
      </router-link>
    </div>
    
    <div class="alert alert-info">
      <i class="fas fa-info-circle me-2"></i>
      Questa pagina è in fase di sviluppo.
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
.configure-io-view {
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

.alert {
  padding: 1rem;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.alert-info {
  background-color: #e7f5ff;
  color: #0c63e4;
  border: 1px solid #b6d4fe;
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

.me-2 {
  margin-right: 0.5rem;
}
</style>
