# shadcn-svelte Customization Guide

## Theme Customization

### CSS Variables
Override default CSS variables in your CSS:

```css
:root {
  /* Brand colors */
  --brand: 142 76% 36%;
  --brand-foreground: 355 100% 97%;

  /* Semantic colors */
  --info: 199 89% 48%;
  --info-foreground: 210 40% 98%;
  --warning: 38 92% 50%;
  --warning-foreground: 48 96% 89%;
  --success: 142 76% 36%;
  --success-foreground: 355 100% 97%;

  /* Custom spacing */
  --spacing-18: 4.5rem;
  --spacing-88: 22rem;

  /* Custom border radius */
  --radius: 0.75rem;
}

.dark {
  --brand: 142 70% 45%;
  --brand-foreground: 144 61% 20%;
  --info: 199 89% 68%;
  --warning: 48 96% 89%;
  --success: 142 70% 45%;
}
```

### Tailwind Configuration
Extend your Tailwind config:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
}
```

## Component Customization

### Variant Creation
```typescript
// src/lib/components/ui/button/utils.ts
import { cva, type VariantProps } from "tailwind-variants";

export const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Custom variants
        gradient: "bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600",
        glass: "bg-white/20 backdrop-blur-sm border border-white/20 text-white hover:bg-white/30",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
        // Custom sizes
        xl: "h-12 rounded-lg px-10 text-base",
        xs: "h-8 rounded px-2 text-xs",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export type ButtonVariants = VariantProps<typeof buttonVariants>;
```

### Custom Component
```svelte
<!-- src/lib/components/ui/custom-card.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";
  import type { HTMLAttributes } from "svelte/elements";

  interface Props extends HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "elevated" | "outlined" | "glass";
    hover?: boolean;
  }

  let {
    variant = "default",
    hover = true,
    class: className,
    children,
    ...restProps
  }: Props = $props();

  const variants = {
    default: "bg-card text-card-foreground rounded-lg shadow-sm border",
    elevated: "bg-card text-card-foreground rounded-lg shadow-xl border-0",
    outlined: "bg-transparent text-card-foreground rounded-lg border-2 border-card",
    glass: "bg-white/10 backdrop-blur-md rounded-lg border border-white/20 text-card-foreground",
  };

  const hoverEffects = hover ? "hover:shadow-lg transition-shadow duration-200" : "";
</script>

<div
  class={cn(variants[variant], hoverEffects, className)}
  {...restProps}
>
  {@render children()}
</div>
```

### Component Composition
```svelte
<script lang="ts">
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";

  interface UserCardProps {
    name: string;
    email: string;
    avatar?: string;
    role: string;
    skills: string[];
  }

  let { name, email, avatar, role, skills }: UserCardProps = $props();
</script>

<Card class="overflow-hidden hover:shadow-xl transition-shadow duration-300">
  <div class="h-32 bg-gradient-to-r from-purple-500 to-pink-500"></div>
  <Card.Content class="pt-0">
    <div class="flex flex-col items-center -mt-16">
      <Avatar class="h-32 w-32 border-4 border-background shadow-lg">
        <AvatarImage src={avatar} alt={name} />
        <AvatarFallback class="text-2xl">{name.slice(0, 2).toUpperCase()}</AvatarFallback>
      </Avatar>
      <Card.Title class="mt-4 text-xl text-center">{name}</Card.Title>
      <Card.Description class="text-center">{role}</Card.Description>
      <p class="text-sm text-muted-foreground text-center mt-1">{email}</p>

      <div class="flex flex-wrap gap-2 mt-4 justify-center">
        {#each skills as skill}
          <Badge variant="secondary" class="text-xs">{skill}</Badge>
        {/each}
      </div>

      <div class="flex gap-2 mt-6 w-full">
        <Button variant="outline" class="flex-1">Message</Button>
        <Button class="flex-1">Follow</Button>
      </div>
    </div>
  </Card.Content>
</Card>
```

## Dark Mode Implementation

### Theme Provider
```svelte
<!-- src/lib/components/theme-provider.svelte -->
<script lang="ts">
  import { browser } from '$app/environment';
  import { writable } from 'svelte/store';
  import { setContext, onMount } from 'svelte';

  const theme = writable<'light' | 'dark'>('light');

  onMount(() => {
    if (browser) {
      const stored = localStorage.getItem('theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initial = stored || (prefersDark ? 'dark' : 'light');

      theme.set(initial as 'light' | 'dark');
      document.documentElement.classList.toggle('dark', initial === 'dark');

      theme.subscribe(value => {
        localStorage.setItem('theme', value);
        document.documentElement.classList.toggle('dark', value === 'dark');
      });
    }
  });

  setContext('theme', theme);
</script>

<slot />
```

### Theme Toggle
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { getContext } from 'svelte';
  import { Moon, Sun } from "@lucide/svelte";

  const theme = getContext('theme');
  $: isDark = $theme === 'dark';
</script>

<Button
  variant="outline"
  size="icon"
  onclick={() => theme.update(prev => prev === 'light' ? 'dark' : 'light')}
  aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
>
  {#if isDark}
    <Sun class="h-4 w-4" />
  {:else}
    <Moon class="h-4 w-4" />
  {/if}
</Button>
```

### System Preference Detection
```svelte
<script lang="ts">
  import { onMount } from 'svelte';

  let prefersDark = $state(false);

  onMount(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    prefersDark = mediaQuery.matches;

    const handleChange = (e: MediaQueryListEvent) => {
      prefersDark = e.matches;
    };

    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  });
</script>

{#if prefersDark}
  <p>System prefers dark mode</p>
{:else}
  <p>System prefers light mode</p>
{/if}
```

## Advanced Customization

### Animation Presets
```css
/* Custom animations for components */
@keyframes shimmer {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Utility classes */
.animate-shimmer {
  animation: shimmer 2s infinite linear;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  background-size: 200px 100%;
}

.animate-bounce-in {
  animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### Glass Morphism
```svelte
<script lang="ts">
  import { Card } from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
</script>

<!-- Glass morphism card -->
<Card
  class={cn(
    "bg-white/10 backdrop-blur-lg border border-white/20",
    "shadow-xl shadow-white/10"
  )}
>
  <Card.Content>
    <Card.Title class="text-white">Glass Card</Card.Title>
    <Card.Description class="text-white/80">
      Beautiful glass effect with backdrop blur
    </Card.Description>
  </Card.Content>
</Card>
```

### Gradient Variants
```typescript
// Button gradient variants
export const gradientVariants = {
  primary: "bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700",
  secondary: "bg-gradient-to-r from-green-400 to-blue-500 hover:from-green-500 hover:to-blue-600",
  accent: "bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600",
  warm: "bg-gradient-to-r from-orange-400 to-red-500 hover:from-orange-500 hover:to-red-600",
  cool: "bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-500 hover:to-blue-600",
};
```

## Best Practices

### Performance
- Use CSS variables for dynamic theming
- Leverage Tailwind's JIT compilation
- Minimize custom CSS
- Optimize bundle size with tree shaking

### Accessibility
- Maintain sufficient color contrast ratios
- Respect user's motion preferences
- Ensure keyboard navigation works
- Test with screen readers

### Maintainability
- Document custom variants
- Use consistent naming conventions
- Keep custom CSS minimal
- Test across browsers and devices