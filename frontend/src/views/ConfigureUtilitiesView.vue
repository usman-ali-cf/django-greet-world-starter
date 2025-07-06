<template>
  <div class="configure-utilities">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">Configurazione Utenze</h3>
      </div>
      <div class="card-body">
        <!-- Search and Filter Section -->
        <div class="row mb-4">
          <div class="col-md-6">
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-search"></i></span>
              <input 
                type="text" 
                class="form-control" 
                placeholder="Cerca utenza..."
                v-model="searchQuery"
                @input="filterUtilities"
              >
            </div>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filterCategory" @change="filterUtilities">
              <option value="">Tutte le categorie</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filterStatus" @change="filterUtilities">
              <option value="">Tutti gli stati</option>
              <option value="attivo">Attivo</option>
              <option value="disattivo">Disattivo</option>
            </select>
          </div>
        </div>
        
        <!-- Utilities Table -->
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Nome Utenza</th>
                <th>Categoria</th>
                <th>Stato</th>
                <th>Ultima Modifica</th>
                <th class="text-end">Azioni</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="6" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Caricamento...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="filteredUtilities.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">
                  Nessuna utenza trovata
                </td>
              </tr>
              <tr v-for="utility in filteredUtilities" :key="utility.id">
                <td>{{ utility.id }}</td>
                <td>{{ utility.nome }}</td>
                <td>
                  <span class="badge bg-secondary">{{ utility.categoria }}</span>
                </td>
                <td>
                  <span 
                    class="badge" 
                    :class="{ 'bg-success': utility.stato === 'attivo', 'bg-danger': utility.stato !== 'attivo' }"
                  >
                    {{ utility.stato === 'attivo' ? 'Attivo' : 'Disattivo' }}
                  </span>
                </td>
                <td>{{ formatDate(utility.ultima_modifica) }}</td>
                <td class="text-end">
                  <button 
                    class="btn btn-sm btn-outline-primary me-1"
                    @click="editUtility(utility)"
                    title="Modifica"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-danger"
                    @click="confirmDelete(utility)"
                    title="Elimina"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted">
            Mostrati {{ filteredUtilities.length }} di {{ totalUtilities }} utenze
          </div>
          <nav>
            <ul class="pagination mb-0">
              <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
                <button class="page-link" @click="changePage(currentPage - 1)">
                  <i class="fas fa-chevron-left"></i>
                </button>
              </li>
              <li 
                v-for="page in totalPages" 
                :key="page" 
                class="page-item"
                :class="{ 'active': page === currentPage }"
              >
                <button class="page-link" @click="changePage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ 'disabled': currentPage === totalPages }">
                <button class="page-link" @click="changePage(currentPage + 1)">
                  <i class="fas fa-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
        
        <!-- Add/Edit Utility Modal -->
        <div class="modal fade" :class="{ 'show d-block': showModal }" tabindex="-1" v-if="showModal">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">{{ isEditing ? 'Modifica Utenza' : 'Aggiungi Nuova Utenza' }}</h5>
                <button type="button" class="btn-close" @click="closeModal"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="saveUtility">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="nome" class="form-label">Nome Utenza</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        id="nome" 
                        v-model="formData.nome"
                        required
                      >
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="categoria" class="form-label">Categoria</label>
                      <select 
                        class="form-select" 
                        id="categoria" 
                        v-model="formData.categoria"
                        required
                      >
                        <option value="">Seleziona una categoria</option>
                        <option v-for="category in categories" :key="category" :value="category">
                          {{ category }}
                        </option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="stato" class="form-label">Stato</label>
                      <select 
                        class="form-select" 
                        id="stato" 
                        v-model="formData.stato"
                        required
                      >
                        <option value="attivo">Attivo</option>
                        <option value="disattivo">Disattivo</option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="priorita" class="form-label">Priorità</label>
                      <select 
                        class="form-select" 
                        id="priorita" 
                        v-model="formData.priorita"
                        required
                      >
                        <option value="bassa">Bassa</option>
                        <option value="media">Media</option>
                        <option value="alta">Alta</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="descrizione" class="form-label">Descrizione</label>
                    <textarea 
                      class="form-control" 
                      id="descrizione" 
                      v-model="formData.descrizione"
                      rows="3"
                    ></textarea>
                  </div>
                  
                  <div class="d-flex justify-content-end gap-2">
                    <button type="button" class="btn btn-secondary" @click="closeModal">
                      Annulla
                    </button>
                    <button type="submit" class="btn btn-primary" :disabled="saving">
                      <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                      {{ saving ? 'Salvataggio...' : 'Salva' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Delete Confirmation Modal -->
        <div class="modal fade" :class="{ 'show d-block': showDeleteModal }" tabindex="-1" v-if="showDeleteModal">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Conferma Eliminazione</h5>
                <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
              </div>
              <div class="modal-body">
                Sei sicuro di voler eliminare l'utenza "{{ selectedUtility?.nome }}"?
                Questa azione non può essere annullata.
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                  Annulla
                </button>
                <button 
                  type="button" 
                  class="btn btn-danger" 
                  @click="deleteUtility"
                  :disabled="deleting"
                >
                  <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
                  {{ deleting ? 'Eliminazione...' : 'Elimina' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card-footer bg-light">
        <button class="btn btn-primary" @click="addNewUtility">
          <i class="fas fa-plus me-2"></i>Aggiungi Utenza
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const route = useRoute();

// Data
const loading = ref(true);
const utilities = ref([]);
const categories = ref(['Elettrico', 'Idrico', 'Gas', 'Riscaldamento', 'Condizionamento']);
const searchQuery = ref('');
const filterCategory = ref('');
const filterStatus = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;
const showModal = ref(false);
const showDeleteModal = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const deleting = ref(false);
const selectedUtility = ref(null);

// Form data
const formData = ref({
  nome: '',
  categoria: '',
  stato: 'attivo',
  priorita: 'media',
  descrizione: ''
});

// Computed properties
const filteredUtilities = computed(() => {
  return utilities.value.filter(utility => {
    const matchesSearch = utility.nome.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         utility.descrizione?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCategory = !filterCategory.value || utility.categoria === filterCategory.value;
    const matchesStatus = !filterStatus.value || utility.stato === filterStatus.value;
    
    return matchesSearch && matchesCategory && matchesStatus;
  });
});

const totalUtilities = computed(() => filteredUtilities.value.length);
const totalPages = computed(() => Math.ceil(totalUtilities.value / itemsPerPage));

// Methods
function loadUtilities() {
  // Simulate API call
  loading.value = true;
  setTimeout(() => {
    // Mock data - replace with actual API call
    utilities.value = Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      nome: `Utenza ${i + 1}`,
      categoria: categories.value[Math.floor(Math.random() * categories.value.length)],
      stato: Math.random() > 0.3 ? 'attivo' : 'disattivo',
      priorita: ['bassa', 'media', 'alta'][Math.floor(Math.random() * 3)],
      descrizione: `Descrizione dell'utenza ${i + 1}`,
      ultima_modifica: new Date(Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000).toISOString()
    }));
    loading.value = false;
  }, 800);
}

function filterUtilities() {
  currentPage.value = 1; // Reset to first page when filters change
}

function changePage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

function addNewUtility() {
  isEditing.value = false;
  formData.value = {
    nome: '',
    categoria: '',
    stato: 'attivo',
    priorita: 'media',
    descrizione: ''
  };
  showModal.value = true;
}

function editUtility(utility) {
  isEditing.value = true;
  selectedUtility.value = utility;
  formData.value = { ...utility };
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedUtility.value = null;
}

async function saveUtility() {
  try {
    saving.value = true;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (isEditing.value) {
      // Update existing utility
      const index = utilities.value.findIndex(u => u.id === selectedUtility.value.id);
      if (index !== -1) {
        utilities.value[index] = { 
          ...formData.value, 
          id: selectedUtility.value.id,
          ultima_modifica: new Date().toISOString()
        };
      }
    } else {
      // Add new utility
      const newId = Math.max(0, ...utilities.value.map(u => u.id)) + 1;
      utilities.value.unshift({
        ...formData.value,
        id: newId,
        ultima_modifica: new Date().toISOString()
      });
    }
    
    showModal.value = false;
  } catch (error) {
    console.error('Error saving utility:', error);
  } finally {
    saving.value = false;
  }
}

function confirmDelete(utility) {
  selectedUtility.value = utility;
  showDeleteModal.value = true;
}

async function deleteUtility() {
  if (!selectedUtility.value) return;
  
  try {
    deleting.value = true;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Remove from local array
    const index = utilities.value.findIndex(u => u.id === selectedUtility.value.id);
    if (index !== -1) {
      utilities.value.splice(index, 1);
    }
    
    showDeleteModal.value = false;
    selectedUtility.value = null;
  } catch (error) {
    console.error('Error deleting utility:', error);
  } finally {
    deleting.value = false;
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Lifecycle hooks
onMounted(() => {
  loadUtilities();
});
</script>

<style scoped>
.configure-utilities {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
  border-radius: 0.5rem;
  overflow: hidden;
}

.card-header {
  padding: 1rem 1.5rem;
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.table {
  margin-bottom: 0;
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  color: #6c757d;
  border-bottom-width: 1px;
}

.table td {
  vertical-align: middle;
  padding: 1rem 0.75rem;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  border-radius: 0.25rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.2rem;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.15);
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
}

.modal-footer {
  border-top: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #495057;
}

.input-group-text {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.page-item.active .page-link {
  background-color: #3498db;
  border-color: #3498db;
}

.page-link {
  color: #3498db;
  border: 1px solid #dee2e6;
  padding: 0.375rem 0.75rem;
}

.page-link:hover {
  color: #1a6fb3;
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.spinner-border {
  width: 1.25rem;
  height: 1.25rem;
  border-width: 0.15em;
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
