<template>
  <div class="project-list-view">
    <div class="row g-0 h-100">
      <!-- Sidebar -->
      <div class="col-md-3 border-end">
        <div class="sidebar-header p-3 border-bottom">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="h5 mb-0">Progetti</h3>
            <router-link to="/projects/new" class="btn btn-sm btn-primary">
              <i class="fas fa-plus"></i> Nuovo
            </router-link>
          </div>
        </div>
        
        <div class="project-list p-2" style="height: calc(100vh - 150px); overflow-y: auto;">
          <div 
            v-for="project in projects.data" 
            :key="project.id_prg" 
            class="project-item p-2 mb-2 rounded"
            :class="{ 'bg-light': currentProjectId === project.id_prg }"
            @click="selectProject(project.id_prg)"
          >
            <div class="fw-bold">{{ project.name }}</div>
            <div class="text-muted small">{{ project.description || 'Nessuna descrizione' }}</div>
          </div>
          
          <div v-if="loading" class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Caricamento...</span>
            </div>
          </div>
          
          <div v-if="!loading && projects.length === 0" class="text-muted py-3 text-center">
            Nessun progetto trovato
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="col-md-9">
        <div class="p-4">
          <div v-if="!currentProjectId" class="d-flex flex-column align-items-center justify-content-center h-100">
            <i class="fas fa-folder-open fa-4x mb-3 text-muted"></i>
            <h4>Seleziona un progetto</h4>
            <p class="text-muted mb-4">Seleziona un progetto esistente o creane uno nuovo per iniziare.</p>
            <router-link to="/projects/new" class="btn btn-primary">
              <i class="fas fa-plus me-2"></i> Crea Nuovo Progetto
            </router-link>
          </div>
          
          <router-view v-else />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const projects = ref([]);
const loading = ref(false);
const currentProjectId = ref(route.params.id || null);

// Load projects when component mounts
const fetchProjects = async () => {
  try {
    loading.value = true;
    const response = await api.getProjects();
    console.log(response.data);
    projects.value = response.data;
    console.log(projects.value);
  } catch (error) {
    console.error('Error fetching projects:', error);
  } finally {
    loading.value = false;
  }
};

// Select project
const selectProject = (projectId) => {
  currentProjectId.value = projectId;
  router.push(`/projects/${projectId}`);
};

// Initialize component
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 0.75rem;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.project-list {
  overflow-y: auto;
  max-height: calc(100vh - 150px);
}

.project-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.project-item:hover {
  background-color: #f8f9fa;
}

.project-item.active {
  background-color: #e9f5ff;
  border-left: 3px solid #3498db;
}

.project-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
  color: #2c3e50;
}

.project-desc {
  font-size: 0.85rem;
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
  text-align: center;
  color: #6c757d;
}

.empty-state i {
  color: #dee2e6;
  margin-bottom: 1rem;
}

.empty-state h4 {
  color: #343a40;
  margin-bottom: 0.5rem;
}

.empty-state p {
  margin-bottom: 1.5rem;
  max-width: 300px;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.spinner-border {
  width: 1.5rem;
  height: 1.5rem;
  border-width: 0.15em;
}
</style>
