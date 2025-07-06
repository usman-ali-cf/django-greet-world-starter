import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from './auth';

export const useProjectStore = defineStore('project', () => {
  const router = useRouter();
  const authStore = useAuthStore();
  
  const projects = ref([]);
  const currentProject = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const lastFetchTime = ref(0);
  const FETCH_CACHE_TIME = 5 * 60 * 1000; // 5 minutes cache

  // Get all projects
  async function fetchProjects(force = false) {
    // Return cached results if they're still fresh
    const now = Date.now();
    if (!force && projects.value.length > 0 && (now - lastFetchTime.value) < FETCH_CACHE_TIME) {
      return projects.value;
    }

    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.getProjects();
      // Map the response data to match frontend expectations
      projects.value = response.data.data.map(project => ({
        id: project.id_prg, // Ensure we're using 'id' consistently
        id_prg: project.id_prg,
        nome_prg: project.name, // Match the template expectation
        nome_progetto: project.name,
        descrizione: project.description,
        data_creazione: project.createdAt || new Date().toISOString()
      }));
      
      lastFetchTime.value = now;
      return projects.value;
    } catch (err) {
      console.error('Error fetching projects:', err);
      error.value = err.response?.data?.message || 'Errore nel caricamento dei progetti';
      
      // Handle unauthorized errors
      if (err.response?.status === 401) {
        authStore.logout();
        router.push({ name: 'login' });
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Get single project
  async function fetchProject(id) {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getProject(id);
      currentProject.value = response.data;
      return currentProject.value;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore nel caricamento del progetto';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Create new project
  async function createProject(projectData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.createProject(projectData);
      projects.value.unshift(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore nella creazione del progetto';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Update project
  async function updateProject(id, projectData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.updateProject(id, projectData);
      const index = projects.value.findIndex(p => p.id_prg === id);
      if (index !== -1) {
        projects.value[index] = response.data;
      }
      if (currentProject.value && currentProject.value.id_prg === id) {
        currentProject.value = response.data;
      }
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore nell\'aggiornamento del progetto';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Delete project
  async function deleteProject(id) {
    loading.value = true;
    error.value = null;
    try {
      await api.deleteProject(id);
      projects.value = projects.value.filter(p => p.id_prg !== id);
      if (currentProject.value && currentProject.value.id_prg === id) {
        currentProject.value = null;
      }
      return true;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore nell\'eliminazione del progetto';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Upload utilities file
  async function uploadUtilities(projectId, file) {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.uploadUtilities(projectId, file);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore nel caricamento del file delle utenze';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  // Clear current project
  function clearCurrentProject() {
    currentProject.value = null;
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    uploadUtilities,
    clearCurrentProject
  };
});
