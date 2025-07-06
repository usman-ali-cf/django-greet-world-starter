<template>
  <div class="assegna-io">
    <div class="container-fluid">
      <div class="row">
        <!-- Left Column: Unassigned IO -->
        <div class="col-md-5">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">I/O Non Assegnati</h5>
              <button 
                class="btn btn-sm btn-outline-secondary"
                @click="aggiornaIO"
              >
                <i class="fas fa-sync-alt me-1"></i>Aggiorna IO
              </button>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="form-check form-check-inline">
                  <input 
                    class="form-check-input"
                    type="checkbox"
                    id="selectAllUnassigned"
                    @change="selectAllUnassigned"
                  >
                  <label class="form-check-label" for="selectAllUnassigned">Seleziona Tutto</label>
                </div>
                <div class="ms-2">
                  <input 
                    type="text"
                    class="form-control form-control-sm"
                    placeholder="Filtra per Commento IO"
                    v-model="filtroUnassigned"
                  >
                </div>
              </div>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Commento IO</th>
                      <th>Indirizzo</th>
                      <th>Tipo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="io in ioNonAssegnatiFiltrati"
                      :key="io.id"
                      :class="{ 'table-active': io.selezionato }"
                    >
                      <td>
                        <div class="form-check">
                          <input 
                            class="form-check-input"
                            type="checkbox"
                            :id="`io-${io.id}`"
                            :value="io.id"
                            v-model="io.selezionato"
                          >
                        </div>
                      </td>
                      <td>{{ io.commento }}</td>
                      <td>{{ io.indirizzo }}</td>
                      <td>
                        <span class="badge" :class="getTipoIOBadge(io.tipo)">{{ io.tipo }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Middle Column: Actions -->
        <div class="col-md-2 d-flex flex-column align-items-center">
          <button 
            class="btn btn-success w-100 mb-2"
            @click="assegnaSelezionati"
            :disabled="!ioSelezionati.length"
          >
            <i class="fas fa-arrow-right me-1"></i>Assegna
          </button>
          <button 
            class="btn btn-danger w-100"
            @click="rimuoviSelezionati"
            :disabled="!ioAssegnatiSelezionati.length"
          >
            <i class="fas fa-arrow-left me-1"></i>Rimuovi
          </button>
        </div>

        <!-- Right Column: Assigned IO -->
        <div class="col-md-5">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">I/O Assegnati al Modulo</h5>
              <div class="btn-group">
                <button 
                  class="btn btn-sm btn-outline-secondary"
                  @click="selectAllAssigned"
                >
                  Seleziona Tutto
                </button>
                <button 
                  class="btn btn-sm btn-outline-secondary"
                  @click="deselectAllAssigned"
                >
                  Deseleziona Tutto
                </button>
              </div>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <input 
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Filtra per Commento IO"
                  v-model="filtroAssigned"
                >
              </div>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Commento IO</th>
                      <th>Indirizzo</th>
                      <th>Modulo</th>
                      <th>Slot</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="io in ioAssegnatiFiltrati"
                      :key="io.id"
                      :class="{ 'table-active': io.selezionato }"
                    >
                      <td>
                        <div class="form-check">
                          <input 
                            class="form-check-input"
                            type="checkbox"
                            :id="`assigned-io-${io.id}`"
                            :value="io.id"
                            v-model="io.selezionato"
                          >
                        </div>
                      </td>
                      <td>{{ io.commento }}</td>
                      <td>{{ io.indirizzo }}</td>
                      <td>
                        <span class="badge bg-primary">{{ io.modulo }}</span>
                      </td>
                      <td>{{ io.slot }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Section: Node and Module Selection -->
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">Moduli (Hardware) del Nodo</h5>
        </div>
        <div class="card-body">
          <div class="d-flex align-items-center mb-3">
            <select 
              class="form-select me-2"
              v-model="nodoSelezionato"
              @change="caricaModuli"
            >
              <option value="">Seleziona un nodo...</option>
              <option 
                v-for="nodo in nodi"
                :key="nodo.id"
                :value="nodo.id"
              >
                {{ nodo.nome }}
              </option>
            </select>
            <button 
              class="btn btn-sm btn-outline-secondary me-2"
              @click="aggiornaNodi"
            >
              <i class="fas fa-sync-alt me-1"></i>Aggiorna Nodi
            </button>
            <button 
              class="btn btn-info me-2"
              @click="assegnazioneAutomatica"
            >
              <i class="fas fa-magic me-1"></i>Assegnazione automatica
            </button>
            <button 
              class="btn btn-warning me-2"
              @click="exportIO"
            >
              <i class="fas fa-file-excel me-1"></i>Esporta Excel
            </button>
            <button 
              class="btn btn-primary"
              @click="generaSchema"
            >
              <i class="fas fa-file-alt me-1"></i>Genera Schema Elettrico
            </button>
          </div>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Slot</th>
                  <th>Nome HW</th>
                  <th>Tipo</th>
                  <th>Indirizzo</th>
                  <th>I/O Assegnati</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="modulo in moduli" :key="modulo.id">
                  <td>{{ modulo.slot }}</td>
                  <td>{{ modulo.nome }}</td>
                  <td>
                    <span class="badge" :class="getTipoModuloBadge(modulo.tipo)">
                      {{ modulo.tipo }}
                    </span>
                  </td>
                  <td>{{ modulo.indirizzo }}</td>
                  <td>
                    <span class="badge bg-success">
                      {{ modulo.ioAssegnati || 0 }}/{{ modulo.ioTotali }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/api';

const ioNonAssegnati = ref([]);
const ioAssegnati = ref([]);
const nodi = ref([]);
const moduli = ref([]);
const nodoSelezionato = ref(null);
const filtroUnassigned = ref('');
const filtroAssigned = ref('');

// Computed properties
const ioNonAssegnatiFiltrati = computed(() => {
  if (!filtroUnassigned.value) return ioNonAssegnati.value;
  return ioNonAssegnati.value.filter(io => 
    io.commento.toLowerCase().includes(filtroUnassigned.value.toLowerCase())
  );
});

const ioAssegnatiFiltrati = computed(() => {
  if (!filtroAssigned.value) return ioAssegnati.value;
  return ioAssegnati.value.filter(io => 
    io.commento.toLowerCase().includes(filtroAssigned.value.toLowerCase())
  );
});

const ioSelezionati = computed(() => 
  ioNonAssegnati.value.filter(io => io.selezionato)
);

const ioAssegnatiSelezionati = computed(() => 
  ioAssegnati.value.filter(io => io.selezionato)
);

// Methods
async function caricaIO() {
  try {
    const response = await api.getUnassignedIO();
    ioNonAssegnati.value = response.data.map(io => ({
      ...io,
      selezionato: false
    }));
  } catch (error) {
    console.error('Errore nel caricamento degli IO:', error);
  }
}

async function caricaNodi() {
  try {
    const response = await api.getNodes();
    nodi.value = response.data;
  } catch (error) {
    console.error('Errore nel caricamento dei nodi:', error);
  }
}

async function caricaModuli() {
  if (!nodoSelezionato.value) return;
  try {
    const response = await api.getHardwareByNode(nodoSelezionato.value);
    moduli.value = response.data;
    // Carica anche gli IO assegnati per questo nodo
    await caricaIOAssegnati();
  } catch (error) {
    console.error('Errore nel caricamento dei moduli:', error);
  }
}

async function caricaIOAssegnati() {
  try {
    const response = await api.getAssignedIO(nodoSelezionato.value);
    ioAssegnati.value = response.data.map(io => ({
      ...io,
      selezionato: false
    }));
  } catch (error) {
    console.error('Errore nel caricamento degli IO assegnati:', error);
  }
}

function selectAllUnassigned() {
  const selected = !ioNonAssegnati.value.some(io => !io.selezionato);
  ioNonAssegnati.value.forEach(io => io.selezionato = !selected);
}

function selectAllAssigned() {
  ioAssegnati.value.forEach(io => io.selezionato = true);
}

function deselectAllAssigned() {
  ioAssegnati.value.forEach(io => io.selezionato = false);
}

async function assegnaSelezionati() {
  if (!nodoSelezionato.value || !ioSelezionati.value.length) return;
  try {
    await api.assignIO({
      nodo_id: nodoSelezionato.value,
      io_ids: ioSelezionati.value.map(io => io.id)
    });
    // Aggiorna gli stati locali
    ioSelezionati.value.forEach(io => io.selezionato = false);
    await caricaIO();
    await caricaIOAssegnati();
  } catch (error) {
    console.error('Errore nell\'assegnazione degli IO:', error);
  }
}

async function rimuoviSelezionati() {
  if (!ioAssegnatiSelezionati.value.length) return;
  try {
    await api.removeIO({
      io_ids: ioAssegnatiSelezionati.value.map(io => io.id)
    });
    // Aggiorna gli stati locali
    ioAssegnatiSelezionati.value.forEach(io => io.selezionato = false);
    await caricaIO();
    await caricaIOAssegnati();
  } catch (error) {
    console.error('Errore nella rimozione degli IO:', error);
  }
}

async function aggiornaIO() {
  await caricaIO();
}

async function aggiornaNodi() {
  await caricaNodi();
}

async function assegnazioneAutomatica() {
  if (!nodoSelezionato.value) return;
  try {
    await api.assignIOAutomatically(nodoSelezionato.value);
    await caricaIO();
    await caricaIOAssegnati();
  } catch (error) {
    console.error('Errore nell\'assegnazione automatica:', error);
  }
}

async function exportIO() {
  try {
    const response = await api.exportIO();
    // Gestisci il download del file
    const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'io_assegnati.xlsx';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Errore nell\'esportazione:', error);
  }
}

async function generaSchema() {
  try {
    const response = await api.generaSchema();
    // Gestisci il download del file
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'schema_elettrico.pdf';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Errore nella generazione del schema:', error);
  }
}

// Utility functions
function getTipoIOBadge(tipo) {
  const badges = {
    'input': 'bg-success',
    'output': 'bg-primary',
    'analog': 'bg-warning',
    'digital': 'bg-info'
  };
  return badges[tipo] || 'bg-secondary';
}

function getTipoModuloBadge(tipo) {
  const badges = {
    'cpu': 'bg-primary',
    'io': 'bg-success',
    'communication': 'bg-info',
    'power': 'bg-warning'
  };
  return badges[tipo] || 'bg-secondary';
}

// Initialize data on component mount
onMounted(() => {
  caricaIO();
  caricaNodi();
});
</script>

<style scoped>
.assegna-io {
  padding: 1rem;
  max-width: 1400px;
  margin: 0 auto;
}

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

.form-check-input {
  margin-top: 0.3rem;
}

.btn-group .btn {
  padding: 0.25rem 0.75rem;
}

.badge {
  padding: 0.35em 0.65em;
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
