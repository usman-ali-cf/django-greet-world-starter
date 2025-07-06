import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useProjectStore } from '@/stores/project';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import ProjectDetailView from '@/views/ProjectDetailView.vue';
import ProjectOverviewView from '@/views/ProjectOverviewView.vue';
import CreateProjectView from '@/views/CreateProjectView.vue';
import UploadUtilitiesView from '@/views/UploadUtilitiesView.vue';
import ConfigureUtilitiesView from '@/views/ConfigureUtilitiesView.vue';
import ConfigurePowerView from '@/views/ConfigurePowerView.vue';
import ConfigureIOView from '@/views/ConfigureIOView.vue';
import ConfigurePanelView from '@/views/ConfigurePanelView.vue';
import CreaNodoView from '@/views/CreaNodoView.vue';
import AssignIOView from '@/views/AssegnaIOView.vue';
import api from '@/services/api';

// Public routes that don't require authentication
const publicRoutes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { public: true }
  }
];

// Routes that require authentication
const protectedRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/ProjectsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/new',
    name: 'create-project',
    component: CreateProjectView,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/:id',
    component: ProjectDetailView,
    props: true,
    meta: { requiresAuth: true, requiresProject: true },
    children: [
      {
        path: '',
        name: 'project-overview',
        component: ProjectOverviewView
      },
      {
        path: 'upload-utilities',
        name: 'upload-utilities',
        component: UploadUtilitiesView
      },
      {
        path: 'configure-utilities',
        name: 'configure-utilities',
        component: ConfigureUtilitiesView
      },
      {
        path: 'configure-power',
        name: 'configure-power',
        component: ConfigurePowerView
      },
      {
        path: 'configure-io',
        name: 'configure-io',
        component: ConfigureIOView
      },
      {
        path: 'configure-panel',
        name: 'configure-panel',
        component: ConfigurePanelView
      },
      {
        path: 'create-node',
        name: 'create-node',
        component: CreaNodoView
      },
      {
        path: 'assign-io',
        name: 'assign-io',
        component: AssignIOView
      }
    ]
  },
  // 404 catch-all
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue')
  }
];

const routes = [...publicRoutes, ...protectedRoutes];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Return desired position
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    } else {
      return { top: 0 };
    }
  }
});

/**
 * Check if a route requires authentication
 */
function requiresAuth(to) {
  return to.matched.some(record => record.meta.requiresAuth);
}

/**
 * Check if a route is public
 */
function isPublicRoute(to) {
  return to.matched.some(record => record.meta.public);
}

/**
 * Check if a route requires a valid project
 */
function requiresProject(to) {
  return to.matched.some(record => record.meta.requiresProject);
}

/**
 * Check if a project ID is valid
 */
function isValidProjectId(projectId) {
  return projectId && !isNaN(parseInt(projectId));
}

// Navigation guard to check auth status
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // Skip auth check for public routes
  if (isPublicRoute(to)) {
    next();
    return;
  }
  
  // Check if the route requires authentication
  if (requiresAuth(to)) {
    try {
      // Only force auth check if we're not already authenticated
      const forceCheck = !authStore.isAuthenticated;
      const isAuthenticated = await authStore.checkAuth(forceCheck);
      
      if (!isAuthenticated) {
        // Store the attempted URL for redirecting after login
        if (to.path !== '/login') {
          authStore.setReturnUrl(to.fullPath);
        }
        
        // Redirect to login page if not already there
        if (to.name !== 'login') {
          next({
            name: 'login',
            query: { redirect: to.fullPath }
          });
          return;
        }
      }
      
      // If we're on the login page but already authenticated, redirect to home
      if (to.name === 'login' && isAuthenticated) {
        next({ name: 'home' });
        return;
      }
      
      // Check if the route requires a valid project
      if (requiresProject(to)) {
        const projectId = to.params.id;
        
        // Validate project ID format
        if (!isValidProjectId(projectId)) {
          // Invalid project ID format, redirect to projects list with error
          next({
            name: 'projects',
            query: { error: 'invalid_project' }
          });
          return;
        }
        
        // At this point, we know the ID is a valid number
        // We'll let the component handle the actual project existence check
        // to avoid duplicate API calls
      }
    } catch (error) {
      console.error('Error during navigation guard:', error);
      // On error, clear auth state and redirect to login
      authStore.logout();
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      });
      return;
    }
  }
  
  // Continue with the navigation
  next();
});

// Global error handler for navigation
router.onError((error) => {
  console.error('Navigation error:', error);
  // You can implement custom error handling here, e.g., show a notification
});

export default router;
