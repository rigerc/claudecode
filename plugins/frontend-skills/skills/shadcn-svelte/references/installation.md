# shadcn-svelte Installation Guide

## Prerequisites
- Node.js 18+
- Svelte or SvelteKit project
- Tailwind CSS configured (recommended)

## Quick Installation

### 1. Initialize shadcn-svelte
```bash
# New project
npm create svelte@latest my-app
cd my-app
npx shadcn-svelte@latest init

# Existing project
npx shadcn-svelte@latest init
```

### 2. Install Components
```bash
# Single component
npx shadcn-svelte@latest add button

# Multiple components
npx shadcn-svelte@latest add button card input

# List available components
npx shadcn-svelte@latest add --help
```

## Manual Setup

### Dependencies
```bash
npm install tailwind-variants clsx tailwind-merge tw-animate-css @lucide/svelte bits-ui
```

### Tailwind Configuration
```javascript
// tailwind.config.js
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)"
      },
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))"
        }
        // ... more colors
      }
    }
  },
  plugins: [require("tailwindcss-animate")]
} satisfies Config;

export default config;
```

### CSS Variables
```css
/* src/app.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Utils File
```typescript
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Framework-Specific Setup

### SvelteKit
```bash
npx create-svelte@latest my-app
cd my-app
npx shadcn-svelte@latest init
```

### Astro
```bash
npm create astro@latest my-app
cd my-app
npx shadcn-svelte@latest init
```

**Important**: Use `client` directives for interactive components in Astro:
```astro
---
import { Button } from "$lib/components/ui/button";
---
<Button client:load>Click me</Button>
```

## Verification

Test installation with a simple component:
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<Button>Test Button</Button>
```

## Troubleshooting

### Common Issues

**Tailwind classes not working**
- Verify CSS variables are defined
- Check Tailwind configuration
- Ensure CSS file is imported

**TypeScript errors**
- Install type definitions
- Check component imports
- Verify utils.ts export

**Components not found**
- Run `npx shadcn-svelte@latest add <component>`
- Check `$lib/components/ui/` directory
- Verify proper file structure