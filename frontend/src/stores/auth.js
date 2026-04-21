import { defineStore } from 'pinia';
import apiFetch from '../api'; // Import the wrapper

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    authError: null,
  }),
  actions: {
    async login(email, password) {
      try {
        // fastapi-users' login endpoint is special, it wants form data
        await apiFetch('/auth/cookie/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({ username: email, password: password }).toString(),
        });
        await this.fetchUser();
        return true;
      } catch (error) {
        this.authError = error.message;
        this.isAuthenticated = false;
        this.user = null;
        return false;
      }
    },

    async register(email, password, nickname) {
      try {
        await apiFetch('/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, password, nickname }),
        });
        // After successful registration, log the user in
        await this.login(email, password);
        return true;
      } catch (error) {
        this.authError = error.message;
        this.isAuthenticated = false;
        this.user = null;
        return false;
      }
    },

    async logout() {
      try {
        await apiFetch('/auth/cookie/logout', { method: 'POST' });
        this.user = null;
        this.isAuthenticated = false;
        this.authError = null;
        return true;
      } catch (error) {
        this.authError = error.message;
        return false;
      }
    },

    async fetchUser() {
      try {
        const userData = await apiFetch('/users/me');
        if (userData) {
          this.user = userData;
          this.isAuthenticated = true;
          this.authError = null;
        } else {
          this.user = null;
          this.isAuthenticated = false;
        }
      } catch (error) {
        this.user = null;
        this.isAuthenticated = false;
      }
    },
    
    async markTaskAsDone(taskId) {
        if (!this.isAuthenticated) return;
        try {
            await apiFetch(`/api/v1/tasks/${taskId}/mark_done`, {
                method: 'POST',
            });
            // Add task to local state to update UI immediately
            if (this.user && !this.user.solved_tasks.includes(taskId)) {
                this.user.solved_tasks.push(taskId);
            }
        } catch (error) {
            console.error(`Failed to mark task ${taskId} as done:`, error);
        }
    },
  },
});
