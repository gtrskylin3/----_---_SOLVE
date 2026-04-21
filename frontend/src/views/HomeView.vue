<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[#f0f0f0] press-start-font">FIPI Math Tasks</h2>
        <p class="text-[#9ca3af] mt-1">Explore the latest tasks from the FIPI database below.</p>
      </div>
    </div>

    <div v-if="loading" class="text-center text-muted-foreground py-12">
      Loading tasks...
    </div>
    <div v-else-if="error" class="text-center text-destructive py-12">
      Error loading tasks: {{ error.message }}
      <p class="text-muted-foreground mt-2">Please ensure the backend is running and tasks are loaded into the database.</p>
    </div>
    <div v-else-if="tasks.length === 0" class="text-center py-12">
        <div class="mx-auto w-24 h-24 rounded-full bg-[#0f0f0f] flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-[#333]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
        </div>
        <h3 class="text-xl font-medium text-[#f0f0f0] mb-1">No tasks found</h3>
        <p class="text-[#9ca3af] mb-4">The database might be empty. Try running the parser.</p>
    </div>
    <div v-else class="space-y-4">
      <TaskCard v-for="task in tasks" :key="task.guid" :task="task" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, nextTick } from 'vue';
import { fetchTasks } from '../api/tasks';
import TaskCard from '../components/TaskCard.vue';

const tasks = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    tasks.value = await fetchTasks();
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
});

// Watch for changes in tasks and trigger MathJax typesetting once
watch(tasks, async (newTasks) => {
  if (newTasks.length > 0 && window.MathJax) {
    await nextTick(); // Wait for DOM to update
    MathJax.typesetPromise();
  }
}, { deep: true });
</script>

<style scoped>
/* Scoped styles for HomeView if necessary */
</style>
