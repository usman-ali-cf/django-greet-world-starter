<template>
  <div class="main-layout">
    <!-- Header Component -->
    <header class="header">
      <button id="sidebar-toggle" class="sidebar-toggle" @click="toggleSidebar">
        ☰
      </button>
      <div class="header-left">
        <h1>{{ pageTitle }}</h1>
      </div>
      <nav class="header-nav">
        <router-link to="/">🏠 Home</router-link>
        <router-link v-if="projectId" :to="'/projects/' + projectId" class="ml-3">
          🔙 Torna al Progetto
        </router-link>
      </nav>
      <img class="logo-app" src="@/assets/Logo.png" alt="Logo">
    </header>

    <!-- Sidebar Component -->
    <div id="sidebar" class="sidebar" :class="{ 'hidden': !sidebarVisible }">
      <nav class="sidebar-nav">
        <router-link to="/">🏠 Home</router-link>
        <router-link v-if="projectId" :to="'/projects/' + projectId">
          🔙 Torna al Progetto
        </router-link>
        
        <template v-if="projectId">
          <router-link :to="'/projects/' + projectId + '/upload-utilities'">
            📁 Carica File Utenze
          </router-link>
          <router-link :to="'/projects/' + projectId + '/configure-utilities'">
            🛠️ Configura Utenze
          </router-link>
          <router-link :to="'/projects/' + projectId + '/configure-power'">
            ⚡ Configura Utenze di Potenza
          </router-link>
          <router-link :to="'/projects/' + projectId + '/create-node'">
            🖧 Crea Nodi e PLC
          </router-link>
          <router-link :to="'/projects/' + projectId + '/assign-io'">
            🔗 Assegna I/O ai Nodi
          </router-link>
          <router-link :to="'/projects/' + projectId + '/configure-panel'">
            🗄️ Configura Quadro Elettrico
          </router-link>
        </template>
      </nav>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const sidebarVisible = ref(true);

// Get project ID from route params
const projectId = computed(() => {
  return route.params.id;
});

// Set page title based on current route
const pageTitle = computed(() => {
  const routeName = route.name;
  const titles = {
    'home': 'Home',
    'projects': 'Progetti',
    'project-detail': 'Dettaglio Progetto',
    'upload-utilities': 'Carica File Utenze',
    'configure-utilities': 'Configura Utenze',
    'configure-power': 'Configura Potenza',
    'configure-io': 'Configura I/O',
    'configure-panel': 'Configura Quadro',
    'create-node': 'Crea Nodo',
    'assign-io': 'Assegna I/O',
    'create-project': 'Nuovo Progetto'
  };
  return titles[routeName] || 'Electrical Project Manager';
});

// Toggle sidebar visibility
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
};

// Close sidebar on mobile when clicking outside
const handleClickOutside = (event) => {
  const sidebar = document.getElementById('sidebar');
  const toggleButton = document.getElementById('sidebar-toggle');
  
  if (sidebar && !sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
    sidebarVisible.value = false;
  }
};

// Add event listeners for mobile responsiveness
onMounted(() => {
  // Check screen size on mount
  const handleResize = () => {
    if (window.innerWidth < 992) {
      sidebarVisible.value = false;
      document.addEventListener('click', handleClickOutside);
    } else {
      sidebarVisible.value = true;
      document.removeEventListener('click', handleClickOutside);
    }
  };
  
  // Initial check
  handleResize();
  
  // Add resize listener
  window.addEventListener('resize', handleResize);
  
  // Cleanup
  return () => {
    window.removeEventListener('resize', handleResize);
    document.removeEventListener('click', handleClickOutside);
  };
});
</script>

<style scoped>
/* Main Layout */
.main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #032952;
  color: white;
  padding: 0.75rem 1.5rem;
  position: relative;
  z-index: 1001;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-nav a {
  color: white;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.header-nav a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.header-nav a.router-link-active {
  font-weight: 600;
  background-color: rgba(255, 255, 255, 0.15);
}

.logo-app {
  height: 40px;
  margin-left: 1rem;
}

/* Sidebar Toggle Button */
.sidebar-toggle {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  margin-right: 0.5rem;
  display: none;
}

/* Sidebar Styles */
.sidebar {
  width: 250px;
  background-color: #032952;
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  padding-top: 70px;
  transition: transform 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
}

.sidebar.hidden {
  transform: translateX(-100%);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}

.sidebar-nav a {
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-nav a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  font-weight: 500;
  border-left: 4px solid #4a9fe0;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 250px;
  margin-top: 60px;
  padding: 1.5rem;
  overflow-y: auto;
  height: calc(100vh - 60px);
  background-color: #f4f4f4;
  transition: margin-left 0.3s ease;
}

/* Responsive Styles */
@media (max-width: 991.98px) {
  .sidebar-toggle {
    display: block;
  }
  
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar:not(.hidden) {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .logo-app {
    height: 35px;
  }
}

/* Utility Classes */
.ml-3 {
  margin-left: 0.75rem;
}
</style>
