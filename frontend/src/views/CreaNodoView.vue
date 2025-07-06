<template>
  <div class="crea-nodo">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">Crea Nuovo Nodo</h3>
      </div>
      <div class="card-body">
        <div v-if="successMessage" class="alert alert-success">
          <i class="fas fa-check-circle me-2"></i>
          {{ successMessage }}
        </div>
        
        <form @submit.prevent="submitForm">
          <div class="row">
            <div class="col-md-6">
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h5 class="mb-0">Dati Nodo</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="nome_nodo" class="form-label">Nome Nodo</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="nome_nodo" 
                      v-model="formData.nome_nodo"
                      required
                      :class="{ 'is-invalid': errors.nome_nodo }"
                    >
                    <div class="invalid-feedback">{{ errors.nome_nodo }}</div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="tipo_nodo" class="form-label">Tipo Nodo</label>
                    <select 
                      class="form-select" 
                      id="tipo_nodo" 
                      v-model="formData.tipo_nodo"
                      required
                      :class="{ 'is-invalid': errors.tipo_nodo }"
                    >
                      <option value="">Seleziona un tipo</option>
                      <option value="plc">PLC</option>
                      <option value="hmi">HMI</option>
                      <option value="remoto">Remoto I/O</option>
                      <option value="altro">Altro</option>
                    </select>
                    <div class="invalid-feedback">{{ errors.tipo_nodo }}</div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="indirizzo_ip" class="form-label">Indirizzo IP</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="indirizzo_ip" 
                      v-model="formData.indirizzo_ip"
                      placeholder="Es: 192.168.1.100"
                      :class="{ 'is-invalid': errors.indirizzo_ip }"
                    >
                    <div class="invalid-feedback">{{ errors.indirizzo_ip }}</div>
                    <div class="form-text">Lascia vuoto per configurazione DHCP</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="card mb-4">
                <div class="card-header bg-light d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">Moduli Hardware</h5>
                  <button 
                    type="button" 
                    class="btn btn-sm btn-outline-primary"
                    @click="addHardwareModule"
                  >
                    <i class="fas fa-plus me-1"></i>Aggiungi Modulo
                  </button>
                </div>
                <div class="card-body">
                  <div v-if="formData.moduli.length === 0" class="text-center py-4 text-muted">
                    <i class="fas fa-cube fa-2x mb-2 d-block"></i>
                    <p class="mb-0">Nessun modulo hardware aggiunto</p>
                  </div>
                  
                  <div v-else>
                    <div 
                      v-for="(modulo, index) in formData.moduli" 
                      :key="index"
                      class="card mb-3"
                    >
                      <div class="card-header py-2 bg-light d-flex justify-content-between align-items-center">
                        <span>Modulo #{{ index + 1 }}</span>
                        <button 
                          type="button" 
                          class="btn btn-sm btn-outline-danger"
                          @click="removeHardwareModule(index)"
                        >
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                      <div class="card-body">
                        <div class="mb-3">
                          <label :for="'modulo_hw_' + index" class="form-label small">Tipo Modulo</label>
                          <select 
                            class="form-select form-select-sm" 
                            :id="'modulo_hw_' + index"
                            v-model="modulo.id_hw"
                            required
                          >
                            <option value="">Seleziona un modulo</option>
                            <option 
                              v-for="hw in hardwareCatalog" 
                              :key="hw.id_hw" 
                              :value="hw.id_hw"
                            >
                              {{ hw.descrizione }} ({{ hw.codice }})
                            </option>
                          </select>
                        </div>
                        <div class="mb-2">
                          <label :for="'posizione_' + index" class="form-label small">Posizione Rack</label>
                          <input 
                            type="number" 
                            class="form-control form-control-sm" 
                            :id="'posizione_' + index"
                            v-model.number="modulo.posizione"
                            min="1"
                            required
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-between">
            <button 
              type="button" 
              class="btn btn-outline-secondary"
              @click="$router.go(-1)"
            >
              <i class="fas fa-arrow-left me-1"></i>Indietro
            </button>
            <div>
              <button 
                type="button" 
                class="btn btn-outline-secondary me-2"
                @click="resetForm"
              >
                <i class="fas fa-undo me-1"></i>Annulla
              </button>
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="saving"
              >
                <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="fas fa-save me-1"></i>
                {{ saving ? 'Salvataggio in corso...' : 'Salva Nodo' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Modal Aggiungi Modulo -->
    <div class="modal fade" :class="{ 'show d-block': showAddModuleModal }" tabindex="-1" v-if="showAddModuleModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Aggiungi Modulo Hardware</h5>
            <button type="button" class="btn-close" @click="showAddModuleModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="new_module_type" class="form-label">Seleziona Modulo</label>
              <select 
                class="form-select" 
                id="new_module_type" 
                v-model="newModule.id_hw"
                required
              >
                <option value="">Seleziona un modulo</option>
                <option 
                  v-for="hw in hardwareCatalog" 
                  :key="hw.id_hw" 
                  :value="hw.id_hw"
                >
                  {{ hw.descrizione }} ({{ hw.codice }})
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="module_position" class="form-label">Posizione Rack</label>
              <input 
                type="number" 
                class="form-control" 
                id="module_position" 
                v-model.number="newModule.posizione"
                min="1"
                required
              >
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddModuleModal = false">Annulla</button>
            <button type="button" class="btn btn-primary" @click="confirmAddModule">Aggiungi</button>
          </div>
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

// Form data
const formData = ref({
  id_prg: route.params.id,
  nome_nodo: '',
  tipo_nodo: 'plc',
  indirizzo_ip: '',
  note: '',
  moduli: []
});

const newModule = ref({
  id_hw: '',
  posizione: 1
});

const hardwareCatalog = ref([]);
const showAddModuleModal = ref(false);
const saving = ref(false);
const successMessage = ref('');
const errors = ref({});

// Load hardware catalog
async function loadHardwareCatalog() {
  try {
    const response = await api.getHardwareCatalog();
    hardwareCatalog.value = response.data;
  } catch (error) {
    console.error('Error loading hardware catalog:', error);
  }
}

// Form submission
async function submitForm() {
  try {
    saving.value = true;
    errors.value = {};
    
    // Basic validation
    if (!formData.value.nome_nodo.trim()) {
      errors.value.nome_nodo = 'Il nome del nodo è obbligatorio';
      return;
    }
    
    // IP validation if provided
    if (formData.value.indirizzo_ip && !isValidIP(formData.value.indirizzo_ip)) {
      errors.value.indirizzo_ip = 'Inserire un indirizzo IP valido';
      return;
    }
    
    // Prepare data for API
    const payload = {
      ...formData.value,
      // Ensure moduli is an array of objects with the correct structure
      moduli: formData.value.moduli.map(modulo => ({
        id_hw: parseInt(modulo.id_hw),
        posizione: parseInt(modulo.posizione) || 1
      }))
    };
    
    // Call API to create node
    const response = await api.createNode(payload);
    
    // Show success message
    successMessage.value = `Nodo "${formData.value.nome_nodo}" creato con successo!`;
    
    // Reset form after a delay
    setTimeout(() => {
      resetForm();
      // Redirect to node list or project detail after creation
      router.push(`/project/${route.params.id}`);
    }, 1500);
    
  } catch (error) {
    console.error('Error creating node:', error);
    // Handle API validation errors
    if (error.response && error.response.data && error.response.data.errors) {
      errors.value = error.response.data.errors;
    } else {
      alert('Si è verificato un errore durante il salvataggio del nodo.');
    }
  } finally {
    saving.value = false;
  }
}

// Reset form
function resetForm() {
  formData.value = {
    id_prg: route.params.id,
    nome_nodo: '',
    tipo_nodo: 'plc',
    indirizzo_ip: '',
    note: '',
    moduli: []
  };
  errors.value = {};
  successMessage.value = '';
}

// Hardware module management
function addHardwareModule() {
  // Reset new module form
  newModule.value = {
    id_hw: '',
    posizione: formData.value.moduli.length > 0 
      ? Math.max(...formData.value.moduli.map(m => m.posizione)) + 1 
      : 1
  };
  showAddModuleModal.value = true;
}

function confirmAddModule() {
  if (!newModule.value.id_hw) return;
  
  // Find the selected hardware details
  const hw = hardwareCatalog.value.find(h => h.id_hw == newModule.value.id_hw);
  
  if (hw) {
    formData.value.moduli.push({
      ...newModule.value,
      descrizione: hw.descrizione,
      codice: hw.codice
    });
    
    // Sort modules by position
    formData.value.moduli.sort((a, b) => a.posizione - b.posizione);
    
    showAddModuleModal.value = false;
  }
}

function removeHardwareModule(index) {
  if (confirm('Sei sicuro di voler rimuovere questo modulo?')) {
    formData.value.moduli.splice(index, 1);
  }
}

// Helper function to validate IP address
function isValidIP(ip) {
  const pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
  if (!pattern.test(ip)) return false;
  
  return ip.split('.').every(segment => {
    const num = parseInt(segment, 10);
    return num >= 0 && num <= 255;
  });
}

// Lifecycle hooks
onMounted(() => {
  loadHardwareCatalog();
});
</script>

<style scoped>
.crea-nodo {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.card-header {
  padding: 1rem 1.5rem;
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-body {
  padding: 1.5rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #495057;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  padding: 0.5rem 1.25rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.2rem;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #dee2e6;
  background-color: transparent;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
  background-color: transparent;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
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

.alert {
  border: none;
  border-radius: 0.5rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.alert-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.alert i {
  font-size: 1.25rem;
  margin-right: 0.5rem;
}

.spinner-border {
  width: 1.25rem;
  height: 1.25rem;
  border-width: 0.15em;
}

.form-text {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.small {
  font-size: 0.75rem;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .card-body {
    padding: 1rem;
  }
  
  .btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.875rem;
  }
}
</style>
