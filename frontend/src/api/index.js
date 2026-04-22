// src/api/index.js
import { useAuthStore } from '@/stores/auth.js';

const BASE_URL = 'http://localhost:8000';

async function apiFetch(url, options = {}) {
  const defaultOptions = {
    credentials: 'include', // Send cookies with all requests
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  const response = await fetch(`${BASE_URL}${url}`, { ...options, ...defaultOptions });

  if (response.status === 401) {
    // Unauthorized, maybe the cookie expired.
    const authStore = useAuthStore();
    authStore.user = null;
    authStore.isAuthenticated = false;
    // Optionally redirect to login
    // window.location.href = '/login';
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'An unknown error occurred' }));
    throw new Error(errorData.detail);
  }

  if (response.status === 204) { // No Content
    return null;
  }

  return response.json();
}

export default apiFetch;
