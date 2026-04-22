<template>
  <div class="task-card">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
      <div class="flex-1">
        <div class="flex flex-col md:flex-row gap-8 items-start">
          <div class="question-html prose prose-invert prose-lg max-w-none flex-1">
            <div v-html="task.question_html"></div>
          </div>
          <div v-if="processedImages.length > 0" class="flex-shrink-0">
            <img v-for="(image, index) in processedImages" :key="index" :src="image" alt="Изображение к заданию" class="max-w-xs h-auto object-contain rounded-lg border border-border bg-white">
          </div>
        </div>

        <!-- Answer Input/Actions -->
        <div class="mt-6">
          <div v-if="task.task_type === 'short_answer'" class="flex items-center gap-2">
            <input v-model="userAnswer" type="text" placeholder="Ваш ответ" class="input-field flex-grow" @keyup.enter="handleCheckAnswer" />
            <button @click="handleCheckAnswer" class="btn-primary" :disabled="isChecking">
              {{ isChecking ? 'Проверка...' : 'Проверить' }}
            </button>
          </div>
          <div v-else>
            <button @click="handleMarkDone" class="btn-secondary" :disabled="isMarkingDone">
              {{ isMarkingDone ? 'Сохранение...' : 'Отметить как выполненное' }}
            </button>
          </div>
        </div>

        <!-- Result Display -->
        <div v-if="checkResult" class="mt-4 p-4 rounded-lg" :class="resultClass">
          <p class="font-semibold">{{ resultMessage }}</p>
          <p v-if="checkResult.user_answer">Ваш ответ: {{ checkResult.user_answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed, ref } from 'vue';
import { checkTaskAnswer } from '../api/tasks';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const authStore = useAuthStore();
const FIPI_DATA_BASE_URL = "https://ege.fipi.ru/";

const userAnswer = ref('');
const checkResult = ref(null);
const isChecking = ref(false);
const isMarkingDone = ref(false);

const processedImages = computed(() => {
  if (!props.task.images || props.task.images.length === 0) return [];
  return props.task.images.map(imagePath => {
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) return imagePath;
    const separator = imagePath.startsWith('/') ? '' : '/';
    return FIPI_DATA_BASE_URL.replace(/\/$/, '') + separator + imagePath;
  });
});

const handleCheckAnswer = async () => {
  if (!userAnswer.value.trim() || isChecking.value) return;
  isChecking.value = true;
  checkResult.value = null;

  try {
    const result = await checkTaskAnswer(props.task.id, userAnswer.value);
    checkResult.value = result;
    if (result && result.result === 'correct' && result.solved_tasks && authStore.isAuthenticated) {
      authStore.user.solved_tasks = result.solved_tasks;
    }
  } catch (error) {
    checkResult.value = { result: 'error', user_answer: 'Не удалось получить ответ' };
  } finally {
    isChecking.value = false;
  }
};

const handleMarkDone = async () => {
    if (!authStore.isAuthenticated) {
        // Maybe show a message encouraging login
        alert('Пожалуйста, войдите в систему, чтобы сохранить ваш прогресс.');
        return;
    }
    isMarkingDone.value = true;
    await authStore.markTaskAsDone(props.task.id);
    isMarkingDone.value = false;
    // Optionally hide the card or show a "Done" state
};

const resultMessage = computed(() => {
  if (!checkResult.value) return '';
  switch (checkResult.value.result) {
    case 'correct': return 'Правильно!';
    case 'incorrect': return 'Неправильно. Попробуйте еще раз!';
    case 'error': return 'Произошла ошибка при проверке ответа.';
    default: return 'Получен неизвестный результат.';
  }
});

const resultClass = computed(() => {
  if (!checkResult.value) return '';
  switch (checkResult.value.result) {
    case 'correct': return 'bg-emerald-900/50 text-emerald-300 border border-emerald-800';
    case 'incorrect': return 'bg-rose-900/50 text-rose-300 border border-rose-800';
    default: return 'bg-amber-900/50 text-amber-300 border border-amber-800';
  }
});
</script>

<style scoped>
.prose {
  color: var(--color-foreground);
}
</style>
