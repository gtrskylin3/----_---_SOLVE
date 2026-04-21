<script setup>
import { onMounted } from 'vue';
import DefaultLayout from './components/layouts/DefaultLayout.vue';
import { useAuthStore } from '@/stores/auth.js';

const authStore = useAuthStore();

onMounted(() => {
  authStore.fetchUser();
});
</script>

<template>
  <DefaultLayout>
    <router-view />
  </DefaultLayout>
</template>

<style scoped>
/* App-wide styles can go here if necessary */
</style>
