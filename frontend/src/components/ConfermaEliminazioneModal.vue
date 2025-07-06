<template>
  <div class="modal fade" :class="{ 'show d-block': show }" tabindex="-1" v-if="show">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">
            <i class="fas fa-exclamation-triangle me-2"></i>Conferma Eliminazione
          </h5>
          <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <p v-if="!itemName">Sei sicuro di voler eliminare questo elemento?</p>
          <p v-else>Sei sicuro di voler eliminare <strong>{{ itemName }}</strong>?</p>
          <p class="text-muted small mb-0">Questa azione non può essere annullata.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" @click="closeModal" :disabled="deleting">
            Annulla
          </button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="confirmDelete"
            :disabled="deleting"
          >
            <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
            {{ deleting ? 'Eliminazione in corso...' : 'Elimina' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  itemName: {
    type: String,
    default: ''
  },
  deleting: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['confirm', 'close']);

function confirmDelete() {
  emit('confirm');
}

function closeModal() {
  emit('close');
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
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

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #bb2d3b;
  border-color: #b02a37;
}

.btn-danger:disabled {
  background-color: #dc3545;
  border-color: #dc3545;
  opacity: 0.65;
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

.spinner-border {
  width: 1.25rem;
  height: 1.25rem;
  border-width: 0.15em;
}
</style>
