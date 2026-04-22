<template>
  <div class="task-card">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
      <div class="flex-1">
        <div class="flex flex-col md:flex-row gap-8 items-start">
          <div class="question-html prose max-w-none flex-1">
            <div v-html="task.question_html"></div>
          </div>
          <div v-if="processedImages.length > 0" class="flex-shrink-0">
            <img v-for="(image, index) in processedImages" :key="index" :src="image" alt="Изображение к заданию" class="max-w-xs h-auto object-contain rounded-lg border border-[color:var(--color-border)] bg-white">
          </div>
        </div>

        <!-- Answer Input/Actions -->
        <div class="mt-6">
          <div v-if="task.part === 1" class="flex items-center gap-2">
            <input v-model="userAnswer" type="text" placeholder="Ваш ответ" class="input-field flex-grow" @keyup.enter="handleCheckAnswer" :disabled="isTaskCompleted" />
            <button @click="handleCheckAnswer" class="btn-primary" :disabled="isChecking || isTaskCompleted">
              {{ isChecking ? 'Проверка...' : 'Проверить' }}
            </button>
          </div>
          <div v-else>
            <button v-if="!isTaskCompleted" @click="handleMarkDone" class="btn-secondary" :disabled="isMarkingDone">
              {{ isMarkingDone ? 'Сохранение...' : 'Отметить как выполненное' }}
            </button>
            <button v-else disabled class="btn-success" :class="{ 'opacity-50 cursor-not-allowed': isTaskCompleted }">
              ✓ Выполнено
            </button>
          </div>
        </div>

        <!-- Result Display for Part 1 -->
        <div v-if="checkResult && task.part === 1" class="mt-4 p-4 rounded-lg" :class="resultClass">
          <p class="font-semibold">{{ resultMessage }}</p>
          <p v-if="checkResult.user_answer">Ваш ответ: {{ checkResult.user_answer }}</p>
        </div>

        <!-- Success Display for Part 2 (when marked as done) -->
        <div v-if="markDoneResult && task.part === 2" class="mt-4 p-4 rounded-lg" :class="markDoneResultClass">
          <p class="font-semibold">{{ markDoneResultMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed, ref, watch } from 'vue';
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
const markDoneResult = ref(null);
const isChecking = ref(false);
const isMarkingDone = ref(false);

// Проверяем, выполнено ли задание
const isTaskCompleted = computed(() => {
  return authStore.isAuthenticated && 
         authStore.user?.solved_tasks?.includes(props.task.id);
});

// Сбрасываем результат отметки при смене задачи
watch(() => props.task.id, () => {
  markDoneResult.value = null;
  checkResult.value = null;
  userAnswer.value = '';
});

const processedImages = computed(() => {
  if (!props.task.images || props.task.images.length === 0) return [];
  return props.task.images.map(imagePath => {
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) return imagePath;
    const separator = imagePath.startsWith('/') ? '' : '/';
    return FIPI_DATA_BASE_URL.replace(/\/$/, '') + separator + imagePath;
  });
});

const handleCheckAnswer = async () => {
  if (!userAnswer.value.trim() || isChecking.value || isTaskCompleted.value) return;
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
        alert('Пожалуйста, войдите в систему, чтобы сохранить ваш прогресс.');
        return;
    }
    if (isTaskCompleted.value) return;
    
    isMarkingDone.value = true;
    markDoneResult.value = null;
    
    try {
        await authStore.markTaskAsDone(props.task.id);
        
        // Показываем сообщение об успехе
        markDoneResult.value = { result: 'correct' };
        
        // Автоматически скрываем сообщение через 3 секунды
        setTimeout(() => {
            markDoneResult.value = null;
        }, 3000);
    } catch (error) {
        markDoneResult.value = { result: 'error' };
        setTimeout(() => {
            markDoneResult.value = null;
        }, 3000);
    } finally {
        isMarkingDone.value = false;
    }
};

const resultMessage = computed(() => {
  if (!checkResult.value) return '';
  switch (checkResult.value.result) {
    case 'correct': return '✅ Правильно!';
    case 'incorrect': return '❌ Неправильно. Попробуйте еще раз!';
    case 'error': return '⚠️ Произошла ошибка при проверке ответа.';
    default: return 'Получен неизвестный результат.';
  }
});

const resultClass = computed(() => {
  if (!checkResult.value) return '';
  switch (checkResult.value.result) {
    case 'correct': return 'bg-[color:var(--color-success)]/20 text-[color:var(--color-success-foreground)] border border-[color:var(--color-success)]/30';
    case 'incorrect': return 'bg-[color:var(--color-destructive)]/20 text-[color:var(--color-destructive-foreground)] border border-[color:var(--color-destructive)]/30';
    default: return 'bg-amber-500/20 text-amber-300 border border-amber-800';
  }
});

// Для отметки выполненного (часть 2)
const markDoneResultMessage = computed(() => {
  if (!markDoneResult.value) return '';
  switch (markDoneResult.value.result) {
    case 'correct': return '✓ Задание отмечено как выполненное!';
    case 'error': return '⚠️ Не удалось отметить задание. Попробуйте позже.';
    default: return '';
  }
});

const markDoneResultClass = computed(() => {
  if (!markDoneResult.value) return '';
  switch (markDoneResult.value.result) {
    case 'correct': return 'bg-[color:var(--color-success)]/20 text-[color:var(--color-success-foreground)] border border-[color:var(--color-success)]/30';
    case 'error': return 'bg-[color:var(--color-destructive)]/20 text-[color:var(--color-destructive-foreground)] border border-[color:var(--color-destructive)]/30';
    default: return '';
  }
});
</script>