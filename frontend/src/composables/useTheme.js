import { ref, onMounted } from 'vue';

export function useTheme() {
  const theme = ref(localStorage.getItem('theme') || 'dark');

  function applyTheme(newTheme) {
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  const toggleTheme = () => {
    const newTheme = theme.value === 'light' ? 'dark' : 'light';
    theme.value = newTheme;
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  };

  onMounted(() => {
    applyTheme(theme.value);
  });

  return {
    theme,
    toggleTheme,
  };
}
