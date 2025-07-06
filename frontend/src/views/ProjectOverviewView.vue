<template>
  <div class="project-overview">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h2 class="h4 mb-0">{{ project.name }}</h2>
      </div>
      <div class="card-body">
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-2">Loading project details...</p>
        </div>

        <div v-else>
          <div class="row mb-4">
            <div class="col-md-8">
              <h3 class="h5">Project Information</h3>
              <p v-if="project.description" class="text-muted">
                {{ project.description }}
              </p>
              <p v-else class="text-muted fst-italic">
                No description available
              </p>
              
              <div class="project-meta">
                <div class="d-flex align-items-center mb-2">
                  <i class="fas fa-calendar-alt me-2"></i>
                  <span>Created on: {{ formatDate(project.createdAt) }}</span>
                </div>
                <div class="d-flex align-items-center">
                  <i class="fas fa-user me-2"></i>
                  <span>Project ID: {{ project.id_prg }}</span>
                </div>
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="card">
                <div class="card-header bg-light">
                  <h4 class="h6 mb-0">Quick Actions</h4>
                </div>
                <div class="card-body p-0">
                  <div class="list-group list-group-flush">
                    <router-link 
                      :to="`/projects/${project.id_prg}/upload-utilities`"
                      class="list-group-item list-group-item-action"
                    >
                      <i class="fas fa-upload me-2"></i>Upload Utilities
                    </router-link>
                    <router-link 
                      :to="`/projects/${project.id_prg}/create-node`"
                      class="list-group-item list-group-item-action"
                    >
                      <i class="fas fa-plus-circle me-2"></i>Create Node
                    </router-link>
                    <router-link 
                      :to="`/projects/${project.id_prg}/assign-io`"
                      class="list-group-item list-group-item-action"
                    >
                      <i class="fas fa-exchange-alt me-2"></i>Assign I/O
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="project-stats">
            <h3 class="h5 mb-3">Project Statistics</h3>
            <div class="row">
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <div class="text-primary mb-2">
                      <i class="fas fa-server fa-2x"></i>
                    </div>
                    <h5 class="card-title mb-1">Nodes</h5>
                    <p class="h3 mb-0">{{ stats.nodes || 0 }}</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <div class="text-success mb-2">
                      <i class="fas fa-plug fa-2x"></i>
                    </div>
                    <h5 class="card-title mb-1">I/O Points</h5>
                    <p class="h3 mb-0">{{ stats.ioPoints || 0 }}</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <div class="text-warning mb-2">
                      <i class="fas fa-bolt fa-2x"></i>
                    </div>
                    <h5 class="card-title mb-1">Utilities</h5>
                    <p class="h3 mb-0">{{ stats.utilities || 0 }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="recent-activity mt-4">
            <h3 class="h5 mb-3">Recent Activity</h3>
            <div class="card">
              <div class="card-body">
                <div v-if="recentActivity.length > 0" class="list-group list-group-flush">
                  <div v-for="(activity, index) in recentActivity" :key="index" class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">{{ activity.title }}</h6>
                      <small class="text-muted">{{ formatTimeAgo(activity.timestamp) }}</small>
                    </div>
                    <p class="mb-1">{{ activity.description }}</p>
                  </div>
                </div>
                <div v-else class="text-center py-4 text-muted">
                  <i class="fas fa-inbox fa-3x mb-3"></i>
                  <p>No recent activity</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';

const route = useRoute();
const projectStore = useProjectStore();

const project = ref({});
const loading = ref(true);
const stats = ref({
  nodes: 0,
  ioPoints: 0,
  utilities: 0
});

const recentActivity = ref([
  // This would be populated from an API in a real app
  // {
  //   title: 'Project created',
  //   description: 'Project was created',
  //   timestamp: new Date()
  // }
]);

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Format time ago for activity feed
const formatTimeAgo = (date) => {
  if (!date) return '';
  
  const now = new Date();
  const diffInSeconds = Math.floor((now - new Date(date)) / 1000);
  
  if (diffInSeconds < 60) return 'Just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
  return formatDate(date);
};

// Fetch project data
const fetchProjectData = async () => {
  try {
    loading.value = true;
    const projectId = route.params.id;
    
    if (!projectId) {
      console.error('No project ID provided');
      return;
    }
    
    // Fetch project details
    await projectStore.fetchProject(projectId);
    project.value = { ...projectStore.currentProject };
    
    // In a real app, you would fetch statistics and activity here
    // stats.value = await fetchProjectStats(projectId);
    // recentActivity.value = await fetchRecentActivity(projectId);
    
  } catch (error) {
    console.error('Error loading project data:', error);
  } finally {
    loading.value = false;
  }
};

// Watch for route changes to update project data
onMounted(() => {
  fetchProjectData();
});
</script>

<style scoped>
.project-overview {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  font-weight: 600;
}

.list-group-item {
  border-left: none;
  border-right: none;
  padding: 0.75rem 1.25rem;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}

.project-meta {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.25rem;
  margin-top: 1.5rem;
}

.text-primary {
  color: #0d6efd !important;
}

.text-success {
  color: #198754 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.fa-2x {
  font-size: 1.75em;
}

.h-100 {
  min-height: 100%;
}
</style>
