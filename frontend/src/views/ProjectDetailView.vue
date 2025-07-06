<template>
  <div v-if="project" class="project-detail">
    <div class="project-info">
      <h1>{{ project.data.name }}</h1>
      <p class="project-description">{{ project.data.description || 'Nessuna descrizione' }}</p>
      
      <div class="project-actions mb-4">
        <button @click="showDeleteModal = true" class="btn btn-danger btn-sm">
          <i class="fas fa-trash-alt me-1"></i> Elimina Progetto
        </button>
      </div>
    </div>
    
    <div class="project-tabs">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/upload-utilities`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'upload-utilities' }"
          >
            <i class="fas fa-upload me-2"></i>Carica Utenze
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/configure-utilities`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'configure-utilities' }"
          >
            <i class="fas fa-cog me-2"></i>Configura Utenze
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/configure-power`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'configure-power' }"
          >
            <i class="fas fa-bolt me-2"></i>Configura Potenza
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/configure-io`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'configure-io' }"
          >
            <i class="fas fa-plug me-2"></i>Configura I/O
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/configure-panel`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'configure-panel' }"
          >
            <i class="fas fa-th-large me-2"> </i>Configura Quadro
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/create-node`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'create-node' }"
          >
            <i class="fas fa-server me-2"></i>Crea Nodo
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            :to="`/projects/${project.data.id_prg}/assign-io`" 
            class="nav-link"
            :class="{ 'active': $route.name === 'assign-io' }"
          >
            <i class="fas fa-exchange-alt me-2"></i>Assegna I/O
          </router-link>
        </li>
      </ul>
      
      <div class="tab-content p-3 border border-top-0 rounded-bottom">
        <router-view :project="project" />
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Conferma eliminazione</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            Sei sicuro di voler eliminare il progetto "{{ project.nome_progetto }}"?
            Questa azione non può essere annullata.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Annulla</button>
            <button type="button" class="btn btn-danger" @click="deleteProject" :disabled="deleting">
              <span v-if="deleting" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
              {{ deleting ? 'Eliminazione in corso...' : 'Elimina' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else-if="loading" class="text-center py-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Caricamento...</span>
    </div>
    <p class="mt-2">Caricamento progetto...</p>
  </div>
  
  <div v-else class="alert alert-danger">
    Progetto non trovato o errore nel caricamento.
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';

const route = useRoute();
const router = useRouter();
const projectStore = useProjectStore();

const project = ref(null);
const loading = ref(true);
const showDeleteModal = ref(false);
const deleting = ref(false);

// Load project data when component mounts or route changes
onMounted(() => {
  loadProject();
});

watch(() => route.params.id, async (newId) => {
  if (newId) {
    await loadProject();
  }
});

async function loadProject() {
  try {
    loading.value = true;
    const projectId = route.params.id;
    project.value = await projectStore.fetchProject(projectId);
  } catch (error) {
    console.error('Error loading project:', error);
  } finally {
    loading.value = false;
  }
}

async function deleteProject() {
  try {
    deleting.value = true;
    await projectStore.deleteProject(project.value.id_prg);
    showDeleteModal.value = false;
    router.push('/projects');
  } catch (error) {
    console.error('Error deleting project:', error);
  } finally {
    deleting.value = false;
  }
}
</script>

<style scoped>
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.project-header h2 {
  margin: 0;
  color: #2c3e50;
}

.project-description {
  color: #6c757d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.project-tabs {
  margin-top: 2rem;
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 0;
}

.nav-link {
  color: #495057;
  border: 1px solid transparent;
  border-top-left-radius: 0.25rem;
  border-top-right-radius: 0.25rem;
  padding: 0.75rem 1.25rem;
  text-decoration: none;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}

.nav-link:hover {
  border-color: #e9ecef #e9ecef #dee2e6;
  color: #0056b3;
}

.nav-link.active {
  color: #495057;
  background-color: #fff;
  border-color: #dee2e6 #dee2e6 #fff;
  font-weight: 500;
}

.tab-content {
  background-color: #fff;
  border-color: #dee2e6;
  min-height: 200px;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
  background-color: #dc3545;
  border-color: #dc3545;
}

.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 500;
}

.modal-body {
  padding: 1.5rem;
  line-height: 1.6;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-close {
  background: transparent url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23000'%3e%3cpath d='M.293.293a1 1 0 011.414 0L8 6.586 14.293.293a1 1 0 111.414 1.414L9.414 8l6.293 6.293a1 1 0 01-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 01-1.414-1.414L6.586 8 .293 1.707a1 1 0 010-1.414z'/%3e%3c/svg%3e") center/1em auto no-repeat;
  border: 0;
  border-radius: 0.25rem;
  opacity: 0.5;
  padding: 0.5rem;
  margin: -0.5rem -0.5rem -0.5rem auto;
  cursor: pointer;
}

.btn-close:hover {
  opacity: 0.75;
  background-color: rgba(0, 0, 0, 0.05);
}

.spinner-border {
  width: 1.25rem;
  height: 1.25rem;
  border-width: 0.15em;
  vertical-align: middle;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
