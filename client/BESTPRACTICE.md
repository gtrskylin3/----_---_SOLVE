# Complete Guide: Tailwind CSS v4 + Vite 8 + Vue 3.6

## Introduction

This guide covers the latest versions as of April 2026:
- **Tailwind CSS v4.2** – A ground-up rewrite with CSS-first configuration and significant performance improvements 
- **Vite 8** – Now uses Rolldown and Oxc instead of esbuild and Rollup 
- **Vue 3.6** – Introduces experimental Vapor Mode and stable composition features 

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| Node.js | 20.19+ or 22.12+ | Required for Vite 8  |
| Package Manager | pnpm / npm / yarn / bun | Any modern package manager |

---

## Part 1: Creating a New Vue 3.6 Project with Vite 8

### Step 1.1: Scaffold the Project

```bash
# Using pnpm (recommended)
pnpm create vite@latest my-vue-app -- --template vue-ts

# Using npm
npm create vite@latest my-vue-app -- --template vue-ts

# Using yarn
yarn create vite@latest my-vue-app --template vue-ts

# Using bun
bun create vite@latest my-vue-app --template vue-ts
```

Navigate into the project directory:
```bash
cd my-vue-app
```

### Step 1.2: Verify Vite 8 Installation

Check that your `package.json` has Vite 8:
```json
{
  "devDependencies": {
    "vite": "^8.0.0"
  }
}
```

If not, upgrade manually:
```bash
pnpm add -D vite@latest
```

**Important Vite 8 Changes:**
- Uses Rolldown instead of esbuild for dependency optimization
- Uses Oxc instead of esbuild for JavaScript transformation
- The `transformWithEsbuild` function is deprecated (use `transformWithOxc` instead)
- Browser target updated to Chrome 111+, Edge 111+, Firefox 114+, Safari 16.4+ 

---

## Part 2: Installing Tailwind CSS v4

### Step 2.1: Install Dependencies

```bash
pnpm add -D tailwindcss @tailwindcss/vite
```

> **Note:** Tailwind CSS v4 no longer requires `postcss` or `autoprefixer` as separate dependencies – they're bundled internally .

### Step 2.2: Configure Vite Plugin

Update `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),  // Add Tailwind plugin
  ],
})
```

### Step 2.3: Import Tailwind in Your CSS

Create or update `src/style.css`:

```css
@import "tailwindcss";
```

Then import it in `src/main.ts`:

```typescript
import { createApp } from 'vue'
import './style.css'  // Tailwind import
import App from './App.vue'

createApp(App).mount('#app')
```

### Step 2.4: Tailwind v4 Configuration (CSS-First Approach)

Unlike Tailwind v3, **there is no `tailwind.config.js`** in v4. Configuration is done directly in CSS using the `@theme` directive .

Create or update `src/style.css` with custom configuration:

```css
@import "tailwindcss";

@theme {
  /* Custom colors */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  
  /* Custom fonts */
  --font-display: "Inter", sans-serif;
  
  /* Custom breakpoints */
  --breakpoint-3xl: 1920px;
  
  /* Custom spacing */
  --spacing-18: 4.5rem;
}

/* Custom utilities (if needed) */
@utility text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}
```

**Key Changes from Tailwind v3 to v4 :**
- No `tailwind.config.js` – use CSS `@theme` directive
- No `content` array – automatic content detection
- No `mode: "jit"` – JIT is always enabled by default
- New plugin API for compatibility packages

---

## Part 3: Vue 3.6 Integration

### Step 3.1: Ensure Vue 3.6

Check your `package.json`:
```json
{
  "dependencies": {
    "vue": "^3.6.0"
  }
}
```

If upgrading from an older version:
```bash
pnpm add vue@latest
```

### Step 3.2: Vue 3.6 New Features You Can Use

#### `useTemplateRef()` – Replaces template refs (Vue 3.5+)

```vue
<script setup lang="ts">
import { useTemplateRef, onMounted } from 'vue'

// Instead of const inputRef = ref<HTMLInputElement | null>(null)
const inputRef = useTemplateRef<HTMLInputElement>('input')

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <input ref="input" type="text" />
</template>
```


#### `useId()` – Stable SSR-compatible IDs

```vue
<script setup lang="ts">
import { useId } from 'vue'

const formId = useId()
const emailId = `${formId}-email`
const passwordId = `${formId}-password`
</script>

<template>
  <div>
    <label :for="emailId">Email</label>
    <input :id="emailId" type="email" />
    
    <label :for="passwordId">Password</label>
    <input :id="passwordId" type="password" />
  </div>
</template>
```


#### `defineModel()` – Two-way binding made easy (Stable in Vue 3.4+)

```vue
<!-- CustomInput.vue -->
<script setup lang="ts">
const model = defineModel<string>()
// Or with options: defineModel<string>({ required: true })
</script>

<template>
  <input v-model="model" />
</template>
```

Usage:
```vue
<script setup lang="ts">
import CustomInput from './CustomInput.vue'
import { ref } from 'vue'

const text = ref('')
</script>

<template>
  <CustomInput v-model="text" />
</template>
```


#### Experimental Vapor Mode (Vue 3.6)

Vapor Mode removes the need for a Virtual DOM, compiling to more efficient JavaScript :

```vue
<script setup vapor>
// Opt-in to Vapor Mode compilation
const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

> **Warning:** Vapor Mode is experimental in Vue 3.6. Use `createVaporApp()` instead of `createApp()` for full Vapor Mode applications .

---

## Part 4: Complete Working Example

### Project Structure
```
my-vue-app/
├── src/
│   ├── components/
│   │   └── Button.vue
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### `src/style.css` – Full Tailwind v4 Configuration

```css
@import "tailwindcss";

@theme {
  /* Custom color palette */
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-secondary: #64748b;
  --color-accent: #8b5cf6;
  
  /* Custom fonts */
  --font-sans: "Inter", system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  
  /* Custom breakpoints */
  --breakpoint-xs: 480px;
  --breakpoint-3xl: 1920px;
  
  /* Custom animations */
  --animate-slide-up: slide-up 0.3s ease-out;
  
  /* Custom border radius */
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@utility container {
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
  
  @media (width >= 640px) {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  @media (width >= 1024px) {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}
```

### `src/components/Button.vue` – Reusable Component

```vue
<script setup lang="ts">
import { useId } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonId = useId()

const variantClasses = {
  primary: 'bg-primary hover:bg-primary-dark text-white',
  secondary: 'bg-secondary text-white',
  outline: 'border-2 border-primary text-primary hover:bg-primary hover:text-white',
}

const sizeClasses = {
  sm: 'px-3 py-1.5 text-sm rounded-lg',
  md: 'px-4 py-2 text-base rounded-xl',
  lg: 'px-6 py-3 text-lg rounded-2xl',
}

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<template>
  <button
    :id="buttonId"
    :disabled="disabled"
    :class="[
      variantClasses[variant],
      sizeClasses[size],
      'font-medium transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-primary/50',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'active:scale-95',
    ]"
    @click="handleClick"
  >
    <slot />
  </button>
</template>
```

### `src/App.vue` – Main Application

```vue
<script setup lang="ts">
import { ref, useTemplateRef } from 'vue'
import Button from './components/Button.vue'

const count = ref(0)
const message = ref('')
const buttonRef = useTemplateRef('mainButton')

const increment = () => {
  count.value++
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
    <!-- Header -->
    <header class="border-b border-gray-200 bg-white/80 backdrop-blur-sm dark:border-gray-700 dark:bg-gray-900/80">
      <div class="container py-4">
        <h1 class="text-2xl font-bold text-primary">
          Tailwind v4 + Vite 8 + Vue 3.6
        </h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container py-8">
      <!-- Counter Section -->
      <div class="mb-8 rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
        <h2 class="mb-4 text-xl font-semibold">Counter Example</h2>
        <div class="flex items-center gap-4">
          <Button @click="increment">
            Clicked {{ count }} times
          </Button>
          <p class="text-gray-600 dark:text-gray-300">
            {{ count === 0 ? 'Click the button!' : 'Great job!' }}
          </p>
        </div>
      </div>

      <!-- Input Section with defineModel -->
      <div class="rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
        <h2 class="mb-4 text-xl font-semibold">Two-way Binding</h2>
        <input
          v-model="message"
          type="text"
          placeholder="Type something..."
          class="w-full rounded-xl border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
        />
        <p v-if="message" class="mt-4 text-gray-600 dark:text-gray-300">
          You typed: <span class="font-medium text-primary">{{ message }}</span>
        </p>
      </div>

      <!-- Responsive Grid -->
      <div class="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div v-for="i in 3" :key="i" class="rounded-2xl bg-white p-6 shadow-lg transition-transform hover:scale-105 dark:bg-gray-800">
          <div class="mb-3 h-12 w-12 rounded-xl bg-primary/10 p-2 text-primary">
            <svg class="h-full w-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </div>
          <h3 class="mb-2 text-lg font-semibold">Card {{ i }}</h3>
          <p class="text-gray-600 dark:text-gray-300">
            This card demonstrates responsive grid layout with Tailwind's breakpoints.
          </p>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-gray-200 bg-white py-6 dark:border-gray-700 dark:bg-gray-900">
      <div class="container text-center text-sm text-gray-500 dark:text-gray-400">
        Built with Vue 3.6, Vite 8, and Tailwind CSS v4.2
      </div>
    </footer>
  </div>
</template>
```

### `vite.config.ts` – Full Configuration

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  // Optional: Configure Rolldown options (Vite 8 feature)
  optimizeDeps: {
    rolldownOptions: {
      // Custom Rolldown optimization options
    },
  },
  // Optional: Configure Oxc for JS transformation (Vite 8 feature)
  oxc: {
    // Custom Oxc transformation options
  },
})
```

### Running the Development Server

```bash
pnpm run dev
```

### Building for Production

```bash
pnpm run build
pnpm run preview
```

---

## Part 5: Troubleshooting Common Issues

### Issue 1: Tailwind Classes Not Working

**Solution:** Ensure your CSS file is imported correctly in `main.ts` and the Vite plugin is registered.

```typescript
// vite.config.ts – VERIFY this is present
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],  // tailwindcss() must be here
})
```


### Issue 2: Dynamic Classes Not Being Generated

Tailwind v4 automatically detects content, but for dynamic classes, use full class names:

```vue
<!-- ❌ Won't work -->
<div :class="`text-${color}-500`"></div>

<!-- ✅ Will work -->
<div :class="{ 'text-red-500': color === 'red', 'text-blue-500': color === 'blue' }"></div>
```


### Issue 3: Vite 8 Migration Errors

If you were using esbuild-specific options, update them :

```typescript
// Old (Vite 7 and below)
export default defineConfig({
  optimizeDeps: {
    esbuildOptions: { minify: true }
  }
})

// New (Vite 8)
export default defineConfig({
  optimizeDeps: {
    rolldownOptions: {
      output: { minify: true }
    }
  }
})
```

### Issue 4: TypeScript Errors with Vue 3.6

Ensure your `tsconfig.json` has proper Vue support:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "jsxImportSource": "vue",
    "types": ["vite/client"]
  },
  "include": ["src/**/*.ts", "src/**/*.vue"]
}
```


---

## Part 6: Key Features Summary

### Tailwind CSS v4.2 New Features 
| Feature | Description |
|---------|-------------|
| **New Colors** | Mauve, olive, mist, taupe palettes |
| **Logical Properties** | `pbs-*`, `mbs-*`, `inset-s-*` for writing-mode support |
| **Size Utilities** | `inline-*` and `block-*` (logical width/height) |
| **Font Features** | `font-features-*` for OpenType features |
| **Webpack Plugin** | Official `@tailwindcss/webpack` package |

### Vite 8 New Features 
| Feature | Description |
|---------|-------------|
| **Rolldown** | Replaces Rollup for bundling |
| **Oxc** | Replaces esbuild for JS transformation |
| **TSConfig Paths** | Built-in support for `paths` option |
| **Decorator Metadata** | Built-in `emitDecoratorMetadata` support |

### Vue 3.6 New Features 
| Feature | Status | Description |
|---------|--------|-------------|
| **Vapor Mode** | Experimental | No Virtual DOM compilation |
| **useTemplateRef()** | Stable | Better typed template refs |
| **useId()** | Stable | SSR-compatible unique IDs |
| **defineModel()** | Stable | Simplified two-way binding |
| **Alien Signals** | Stable | Improved reactivity memory usage |

---

## Part 7: Additional Resources

- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
- [Vite 8 Migration Guide](https://vite.dev/guide/migration)
- [Vue 3.6 Documentation](https://vuejs.org/)
- [Vue 3.6 API Changes](https://github.com/vuejs/core/blob/main/CHANGELOG.md)

---

## Quick Start Template (One-Command Setup)

If you want a faster setup, you can use the `create-bawo-frontend` CLI which supports Vue + Tailwind v4 :

```bash
npx create-bawo-frontend my-app --framework vue --ts --tailwind v4 -y
cd my-app
pnpm run dev
```

This automatically scaffolds a Vue 3 + TypeScript + Tailwind v4 project with Pinia state management.