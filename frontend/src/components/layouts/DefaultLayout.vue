<template>
  <div class="min-h-screen flex flex-col bg-background text-foreground">
    <!-- Header -->
    <header class="bg-[#0a0a0a] border-b border-[#222] backdrop-blur-sm z-10">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="flex items-center space-x-2">
          <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent press-start-font">Открытый банк ФИПИ</h1>
        </router-link>
        <nav>
          <ul class="flex items-center space-x-2">
            <li>
              <router-link to="/" class="nav-link px-4 py-2" active-class="active-nav-link">
                Главная
              </router-link>
            </li>
            <template v-if="authStore.isAuthenticated">
              <li>
                <router-link to="/dashboard" class="nav-link px-4 py-2" active-class="active-nav-link">
                  Статистика
                </router-link>
              </li>
              <li>
                <button @click="handleLogout" class="nav-link px-4 py-2">
                  Выйти
                </button>
              </li>
              <li v-if="authStore.user" class="pl-2 text-indigo-400">
                Hi, {{ authStore.user.nickname }}
              </li>
            </template>
            <template v-else>
              <li>
                <router-link to="/login" class="nav-link px-4 py-2" active-class="active-nav-link">
                  Войти
                </router-link>
              </li>
              <li>
                <router-link to="/register" class="btn-primary px-4 py-2 text-sm">
                  Регистрация
                </router-link>
              </li>
            </template>
          </ul>
        </nav>
      </div>
    </header>

    <!-- Main Content Slot -->
    <main class="flex-grow container mx-auto px-4 py-8 max-w-6xl">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-border bg-card py-6">
      <div class="container mx-auto px-4 text-center text-sm text-muted-foreground">
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
/* You can add component-specific styles here if needed */
</style>
