import axios from 'axios';
import { useRouter } from 'vue-router';

// Create an axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Access-Control-Allow-Credentials': 'true'
  },
  withCredentials: true, // This is required for cookies to be sent with requests
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  crossDomain: true
});

// Add response interceptor to handle CORS headers
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      if (error.response.status === 401) {
        // Handle unauthorized
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/login')) {
          window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`;
        }
      }
      return Promise.reject(error);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error', error.message);
    }
    return Promise.reject(error);
  }
);

// Request interceptor to add CSRF token if it exists
api.interceptors.request.use(
  (config) => {
    // Get CSRF token from cookies if it exists
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific status codes
      if (error.response.status === 401) {
        // Redirect to login with the current URL as the redirect parameter
        const currentPath = window.location.pathname + window.location.search;
        // Only redirect to login if we're not already on the login page
        if (!currentPath.includes('/login')) {
          window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`;
        }
      } else if (error.response.status === 403) {
        // Handle forbidden (permission denied)
        console.error('Access denied: You do not have permission to perform this action');
      } else if (error.response.status === 404) {
        // Handle not found
        console.error('The requested resource was not found');
      } else if (error.response.status >= 500) {
        // Handle server errors
        console.error('A server error occurred. Please try again later.');
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response from server. Please check your connection.');
    } else {
      // Something happened in setting up the request
      console.error('Request error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API methods
export default {
  // Auth
  login(credentials, redirectUrl = null) {
    // Build URL with redirect_url as query parameter if provided
    let url = '/login';
    if (redirectUrl) {
      const params = new URLSearchParams();
      params.append('redirect_url', redirectUrl);
      url += `?${params.toString()}`;
    }
    
    // Send as JSON body
    return api.post(url, {
      username: credentials.username,
      password: credentials.password
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
  },
  
  logout() {
    return api.post('/logout');
  },
  
  // Get current user
  getCurrentUser() {
    return api.get('/users/me');
  },
  
  // Projects
  getProjects() {
    return api.get('/progetti');
  },
  getProject(id) {
    return api.get(`/progetti/${id}`);
  },
  createProject(projectData) {
    return api.post('/progetti', projectData);
  },
  updateProject(id, projectData) {
    return api.put(`/progetti/${id}`, projectData);
  },
  deleteProject(id) {
    return api.delete(`/progetti/${id}`);
  },
  
  // Utilities
  uploadUtilities(projectId, file) {
    const formData = new FormData();
    formData.append('file_utenze', file);
    return api.post(`/progetto/${projectId}/carica_file_utenze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  // Nodes
  getNodes(projectId) {
    return api.get('/lista_nodi', { params: { id_prg: projectId } });
  },
  createNode(nodeData) {
    return api.post('/crea_nodo', nodeData);
  },
  
  // Hardware
  getHardwareCatalog() {
    return api.get('/catalogo_hw');
  },
  
  // I/O Management
  getUnassignedIO(projectId) {
    return api.get('/io_unassigned', { params: { id_prg: projectId } });
  },
  getAssignedIO(moduleId) {
    return api.get('/io_assigned', { params: { id_modulo: moduleId } });
  },
  assignIO(ioData) {
    return api.post('/io_assign', ioData);
  },
  removeIOAssignment(ioId) {
    return api.delete(`/io_assign/${ioId}`);
  },
  
  // Export
  exportIO(projectId) {
    return api.get('/export_io', { params: { id_prg: projectId } });
  },
  generateSchema(projectId) {
    return api.get('/genera_schema', { params: { id_prg: projectId } });
  },

  // Utility Management
  getAvailableUtilities(projectId) {
    return api.get('/utenze', { params: { id_prg: projectId } });
  },
  getAvailableModules() {
    return api.get('/catalogo_hw');
  },
  assignUtility(assignmentData) {
    return api.post('/assegna_utenza', assignmentData);
  },
  saveAssignments(assignments) {
    return api.post('/salva_assegnazioni', { assignments });
  }
};
