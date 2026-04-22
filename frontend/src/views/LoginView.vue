<template>
  <div class="max-w-md mx-auto mt-10">
    <div class="stats-card">
      <h2 class="text-2xl font-bold text-center mb-6 press-start-font">Вход</h2>
      <form @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-muted-foreground mb-1">Email</label>
            <input type="email" id="email" v-model="email" class="input-field" required>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-muted-foreground mb-1">Пароль</label>
            <input type="password" id="password" v-model="password" class="input-field" required>
          </div>
        </div>
        <div v-if="authStore.authError" class="mt-4 text-center text-destructive">
          {{ authStore.authError }}
        </div>
        <div class="mt-6">
          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>
        </div>
        <div class="mt-4 text-center text-sm">
          <router-link to="/register" class="text-indigo-400 hover:text-indigo-300">
            Нет аккаунта? Зарегистрироваться
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';

const email = ref('');
const password = ref('');
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  authStore.authError = null;
  const success = await authStore.login(email.value, password.value);
  loading.value = false;
  if (success) {
    router.push('/dashboard');
  }
};
</script>
