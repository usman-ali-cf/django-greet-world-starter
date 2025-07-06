import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/services/api';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const user = ref(null);
  const isAuthenticated = ref(false);
  const loading = ref(false);
  const error = ref(null);
  const returnUrl = ref(null);
  const lastAuthCheck = ref(0);
  const AUTH_CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes

  async function login(credentials) {
    loading.value = true;
    error.value = null;
    try {
      // Get the current path for redirect after login
      const currentPath = window.location.pathname + window.location.search + window.location.hash;
      const isLoginPage = currentPath.includes('/login');
      
      // The session cookie will be set by the server in the response
      const response = await api.login(
        credentials,
        // Only pass redirect URL if we're not on the login page
        isLoginPage ? returnUrl.value : currentPath
      );
      
      // Set user data from the login response
      if (response.data && response.data.user) {
        user.value = response.data.user;
        isAuthenticated.value = true;
        lastAuthCheck.value = Date.now();
      }
      
      // Determine where to redirect after login
      let redirectPath = '/';
      if (response.data.redirect_url) {
        redirectPath = response.data.redirect_url;
      } else if (returnUrl.value) {
        redirectPath = returnUrl.value;
      } else if (!isLoginPage) {
        redirectPath = currentPath;
      }
      
      // Clean up and redirect
      returnUrl.value = null;
      await router.push(redirectPath);
      return true;
    } catch (err) {
      error.value = err.response?.data?.message || 'Errore durante il login';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    try {
      await api.logout();
    } finally {
      user.value = null;
      isAuthenticated.value = false;
      lastAuthCheck.value = 0;
      // The cookie will be cleared by the server response
      router.push('/login');
    }
  }

  async function checkAuth(force = false) {
    // If we've checked recently and we're not forcing a check, return cached state
    const now = Date.now();
    if (!force && now - lastAuthCheck.value < AUTH_CHECK_INTERVAL && isAuthenticated.value) {
      return true;
    }

    try {
      const response = await api.getCurrentUser();
      user.value = response.data;
      isAuthenticated.value = true;
      lastAuthCheck.value = now;
      return true;
    } catch (error) {
      // If the request fails with 401, the session is invalid/expired
      if (error.response && error.response.status === 401) {
        console.log('Session expired or invalid');
        user.value = null;
        isAuthenticated.value = false;
      } else {
        console.error('Error checking authentication status:', error);
      }
      return false;
    }
  }
    function setReturnUrl(url) {
    returnUrl.value = url;
  }

  // Initialize auth state on store creation
  (async () => {
    await checkAuth();
  })();

  return {
    user,
    isAuthenticated: computed(() => isAuthenticated.value && !!user.value),
    loading,
    error,
    login,
    logout,
    checkAuth,
    setReturnUrl
  };
});
