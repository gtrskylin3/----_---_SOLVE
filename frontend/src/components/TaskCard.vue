<template>
  <div class="task-card">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
      <div class="flex-1">
        <div class="question-html prose prose-invert prose-lg max-w-none">
          <!-- MathML content will be rendered here by MathJax -->
          <div v-html="task.question_html"></div>
        </div>

        <div v-if="processedImages.length > 0" class="mt-4 flex flex-wrap gap-4">
          <img v-for="(image, index) in processedImages" :key="index" :src="image" alt="Task Image" class="max-w-[300px] h-auto object-contain rounded-lg border border-border">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const FIPI_DATA_BASE_URL = "https://ege.fipi.ru/"; 

const processedImages = computed(() => {
  if (!props.task.images || props.task.images.length === 0) {
    return [];
  }
  return props.task.images.map(imagePath => {
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
      return imagePath;
    }
    // Ensure there's no double slash if imagePath already starts with '/'
    const separator = imagePath.startsWith('/') ? '' : '/';
    return FIPI_DATA_BASE_URL.replace(/\/$/, '') + separator + imagePath;
  });
});
</script>

<style scoped>
/* Scoped styles for TaskCard if necessary */
.prose {
  color: var(--color-foreground);
}
</style>
