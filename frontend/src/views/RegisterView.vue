<template>
  <div class="max-w-md mx-auto mt-10">
    <div class="stats-card">
      <h2 class="text-2xl font-bold text-center mb-6 press-start-font">Регистрация</h2>
      <form @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="nickname" class="block text-sm font-medium text-[color:var(--color-muted-foreground)] mb-1">Никнейм</label>
            <input type="text" id="nickname" v-model="nickname" class="input-field" required>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-[color:var(--color-muted-foreground)] mb-1">Email</label>
            <input type="email" id="email" v-model="email" class="input-field" required>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-[color:var(--color-muted-foreground)] mb-1">Пароль</label>
            <input type="password" id="password" v-model="password" class="input-field" required>
          </div>
        </div>
        <div v-if="authStore.authError" class="mt-4 text-center text-[color:var(--color-destructive)]">
          {{ authStore.authError }}
        </div>
        <div class="mt-6">
          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
        </div>
        <div class="mt-4 text-center text-sm">
          <router-link to="/login" class="text-[color:var(--color-primary)] hover:text-[color:var(--color-primary)]/90">
            Уже есть аккаунт? Войти
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

const nickname = ref('');
const email = ref('');
const password = ref('');
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  loading.value = true;
  authStore.authError = null;
  const success = await authStore.register(email.value, password.value, nickname.value);
  loading.value = false;
  if (success) {
    router.push('/dashboard');
  }
};
</script>
