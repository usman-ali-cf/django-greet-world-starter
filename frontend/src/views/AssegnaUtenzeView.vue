<template>
  <div class="container-fluid py-4">
    <div class="row">
      <!-- Left Column: Available Utilities -->
      <div class="col-md-6">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Utenze Disponibili</h5>
            <button 
              class="btn btn-sm btn-outline-secondary"
              @click="aggiornaUtenze"
            >
              <i class="fas fa-sync-alt me-1"></i>Aggiorna
            </button>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <input 
                type="text"
                class="form-control form-control-sm"
                placeholder="Cerca utenza..."
                v-model="filtroUtenze"
              >
            </div>
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Stato</th>
                    <th>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="utenza in utenzeFiltrate"
                    :key="utenza.id"
                    :class="{ 'table-active': utenza.selezionato }"
                  >
                    <td>{{ utenza.nome }}</td>
                    <td>
                      <span class="badge" :class="getTipoUtenzaBadge(utenza.tipo)">
                        {{ utenza.tipo }}
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatoBadge(utenza.stato)">
                        {{ getStatoLabel(utenza.stato) }}
                      </span>
                    </td>
                    <td>
                      <button 
                        class="btn btn-sm btn-outline-primary"
                        @click="selezionaUtenza(utenza)"
                      >
                        <i class="fas fa-check me-1"></i>Seleziona
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Selected Utilities -->
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Utenze Selezionate</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Stato</th>
                    <th>Modulo</th>
                    <th>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="utenza in utenzeSelezionate"
                    :key="utenza.id"
                  >
                    <td>{{ utenza.nome }}</td>
                    <td>
                      <span class="badge" :class="getTipoUtenzaBadge(utenza.tipo)">
                        {{ utenza.tipo }}
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatoBadge(utenza.stato)">
                        {{ getStatoLabel(utenza.stato) }}
                      </span>
                    </td>
                    <td>
                      <select 
                        class="form-select form-select-sm"
                        v-model="utenza.modulo"
                        @change="salvaAssegnazione(utenza)"
                      >
                        <option value="">Seleziona modulo...</option>
                        <option 
                          v-for="modulo in moduli"
                          :key="modulo.id"
                          :value="modulo.id"
                        >
                          {{ modulo.nome }} ({{ modulo.tipo }})
                        </option>
                      </select>
                    </td>
                    <td>
                      <button 
                        class="btn btn-sm btn-danger"
                        @click="rimuoviUtenza(utenza)"
                      >
                        <i class="fas fa-trash me-1"></i>Rimuovi
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Section: Actions -->
    <div class="mt-4">
      <button 
        class="btn btn-primary"
        @click="salvaAssegnazioni"
      >
        <i class="fas fa-save me-1"></i>Salva Assegnazioni
      </button>
      <button 
        class="btn btn-secondary ms-2"
        @click="annulla"
      >
        <i class="fas fa-times me-1"></i>Annulla
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/api';
import { useProjectStore } from '@/stores/project';

const projectStore = useProjectStore();

const utenze = ref([]);
const utenzeSelezionate = ref([]);
const moduli = ref([]);
const filtroUtenze = ref('');

// Computed properties
const utenzeFiltrate = computed(() => {
  if (!filtroUtenze.value) return utenze.value;
  return utenze.value.filter(utenza => 
    utenza.nome.toLowerCase().includes(filtroUtenze.value.toLowerCase())
  );
});

// Methods
async function caricaUtenze() {
  try {
    const response = await api.getAvailableUtilities();
    utenze.value = response.data.map(utenza => ({
      ...utenza,
      selezionato: false
    }));
  } catch (error) {
    console.error('Errore nel caricamento delle utenze:', error);
  }
}

async function caricaModuli() {
  try {
    const response = await api.getAvailableModules();
    moduli.value = response.data;
  } catch (error) {
    console.error('Errore nel caricamento dei moduli:', error);
  }
}

function selezionaUtenza(utenza) {
  const index = utenzeSelezionate.value.findIndex(u => u.id === utenza.id);
  if (index === -1) {
    utenzeSelezionate.value.push({
      ...utenza,
      modulo: null
    });
  }
}

function rimuoviUtenza(utenza) {
  const index = utenzeSelezionate.value.findIndex(u => u.id === utenza.id);
  if (index !== -1) {
    utenzeSelezionate.value.splice(index, 1);
  }
}

async function salvaAssegnazione(utenza) {
  if (!utenza.modulo) return;
  try {
    await api.assignUtility({
      utenza_id: utenza.id,
      modulo_id: utenza.modulo
    });
  } catch (error) {
    console.error('Errore nell\'assegnazione:', error);
  }
}

async function salvaAssegnazioni() {
  try {
    const assegnazioni = utenzeSelezionate.value
      .filter(u => u.modulo)
      .map(u => ({
        utenza_id: u.id,
        modulo_id: u.modulo
      }));

    await api.saveAssignments(assegnazioni);
    // Reset the form
    utenzeSelezionate.value = [];
    await caricaUtenze();
    await caricaModuli();
  } catch (error) {
    console.error('Errore nel salvataggio delle assegnazioni:', error);
  }
}

function annulla() {
  utenzeSelezionate.value = [];
}

async function aggiornaUtenze() {
  await caricaUtenze();
}

// Utility functions
function getTipoUtenzaBadge(tipo) {
  const badges = {
    'PLC': 'bg-primary',
    'IO_Remoto': 'bg-success',
    'Sensor': 'bg-info',
    'Actuator': 'bg-warning'
  };
  return badges[tipo] || 'bg-secondary';
}

function getStatoBadge(stato) {
  const badges = {
    'disponibile': 'bg-success',
    'assegnato': 'bg-primary',
    'inattivo': 'bg-warning',
    'errore': 'bg-danger'
  };
  return badges[stato] || 'bg-secondary';
}

function getStatoLabel(stato) {
  const labels = {
    'disponibile': 'Disponibile',
    'assegnato': 'Assegnato',
    'inattivo': 'Inattivo',
    'errore': 'Errore'
  };
  return labels[stato] || stato;
}

// Initialize data on component mount
onMounted(() => {
  caricaUtenze();
  caricaModuli();
});
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.table {
  margin-bottom: 0;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.075);
}

.table-active {
  background-color: rgba(0, 123, 255, 0.1);
}

.badge {
  padding: 0.35em 0.65em;
  font-size: 0.85rem;
}

.form-select {
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
}

.btn {
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-responsive {
    overflow-x: auto;
  }
  
  .btn-group {
    flex-wrap: wrap;
  }
  
  .btn-group .btn {
    margin-bottom: 0.5rem;
  }
}
</style>
