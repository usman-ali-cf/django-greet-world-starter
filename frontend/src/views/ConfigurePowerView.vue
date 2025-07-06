<template>
  <div class="configure-power">
    <div class="card">
      <div class="card-body">
        <h2 class="mb-4">Configurazione Potenza</h2>
        
        <div class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          Configura i parametri di potenza per il progetto {{ project.nome_prg }}.
          <span v-if="hasUnsavedChanges" class="ms-2 text-warning">
            <i class="fas fa-exclamation-triangle me-1"></i>Modifiche non salvate
          </span>
        </div>
        
        <form @submit.prevent="saveConfiguration">
          <div class="row">
            <div class="col-md-6">
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h5 class="mb-0">Parametri Generali</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="tensione" class="form-label">Tensione di Rete (V)</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="tensione" 
                        v-model.number="formData.tensione"
                        min="0"
                        step="0.1"
                        required
                      >
                      <span class="input-group-text">V</span>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="frequenza" class="form-label">Frequenza di Rete</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="frequenza" 
                        v-model.number="formData.frequenza"
                        min="0"
                        step="0.1"
                        required
                      >
                      <span class="input-group-text">Hz</span>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="potenza_contrattuale" class="form-label">Potenza Contrattuale</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="potenza_contrattuale" 
                        v-model.number="formData.potenza_contrattuale"
                        min="0"
                        step="0.1"
                        required
                      >
                      <span class="input-group-text">kW</span>
                    </div>
                    <div class="form-text">
                      La potenza disponibile in base al contratto con il fornitore di energia
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h5 class="mb-0">Fattori di Potenza</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="fattore_potenza_min" class="form-label">Fattore di Potenza Minimo</label>
                    <input 
                      type="range" 
                      class="form-range" 
                      id="fattore_potenza_min" 
                      v-model.number="formData.fattore_potenza_min"
                      min="0.7" 
                      max="1" 
                      step="0.01"
                    >
                    <div class="d-flex justify-content-between">
                      <span>0,70</span>
                      <span class="fw-bold">{{ formData.fattore_potenza_min.toFixed(2) }}</span>
                      <span>1,00</span>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="fattore_potenza_obiettivo" class="form-label">Fattore di Potenza Obiettivo</label>
                    <input 
                      type="range" 
                      class="form-range" 
                      id="fattore_potenza_obiettivo" 
                      v-model.number="formData.fattore_potenza_obiettivo"
                      min="0.9" 
                      max="1" 
                      step="0.01"
                    >
                    <div class="d-flex justify-content-between">
                      <span>0,90</span>
                      <span class="fw-bold">{{ formData.fattore_potenza_obiettivo.toFixed(2) }}</span>
                      <span>1,00</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h5 class="mb-0">Soglie di Intervento</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="soglia_preallarme" class="form-label">Soglia di Preallarme</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="soglia_preallarme" 
                        v-model.number="formData.soglia_preallarme"
                        min="0" 
                        max="100" 
                        step="1"
                        required
                      >
                      <span class="input-group-text">%</span>
                    </div>
                    <div class="form-text">
                      Percentuale della potenza contrattuale alla quale attivare il preallarme
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="soglia_allarme" class="form-label">Soglia di Allarme</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="soglia_allarme" 
                        v-model.number="formData.soglia_allarme"
                        min="0" 
                        max="100" 
                        step="1"
                        required
                      >
                      <span class="input-group-text">%</span>
                    </div>
                    <div class="form-text">
                      Percentuale della potenza contrattuale alla quale attivare l'allarme
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="soglia_sovraccarico" class="form-label">Soglia di Sovraccarico</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        id="soglia_sovraccarico" 
                        v-model.number="formData.soglia_sovraccarico"
                        min="0" 
                        max="100" 
                        step="1"
                        required
                      >
                      <span class="input-group-text">%</span>
                    </div>
                    <div class="form-text">
                      Percentuale della potenza contrattuale alla quale attivare l'intervento automatico
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="card mb-4">
                <div class="card-header bg-light">
                  <h5 class="mb-0">Tariffa Energetica</h5>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="tipo_tariffa" class="form-label">Tipo di Tariffa</label>
                    <select 
                      class="form-select" 
                      id="tipo_tariffa" 
                      v-model="formData.tipo_tariffa"
                      required
                    >
                      <option value="monoraria">Monoraria</option>
                      <option value="bioraria">Bioraria</option>
                      <option value="trioraria">Trioraria</option>
                    </select>
                  </div>
                  
                  <div v-if="formData.tipo_tariffa !== 'monoraria'" class="mb-3">
                    <label class="form-label">Fasce Orarie</label>
                    
                    <div v-if="formData.tipo_tariffa === 'bioraria'" class="fasce-orarie">
                      <div class="row mb-2">
                        <div class="col-4">
                          <label class="form-label small">F1 (P1)</label>
                          <div class="input-group input-group-sm">
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F1.inizio"
                              @change="validateTimeRange('F1')"
                            >
                            <span class="input-group-text">-</span>
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F1.fine"
                              @change="validateTimeRange('F1')"
                            >
                          </div>
                        </div>
                        <div class="col-4">
                          <label class="form-label small">F2 (P2)</label>
                          <div class="input-group input-group-sm">
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F2.inizio"
                              @change="validateTimeRange('F2')"
                            >
                            <span class="input-group-text">-</span>
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F2.fine"
                              @change="validateTimeRange('F2')"
                            >
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div v-else-if="formData.tipo_tariffa === 'trioraria'" class="fasce-orarie">
                      <div class="row mb-2">
                        <div class="col-4">
                          <label class="form-label small">F1 (P1)</label>
                          <div class="input-group input-group-sm">
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F1.inizio"
                              @change="validateTimeRange('F1')"
                            >
                            <span class="input-group-text">-</span>
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F1.fine"
                              @change="validateTimeRange('F1')"
                            >
                          </div>
                        </div>
                        <div class="col-4">
                          <label class="form-label small">F2 (P2)</label>
                          <div class="input-group input-group-sm">
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F2.inizio"
                              @change="validateTimeRange('F2')"
                            >
                            <span class="input-group-text">-</span>
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F2.fine"
                              @change="validateTimeRange('F2')"
                            >
                          </div>
                        </div>
                        <div class="col-4">
                          <label class="form-label small">F3 (P3)</label>
                          <div class="input-group input-group-sm">
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F3.inizio"
                              @change="validateTimeRange('F3')"
                            >
                            <span class="input-group-text">-</span>
                            <input 
                              type="time" 
                              class="form-control form-control-sm" 
                              v-model="formData.fasce_orarie.F3.fine"
                              @change="validateTimeRange('F3')"
                            >
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="mb-3">
                    <label class="form-label">Costi per Fascia (€/kWh)</label>
                    <div v-if="formData.tipo_tariffa === 'monoraria'" class="input-group">
                      <span class="input-group-text">F1</span>
                      <input 
                        type="number" 
                        class="form-control" 
                        v-model.number="formData.costi_fascia.F1"
                        min="0"
                        step="0.0001"
                        required
                      >
                      <span class="input-group-text">€/kWh</span>
                    </div>
                    
                    <template v-else>
                      <div class="input-group mb-2">
                        <span class="input-group-text">F1</span>
                        <input 
                          type="number" 
                          class="form-control" 
                          v-model.number="formData.costi_fascia.F1"
                          min="0"
                          step="0.0001"
                          required
                        >
                        <span class="input-group-text">€/kWh</span>
                      </div>
                      
                      <div class="input-group mb-2">
                        <span class="input-group-text">F2</span>
                        <input 
                          type="number" 
                          class="form-control" 
                          v-model.number="formData.costi_fascia.F2"
                          min="0"
                          step="0.0001"
                          required
                        >
                        <span class="input-group-text">€/kWh</span>
                      </div>
                      
                      <div v-if="formData.tipo_tariffa === 'trioraria'" class="input-group">
                        <span class="input-group-text">F3</span>
                        <input 
                          type="number" 
                          class="form-control" 
                          v-model.number="formData.costi_fascia.F3"
                          min="0"
                          step="0.0001"
                          required
                        >
                        <span class="input-group-text">€/kWh</span>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button 
              type="button" 
              class="btn btn-outline-secondary"
              @click="resetForm"
              :disabled="saving"
            >
              <i class="fas fa-undo me-1"></i>Annulla Modifiche
            </button>
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="!hasUnsavedChanges || saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
              <i v-else class="fas fa-save me-1"></i>
              {{ saving ? 'Salvataggio in corso...' : 'Salva Configurazione' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const route = useRoute();
const projectStore = useProjectStore();

// Form data with default values
const defaultFormData = {
  tensione: 400,
  frequenza: 50,
  potenza_contrattuale: 30,
  fattore_potenza_min: 0.85,
  fattore_potenza_obiettivo: 0.95,
  soglia_preallarme: 80,
  soglia_allarme: 90,
  soglia_sovraccarico: 95,
  tipo_tariffa: 'monoraria',
  fasce_orarie: {
    F1: { inizio: '00:00', fine: '23:59' },
    F2: { inizio: '00:00', fine: '23:59' },
    F3: { inizio: '00:00', fine: '23:59' }
  },
  costi_fascia: {
    F1: 0.2,
    F2: 0.15,
    F3: 0.1
  }
};

const originalFormData = ref(JSON.parse(JSON.stringify(defaultFormData)));
const formData = ref(JSON.parse(JSON.stringify(defaultFormData)));
const saving = ref(false);

// Computed properties
const hasUnsavedChanges = computed(() => {
  return JSON.stringify(formData.value) !== JSON.stringify(originalFormData.value);
});

// Methods
async function loadConfiguration() {
  try {
    // Simulate API call to load configuration
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // In a real app, you would fetch this from your API
    // const config = await projectStore.getPowerConfiguration(props.project.id_prg);
    // if (config) {
    //   formData.value = { ...defaultFormData, ...config };
    //   originalFormData.value = JSON.parse(JSON.stringify(formData.value));
    // }
    
  } catch (error) {
    console.error('Error loading power configuration:', error);
  }
}

async function saveConfiguration() {
  try {
    saving.value = true;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // In a real app, you would save to your API
    // await projectStore.savePowerConfiguration(props.project.id_prg, formData.value);
    
    // Update original data after successful save
    originalFormData.value = JSON.parse(JSON.stringify(formData.value));
    
    // Show success message
    // You might want to use a toast or notification component here
    alert('Configurazione salvata con successo!');
    
  } catch (error) {
    console.error('Error saving power configuration:', error);
    alert('Errore durante il salvataggio della configurazione. Riprovare.');
  } finally {
    saving.value = false;
  }
}

function resetForm() {
  if (confirm('Annullare tutte le modifiche?')) {
    formData.value = JSON.parse(JSON.stringify(originalFormData.value));
  }
}

function validateTimeRange(fascia) {
  const fasciaData = formData.value.fasce_orarie[fascia];
  if (fasciaData.inizio >= fasciaData.fine) {
    alert(`L'orario di inizio per la fascia ${fascia} deve essere precedente all'orario di fine`);
    // Reset to default values if invalid
    fasciaData.inizio = '00:00';
    fasciaData.fine = '23:59';
  }
}

// Watch for tariff type changes to update time ranges
watch(() => formData.value.tipo_tariffa, (newVal) => {
  // Reset time ranges when tariff type changes
  if (newVal === 'monoraria') {
    formData.value.fasce_orarie.F1 = { inizio: '00:00', fine: '23:59' };
  } else if (newVal === 'bioraria') {
    formData.value.fasce_orarie.F1 = { inizio: '08:00', fine: '19:00' };
    formData.value.fasce_orarie.F2 = { inizio: '19:00', fine: '08:00' };
  } else if (newVal === 'trioraria') {
    formData.value.fasce_orarie.F1 = { inizio: '08:00', fine: '19:00' };
    formData.value.fasce_orarie.F2 = { inizio: '07:00', fine: '08:00' };
    formData.value.fasce_orarie.F3 = { inizio: '19:00', fine: '23:00' };
  }
});

// Lifecycle hooks
onMounted(() => {
  loadConfiguration();
});
</script>

<style scoped>
.configure-power {
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

.form-range::-webkit-slider-thumb {
  background: #3498db;
}

.form-range::-moz-range-thumb {
  background: #3498db;
}

.form-range::-ms-thumb {
  background: #3498db;
}

.input-group-text {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  min-width: 2.5rem;
  justify-content: center;
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

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  border-color: #bdc3c7;
  opacity: 0.8;
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

.alert {
  border: none;
  border-radius: 0.5rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.alert-info {
  background-color: #e3f2fd;
  color: #0d6efd;
}

.alert i {
  font-size: 1.25rem;
  margin-right: 0.5rem;
}

.text-warning {
  color: #ffc107 !important;
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

.fasce-orarie .form-control-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.fasce-orarie .input-group-text {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

.small {
  font-size: 0.75rem;
  font-weight: 500;
}
</style>
