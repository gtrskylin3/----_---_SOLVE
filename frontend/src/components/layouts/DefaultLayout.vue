<template>
  <div class="min-h-screen flex flex-col bg-[color:var(--color-background)] text-[color:var(--color-foreground)]">
    <!-- Header -->
    <header class="bg-[color:var(--color-card)]/80 border-b border-[color:var(--color-border)] backdrop-blur-sm z-10">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="flex items-center space-x-2">
          <h1 class="text-xl md:text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent press-start-font">Открытый банк ФИПИ</h1>
        </router-link>
        
        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center space-x-2">
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
              <li v-if="authStore.user" class="pl-2 text-[color:var(--color-primary)]">
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
            <li>
              <button @click="toggleTheme" class="nav-link px-4 py-2">
                {{ theme === 'light' ? '🌙' : '☀️' }}
              </button>
            </li>
          </ul>
        </nav>

        <!-- Mobile Burger Button -->
        <div class="md:hidden flex items-center">
          <button @click="toggleTheme" class="nav-link px-3 py-2 mr-2">
            {{ theme === 'light' ? '🌙' : '☀️' }}
          </button>
          <button @click="toggleMobileMenu" class="p-2 rounded-md hover:bg-[color:var(--color-muted)] focus:outline-none focus:ring-2 focus:ring-[color:var(--color-ring)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Nav -->
      <div v-if="isMobileMenuOpen" class="md:hidden bg-[color:var(--color-card)]/95 backdrop-blur-sm">
        <nav class="flex flex-col items-center space-y-2 py-4">
          <router-link to="/" class="nav-link px-4 py-2" active-class="active-nav-link" @click="isMobileMenuOpen = false">
            Главная
          </router-link>
          <template v-if="authStore.isAuthenticated">
            <router-link to="/dashboard" class="nav-link px-4 py-2" active-class="active-nav-link" @click="isMobileMenuOpen = false">
              Статистика
            </router-link>
            <button @click="() => { handleLogout(); isMobileMenuOpen = false; }" class="nav-link px-4 py-2">
              Выйти
            </button>
            <div v-if="authStore.user" class="pt-2 text-[color:var(--color-primary)]">
              Hi, {{ authStore.user.nickname }}
            </div>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link px-4 py-2" active-class="active-nav-link" @click="isMobileMenuOpen = false">
              Войти
            </router-link>
            <router-link to="/register" class="btn-primary px-4 py-2 text-sm" @click="isMobileMenuOpen = false">
              Регистрация
            </router-link>
          </template>
        </nav>
      </div>
    </header>

    <!-- Main Content Slot -->
    <main class="flex-grow container mx-auto px-4 py-8 max-w-6xl">
      <slot />
    </main>

    <!-- Footer -->
    <!-- <footer class="mt-auto border-t border-[color:var(--color-border)] bg-[color:var(--color-card)] py-6">
      <div class="container mx-auto px-4 text-center text-sm text-[color:var(--color-muted-foreground)]">
      </div>
    </footer> -->
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router';
import { useTheme } from '@/composables/useTheme';

const authStore = useAuthStore();
const router = useRouter();
const { theme, toggleTheme } = useTheme();
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
/* You can add component-specific styles here if needed */
</style>
