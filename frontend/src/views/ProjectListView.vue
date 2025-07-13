<template>
  <div class="container mt-4">
    <header class="d-flex justify-content-between align-items-center mb-4">
      <h1>Gestione Progetto</h1>
      <router-link to="/projects/new" class="btn btn-primary">
        <i class="fas fa-plus"></i> Nuovo Progetto
      </router-link>
    </header>

    <main>
      <h2>Seleziona un progetto o creane uno nuovo</h2>

      <section>
        <h3>Progetti disponibili</h3>

        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Caricamento...</span>
          </div>
        </div>

        <div v-else>
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Nome progetto</th>
                <th>Descrizione</th>
                <th class="text-center">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="project in projects.data" :key="project.id_prg">
                <td>
                  <router-link :to="`/projects/${project.id_prg}`" class="text-decoration-none">
                    {{ project.name }}
                  </router-link>
                </td>
                <td>{{ project.description || 'Nessuna descrizione' }}</td>
                <td class="text-center">
                  <div class="btn-group" role="group">
                    <router-link 
                      :to="`/projects/${project.id_prg}`" 
                      class="btn btn-sm btn-outline-primary"
                      title="Modifica"
                    >
                      <i class="fas fa-edit"></i>
                    </router-link>
                    <button 
                      @click="confirmDelete(project)" 
                      class="btn btn-sm btn-outline-danger"
                      title="Elimina"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!loading && projects.data.length === 0">
                <td colspan="3" class="text-center text-muted py-4">
                  Nessun progetto trovato
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Conferma eliminazione</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            Sei sicuro di voler eliminare il progetto "{{ projectToDelete?.name }}"?
            Questa azione non può essere annullata.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Annulla</button>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="deleteProject"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              {{ deleting ? 'Eliminazione in corso...' : 'Elimina' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectStore } from '@/stores/project';

const route = useRoute();
const router = useRouter();
const projectStore = useProjectStore();

const projects = ref({ data: [] });
const loading = ref(false);
const showDeleteModal = ref(false);
const deleting = ref(false);
const projectToDelete = ref(null);

// Load projects when component mounts
const fetchProjects = async () => {
  try {
    loading.value = true;
    const response = await projectStore.fetchProjects();
    projects.value = response.data;
  } catch (error) {
    console.error('Error fetching projects:', error);
  } finally {
    loading.value = false;
  }
};

// Confirm project deletion
const confirmDelete = (project) => {
  projectToDelete.value = project;
  showDeleteModal.value = true;
};

// Delete project
const deleteProject = async () => {
  if (!projectToDelete.value) return;
  
  try {
    deleting.value = true;
    await projectStore.deleteProject(projectToDelete.value.id_prg);
    await fetchProjects();
    showDeleteModal.value = false;
  } catch (error) {
    console.error('Error deleting project:', error);
  } finally {
    deleting.value = false;
  }
};

// Initialize component
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

h1 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin: 0;
}

h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin: 1.5rem 0 1rem;
}

h3 {
  color: #2c3e50;
  font-size: 1.25rem;
  margin: 1.5rem 0 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

tr:hover {
  background-color: #f8f9fa;
}

.btn-group .btn {
  margin: 0 2px;
}

.modal-content {
  border: none;
  border-radius: 0.5rem;
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
  padding: 1rem;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
  padding: 1rem;
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
