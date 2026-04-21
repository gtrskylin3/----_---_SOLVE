<template>
  <div class="space-y-8">
    <!-- Filter Section -->
    <div class="flex flex-col sm:flex-row gap-4">
      <div class="flex-1">
        <label for="kes-filter" class="block text-sm font-medium text-muted-foreground mb-1">Фильтр по коду КЭС</label>
        <select id="kes-filter" v-model="selectedKes" @change="handleFilterChange" class="input-field">
          <option value="">Все коды КЭС</option>
          <option v-for="kes in kesCodes" :key="kes" :value="kes.split(' ')[0]">{{ kes }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-muted-foreground mb-1">Фильтр по части</label>
        <div class="flex gap-2">
          <button @click="setTaskTypeFilter('')" :class="['filter-btn', { 'active': taskTypeFilter === '' }]">Все части</button>
          <button @click="setTaskTypeFilter('short-answer')" :class="['filter-btn', { 'active': taskTypeFilter === 'short-answer' }]">Часть 1</button>
          <button @click="setTaskTypeFilter('not-short-answer')" :class="['filter-btn', { 'active': taskTypeFilter === 'not-short-answer' }]">Часть 2</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center text-muted-foreground py-12">
      Загрузка заданий...
    </div>
    <div v-else-if="error" class="text-center text-destructive py-12">
      Ошибка загрузки заданий: {{ error.message }}
      <p class="text-muted-foreground mt-2">Убедитесь, что бэкенд запущен и задания загружены в базу данных.</p>
    </div>
    <div v-else-if="tasks.length === 0" class="text-center py-12">
        <div class="mx-auto w-24 h-24 rounded-full bg-[#0f0f0f] flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-[#333]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
        </div>
        <h3 class="text-xl font-medium text-[#f0f0f0] mb-1">Задания не найдены</h3>
        <p class="text-[#9ca3af] mb-4">Задания, соответствующие текущим фильтрам, не найдены. Попробуйте изменить настройки фильтра.</p>
    </div>
    <div v-else class="space-y-4">
      <TaskCard v-for="task in tasks" :key="task.guid" :task="task" @task-solved="getTasks" />
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-8">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-secondary">Назад</button>
      <span class="text-muted-foreground">Страница {{ currentPage }} из {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-secondary">Вперед</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, nextTick, computed } from 'vue';
import { fetchTasks, fetchKesCodes } from '../api/tasks';
import TaskCard from '../components/TaskCard.vue';

const tasks = ref([]);
const loading = ref(true);
const error = ref(null);
const kesCodes = ref([]);
const selectedKes = ref('');
const taskTypeFilter = ref('');

const totalTasks = ref(0);
const currentPage = ref(1);
const tasksPerPage = 15;

const totalPages = computed(() => Math.ceil(totalTasks.value / tasksPerPage));

const getTasks = async () => {
  loading.value = true;
  try {
    const kes = selectedKes.value || null;
    const typeFilter = taskTypeFilter.value || null;
    const skip = (currentPage.value - 1) * tasksPerPage;
    
    const response = await fetchTasks(kes, typeFilter, skip, tasksPerPage);
    tasks.value = response.tasks;
    totalTasks.value = response.total;

  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const getKesCodes = async () => {
  try {
    kesCodes.value = await fetchKesCodes();
  } catch (err) {
    console.error("Failed to fetch KES codes", err);
  }
};

const handleFilterChange = () => {
  currentPage.value = 1;
  getTasks();
};

const setTaskTypeFilter = (filter) => {
  taskTypeFilter.value = filter;
  handleFilterChange();
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    getTasks();
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    getTasks();
  }
};

onMounted(async () => {
  await getKesCodes();
  await getTasks();
});

// Watch for changes in tasks and trigger MathJax typesetting once
watch(tasks, async (newTasks) => {
  if (newTasks.length > 0 && window.MathJax) {
    await nextTick(); // Wait for DOM to update
    window.MathJax.typesetPromise();
  }
}, { deep: true });
</script>

<style scoped>
/* Scoped styles for HomeView if necessary */
</style>
