<template>
  <div class="upload-utilities">
    <div class="card">
      <div class="card-body">
        <h2 class="mb-4">Carica File Utenze</h2>
        <div v-if="!fileUploaded" class="upload-area" @dragover.prevent="onDragOver" @drop.prevent="onDrop">
          <div class="text-center p-5">
            <i class="fas fa-cloud-upload-alt fa-3x mb-3 text-primary"></i>
            <h4>Trascina il file qui o clicca per selezionare</h4>
            <p class="text-muted mb-3">Formati supportati: .xlsx, .xls</p>
            <input 
              type="file" 
              ref="fileInput" 
              class="d-none" 
              accept=".xlsx, .xls"
              @change="onFileSelected"
            >
            <button class="btn btn-primary" @click="triggerFileInput">
              <i class="fas fa-folder-open me-2"></i>Seleziona File
            </button>
          </div>
        </div>
        
        <div v-else class="upload-success">
          <div class="alert alert-success">
            <i class="fas fa-check-circle me-2"></i>
            File caricato con successo!
          </div>
          
          <div class="file-info mb-4">
            <h5>Dettagli File:</h5>
            <ul class="list-unstyled">
              <li><strong>Nome:</strong> {{ uploadedFile.name }}</li>
              <li><strong>Dimensione:</strong> {{ formatFileSize(uploadedFile.size) }}</li>
              <li><strong>Tipo:</strong> {{ uploadedFile.type || 'application/vnd.ms-excel' }}</li>
              <li><strong>Ultima modifica:</strong> {{ formatDate(uploadedFile.lastModified) }}</li>
            </ul>
          </div>
          
          <div class="d-flex justify-content-between">
            <button class="btn btn-outline-secondary" @click="resetForm">
              <i class="fas fa-arrow-left me-2"></i>Torna indietro
            </button>
            <div>
              <a :href="downloadTemplateUrl" class="btn btn-outline-primary me-2">
                <i class="fas fa-download me-2"></i>Scarica Template
              </a>
              <button class="btn btn-primary" @click="uploadFile" :disabled="uploading">
                <span v-if="uploading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                <i v-else class="fas fa-upload me-2"></i>
                {{ uploading ? 'Caricamento in corso...' : 'Carica File' }}
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="error" class="alert alert-danger mt-3">
          <i class="fas fa-exclamation-circle me-2"></i>
          {{ error }}
        </div>
      </div>
    </div>
    
    <!-- Processing Modal -->
    <div v-if="processing" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body text-center p-4">
            <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
              <span class="visually-hidden">Caricamento...</span>
            </div>
            <h5>Elaborazione in corso</h5>
            <p class="mb-0">Attendi mentre il file viene elaborato...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
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

const fileInput = ref(null);
const uploadedFile = ref(null);
const fileUploaded = ref(false);
const uploading = ref(false);
const processing = ref(false);
const error = ref('');

const downloadTemplateUrl = computed(() => {
  return `/download_template`;
});

function triggerFileInput() {
  fileInput.value.click();
}

function onDragOver(event) {
  event.currentTarget.classList.add('drag-over');
}

function onDrop(event) {
  event.currentTarget.classList.remove('drag-over');
  const files = event.dataTransfer.files;
  if (files.length) {
    handleFile(files[0]);
  }
}

function onFileSelected(event) {
  const files = event.target.files;
  if (files.length) {
    handleFile(files[0]);
  }
}

function handleFile(file) {
  const validTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (!validTypes.includes(file.type) && !file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    error.value = 'Formato file non valido. Si prega di caricare un file Excel (.xlsx o .xls)';
    return;
  }
  
  if (file.size > maxSize) {
    error.value = 'Il file è troppo grande. Dimensione massima consentita: 10MB';
    return;
  }
  
  error.value = '';
  uploadedFile.value = file;
  fileUploaded.value = true;
}

function resetForm() {
  fileUploaded.value = false;
  uploadedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

async function uploadFile() {
  if (!uploadedFile.value) return;
  
  try {
    uploading.value = true;
    processing.value = true;
    error.value = '';
    
    await projectStore.uploadUtilities(props.project.id_prg, uploadedFile.value);
    
    // Reset form after successful upload
    resetForm();
    
    // Show success message
    setTimeout(() => {
      processing.value = false;
    }, 1000);
    
  } catch (err) {
    console.error('Error uploading file:', err);
    error.value = err.response?.data?.message || 'Si è verificato un errore durante il caricamento del file';
  } finally {
    uploading.value = false;
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(timestamp) {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return date.toLocaleDateString('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
</script>

<style scoped>
.upload-utilities {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
  border-radius: 0.5rem;
  overflow: hidden;
}

.card-header {
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-body {
  padding: 2rem;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover, .upload-area.drag-over {
  border-color: #3498db;
  background-color: #f0f7ff;
}

.upload-success {
  animation: fadeIn 0.3s ease;
}

.file-info {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.file-info h5 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.file-info li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.file-info li:last-child {
  border-bottom: none;
}

.file-info strong {
  color: #495057;
  margin-right: 0.5rem;
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

.btn-outline-primary {
  color: #3498db;
  border-color: #3498db;
  background-color: transparent;
}

.btn-outline-primary:hover {
  background-color: #3498db;
  color: white;
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
  border-radius: 0.375rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.alert-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.alert-danger {
  background-color: #ffebee;
  color: #c62828;
}

.alert i {
  font-size: 1.25rem;
  margin-right: 0.5rem;
}

.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.15);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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
