<template>
  <div class="login-container">
    <div class="login-box">
      <h1>Accesso</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Nome utente</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            class="form-control"
            :disabled="loading"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            class="form-control"
            :disabled="loading"
          >
        </div>
        
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <div class="form-footer">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ loading ? 'Accesso in corso...' : 'Accedi' }}
          </button>
          
          <div v-if="loading" class="mt-3">
            <div class="progress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const route = useRoute();

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = 'Inserisci nome utente e password';
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  // Store the redirect URL if present
  const redirectUrl = route.query.redirect || null;
  if (redirectUrl) {
    authStore.setReturnUrl(redirectUrl);
  }
  
  try {
    await authStore.login({
      username: username.value,
      password: password.value
    });
    
    // The auth store will handle the redirect after successful login
  } catch (err) {
    error.value = err.response?.data?.detail || 'Si è verificato un errore durante il login';
    console.error('Login error:', err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.form-footer {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-box {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.alert {
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.alert-danger {
  background-color: #fde8e8;
  color: #c53030;
  border: 1px solid #feb2b2;
}

.spinner-border {
  margin-right: 0.5rem;
  vertical-align: middle;
}
</style>
