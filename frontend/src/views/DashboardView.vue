<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[color:var(--color-foreground)] press-start-font">Панель Управления</h2>
        <p class="text-[color:var(--color-muted-foreground)] mt-1">Ваша статистика и решенные задачи</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-[color:var(--color-border)]">
      <button @click="activeTab = 'stats'" :class="['tab-btn', { 'active': activeTab === 'stats' }]">
        Статистика
      </button>
      <button @click="activeTab = 'solved'" :class="['tab-btn', { 'active': activeTab === 'solved' }]">
        Решенные задачи
      </button>
    </div>

    <!-- Stats Tab -->
    <div v-if="activeTab === 'stats'">
      <div v-if="loading" class="text-center py-12">Загрузка статистики...</div>
      <div v-else-if="error" class="text-center text-[color:var(--color-destructive)] py-12">
        Ошибка загрузки статистики: {{ error.message }}
      </div>
      <div v-else class="stats-card">
        <h3 class="text-lg font-semibold mb-4 press-start-font">Общая статистика</h3>
        <p class="text-3xl font-bold">{{ stats.total_solved }} из {{ stats.total_tasks }}</p>
        <p class="text-[color:var(--color-muted-foreground)]">Всего решено задач</p>

        <div v-if="stats.total_tasks > 0" class="mt-4">
            <div class="w-full bg-[color:var(--color-muted)] rounded-full h-2.5">
                <div 
                    class="bg-[color:var(--color-primary)] h-2.5 rounded-full" 
                    :style="{ width: (stats.total_solved / stats.total_tasks * 100).toFixed(2) + '%' }"
                ></div>
            </div>
            <p class="text-sm text-[color:var(--color-muted-foreground)] mt-1">
                {{ (stats.total_solved / stats.total_tasks * 100).toFixed(2) }}% выполнено
            </p>
        </div>

        <h3 class="text-lg font-semibold mb-4 mt-8 press-start-font">Решено по темам КЭС</h3>
        <div v-if="Object.keys(stats.solved_by_kes).length > 0" class="space-y-2">
            <div v-for="(count, kes) in stats.solved_by_kes" :key="kes" class="flex justify-between items-center">
                <span class="text-sm font-medium">{{ kes }}</span>
                <span class="font-bold">{{ count }}</span>
            </div>
        </div>
        <div v-else class="text-[color:var(--color-muted-foreground)] text-sm">Вы еще не решили ни одной задачи.</div>
      </div>
    </div>

    <!-- Solved Tasks Tab -->
    <div v-if="activeTab === 'solved'">
      <div v-if="loading" class="text-center py-12">Загрузка решенных задач...</div>
       <div v-else-if="error" class="text-center text-[color:var(--color-destructive)] py-12">
        Ошибка загрузки решенных задач: {{ error.message }}
      </div>
      <div v-else-if="solvedTasks.length === 0" class="text-center py-12">
        <h3 class="text-xl font-medium text-[color:var(--color-foreground)]">Нет решенных задач</h3>
        <p class="text-[color:var(--color-muted-foreground)]">Решайте задачи на главной странице, чтобы они появились здесь.</p>
      </div>
      <div v-else class="space-y-4">
        <TaskCard v-for="task in solvedTasks" :key="task.guid" :task="task" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { fetchDashboardStats, fetchSolvedTasks } from '../api/tasks';
import TaskCard from '../components/TaskCard.vue';

const activeTab = ref('stats');
const loading = ref(true);
const error = ref(null);
const stats = ref({ total_solved: 0, solved_by_kes: {} });
const solvedTasks = ref([]);

const loadStats = async () => {
  loading.value = true;
  error.value = null;
  try {
    stats.value = await fetchDashboardStats();
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const loadSolvedTasks = async () => {
  loading.value = true;
  error.value = null;
  try {
    solvedTasks.value = await fetchSolvedTasks();
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadStats();
});

watch(activeTab, (newTab) => {
  if (newTab === 'stats') {
    loadStats();
  } else if (newTab === 'solved') {
    loadSolvedTasks();
  }
});
</script>

<style scoped>
@reference "@/style.css";
.tab-btn {
  @apply px-4 py-2 text-sm font-medium transition-colors duration-200 border-b-2 border-transparent text-[color:var(--color-muted-foreground)] hover:text-[color:var(--color-foreground)];
  border-radius: 0;
}
.tab-btn.active {
  @apply border-[color:var(--color-primary)] text-[color:var(--color-primary)];
}
</style>
