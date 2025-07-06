<template>
  <div class="projects-container">
    <div class="projects-header">
      <h1>I Tuoi Progetti</h1>
      <router-link to="/projects/new" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Nuovo Progetto
      </router-link>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Caricamento...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="projects.length === 0" class="no-projects">
      <p>Nessun progetto trovato. Crea il tuo primo progetto per iniziare.</p>
    </div>

    <div v-else class="projects-grid">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ project.nome_prg }}</h5>
            <p class="card-text">{{ project.descrizione || 'Nessuna descrizione' }}</p>
            <div class="project-meta">
              <span class="badge bg-secondary">
                <i class="bi bi-calendar"></i> 
                {{ formatDate(project.data_creazione) }}
              </span>
            </div>
            <div class="project-actions">
              <router-link 
                :to="{ name: 'project-overview', params: { id: project.id } }" 
                class="btn btn-outline-primary btn-sm"
              >
                Apri
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import { useAuthStore } from '@/stores/auth';

const projectStore = useProjectStore();
const authStore = useAuthStore();
const router = useRouter();

// Use computed properties from the store
const projects = computed(() => projectStore.projects);
const loading = computed(() => projectStore.loading);
const error = computed(() => projectStore.error);

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('it-IT');
};

// Fetch projects when component mounts
onMounted(async () => {
  try {
    // Only fetch projects if we don't have them already
    if (projects.value.length === 0) {
      await projectStore.fetchProjects();
    }
  } catch (err) {
    console.error('Error in ProjectsView setup:', err);
  }
});
</script>

<style scoped>
.projects-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.projects-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.no-projects {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.project-card {
  transition: transform 0.2s;
}

.project-card:hover {
  transform: translateY(-5px);
}

.card {
  height: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  color: #333;
}

.card-text {
  color: #666;
  flex-grow: 1;
  margin-bottom: 1rem;
}

.project-meta {
  margin: 1rem 0;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.project-actions {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 500;
  line-height: 1;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;
}

.bi {
  font-size: 0.9em;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-primary:hover {
  color: #fff;
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>
