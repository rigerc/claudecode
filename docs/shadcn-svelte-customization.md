# Customization and Theming Guide

This comprehensive guide covers how to customize shadcn-svelte components, create custom themes, and extend the component library to match your brand and design requirements.

## Understanding the Design System

shadcn-svelte uses a design system built on CSS variables and Tailwind CSS utilities. This approach provides:

- **Consistent theming** across all components
- **Easy customization** through CSS variables
- **Dark mode support** built into every component
- **Scalable design tokens** for enterprise applications
- **Utility-first approach** for rapid development

### CSS Variables Structure

The theming system is based on CSS custom properties (variables) defined in `src/app.css`:

```css
:root {
  /* Light theme colors */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  /* ... more variables */
}

.dark {
  /* Dark theme colors */
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... more variables */
}
```

These colors use **HSL (Hue, Saturation, Lightness)** values, which are converted by Tailwind CSS into actual colors.

## Theme Customization

### Basic Color Customization

Modify your `src/app.css` to change the color scheme:

```css
@layer base {
  :root {
    /* Custom blue theme */
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 10% 3.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
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

### Creating Custom Color Schemes

#### Purple Theme Example

```css
@layer base {
  :root {
    /* Purple theme */
    --primary: 262.1 83.3% 57.8%;
    --primary-foreground: 210 20% 98%;
    --secondary: 270 20% 96%;
    --secondary-foreground: 262.1 83.3% 14.1%;
    --accent: 270 20% 96%;
    --accent-foreground: 262.1 83.3% 14.1%;
  }

  .dark {
    --primary: 262.1 83.3% 57.8%;
    --primary-foreground: 210 20% 98%;
    --secondary: 262.1 83.3% 14.1%;
    --secondary-foreground: 210 20% 98%;
    --accent: 262.1 83.3% 14.1%;
    --accent-foreground: 210 20% 98%;
  }
}
```

#### Green Success Theme

```css
@layer base {
  :root {
    /* Green success theme */
    --primary: 142.1 76.2% 36.3%;
    --primary-foreground: 355.7 100% 97.3%;
    --secondary: 138 76% 97%;
    --secondary-foreground: 142.1 76.2% 13.1%;
    --muted: 138 76% 97%;
    --muted-foreground: 138 76% 46.1%;
    /* Custom success color */
    --success: 142.1 76.2% 36.3%;
    --success-foreground: 355.7 100% 97.3%;
  }

  .dark {
    --primary: 142.1 70.6% 45.3%;
    --primary-foreground: 144.9 80.4% 10%;
    --secondary: 142.1 76.2% 13.1%;
    --secondary-foreground: 144.9 80.4% 10%;
    --muted: 142.1 76.2% 13.1%;
    --muted-foreground: 144.9 80.4% 60%;
    --success: 142.1 70.6% 45.3%;
    --success-foreground: 144.9 80.4% 10%;
  }
}
```

### Adding Custom Colors to Tailwind

Update your `tailwind.config.js` to include custom color variables:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Custom colors
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning))",
          foreground: "hsl(var(--warning-foreground))",
        },
        info: {
          DEFAULT: "hsl(var(--info))",
          foreground: "hsl(var(--info-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
```

## Dark Mode Implementation

### Automatic Dark Mode

Create a theme switcher component for automatic dark mode:

```svelte
<!-- src/lib/components/ui/theme-switcher.svelte -->
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { MoonIcon, SunIcon } from 'lucide-svelte';
  import { onMount } from 'svelte';

  let theme: 'light' | 'dark' | 'system' = 'system';
  let systemTheme: 'light' | 'dark' = 'light';

  onMount(() => {
    // Load saved theme or default to system
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | 'system' || 'system';
    theme = savedTheme;
    applyTheme(savedTheme);

    // Watch system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    systemTheme = mediaQuery.matches ? 'dark' : 'light';

    const handleChange = (e: MediaQueryListEvent) => {
      systemTheme = e.matches ? 'dark' : 'light';
      if (theme === 'system') {
        applyTheme('system');
      }
    };

    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  });

  function applyTheme(selectedTheme: 'light' | 'dark' | 'system') {
    const root = document.documentElement;

    if (selectedTheme === 'system') {
      root.classList.remove('light', 'dark');
      root.classList.add(systemTheme);
    } else {
      root.classList.remove('light', 'dark', systemTheme);
      root.classList.add(selectedTheme);
    }
  }

  function toggleTheme() {
    const themes: Array<'light' | 'dark' | 'system'> = ['light', 'dark', 'system'];
    const currentIndex = themes.indexOf(theme);
    theme = themes[(currentIndex + 1) % themes.length];

    localStorage.setItem('theme', theme);
    applyTheme(theme);
  }
</script>

<Button variant="outline" size="icon" on:click={toggleTheme} title="Toggle theme">
  {#if theme === 'light'}
    <SunIcon class="h-4 w-4" />
  {:else if theme === 'dark'}
    <MoonIcon class="h-4 w-4" />
  {:else}
    <SunIcon class="h-4 w-4" />
  {/if}
</Button>
```

### Manual Dark Mode Classes

Apply dark mode classes manually in your components:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';

  let isDark = false;
</script>

<div class="{isDark ? 'dark' : ''}">
  <Card>
    <CardHeader>
      <CardTitle>Theme Example</CardTitle>
    </CardHeader>
    <CardContent>
      <p class="text-sm text-muted-foreground">
        This card adapts to the current theme.
      </p>
      <Button
        variant="outline"
        class="mt-4"
        on:click={() => isDark = !isDark}
      >
        Toggle Dark Mode
      </Button>
    </CardContent>
  </Card>
</div>
```

## Component Customization

### Customizing Button Variants

Extend button variants by modifying the component:

```svelte
<!-- src/lib/components/ui/button/Button.svelte -->
<script lang="ts">
  import { cva } from "class-variance-authority";
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";
  import type { ButtonVariants } from "./types";

  interface Props {
    variant?: ButtonVariants["variant"];
    size?: ButtonVariants["size"];
    class?: string;
    children: Snippet;
  }

  let {
    variant = "default",
    size = "default",
    class: className,
    children,
  }: Props = $props();

  const buttonVariants = cva(
    "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    {
      variants: {
        variant: {
          default: "bg-primary text-primary-foreground hover:bg-primary/90",
          destructive:
            "bg-destructive text-destructive-foreground hover:bg-destructive/90",
          outline:
            "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
          secondary:
            "bg-secondary text-secondary-foreground hover:bg-secondary/80",
          ghost: "hover:bg-accent hover:text-accent-foreground",
          link: "text-primary underline-offset-4 hover:underline",
          // Custom variants
          success: "bg-green-500 text-white hover:bg-green-600",
          warning: "bg-yellow-500 text-white hover:bg-yellow-600",
          info: "bg-blue-500 text-white hover:bg-blue-600",
          // Gradient variant
          gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600",
        },
        size: {
          default: "h-10 px-4 py-2",
          sm: "h-9 rounded-md px-3",
          lg: "h-11 rounded-md px-8",
          icon: "h-10 w-10",
          // Custom sizes
          xs: "h-7 rounded px-2 text-xs",
          xl: "h-12 rounded-lg px-10 text-base",
        },
      },
      defaultVariants: {
        variant: "default",
        size: "default",
      },
    }
  );
</script>

<button
  class={cn(buttonVariants({ variant, size, className }))}
  on:click
  on:keydown
>
  {@render children()}
</button>
```

Update the types file:

```typescript
<!-- src/lib/components/ui/button/types.ts -->
export interface ButtonVariants {
  variant: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link" | "success" | "warning" | "info" | "gradient";
  size: "default" | "sm" | "lg" | "icon" | "xs" | "xl";
}
```

### Creating Custom Card Variants

```svelte
<!-- src/lib/components/ui/card/Card.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  interface Props {
    class?: string;
    variant?: "default" | "outlined" | "elevated" | "glass";
    children: Snippet;
  }

  let {
    class: className,
    variant = "default",
    children,
  }: Props = $props();

  const cardVariants = {
    default: "rounded-lg border bg-card text-card-foreground shadow-sm",
    outlined: "rounded-lg border-2 bg-card text-card-foreground",
    elevated: "rounded-lg border bg-card text-card-foreground shadow-lg",
    glass: "rounded-lg border bg-white/80 text-card-foreground backdrop-blur-sm dark:bg-gray-900/80"
  };
</script>

<div class={cn(cardVariants[variant], className)}>
  {@render children()}
</div>
```

### Custom Input Styles

```svelte
<!-- src/lib/components/ui/input/Input.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";

  interface Props {
    class?: string;
    type?: string;
    placeholder?: string;
    value?: string;
    variant?: "default" | "filled" | "underlined";
    error?: boolean;
  }

  let {
    class: className,
    type = "text",
    placeholder,
    value = $bindable(''),
    variant = "default",
    error = false,
    ...restProps
  }: Props = $props();

  const inputVariants = {
    default: "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
    filled: "flex h-10 w-full rounded-md bg-muted px-3 py-2 text-sm file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
    underlined: "flex h-10 w-full border-b-2 border-input bg-transparent px-1 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
  };

  const errorClasses = error ? "border-red-500 focus-visible:ring-red-500" : "";
</script>

<input
  {type}
  {placeholder}
  bind:value
  class={cn(inputVariants[variant], errorClasses, className)}
  {...restProps}
/>
```

## Design Tokens and System

### Creating Design Tokens

Define a design token system for consistent spacing, typography, and colors:

```css
/* src/app.css */
@layer base {
  :root {
    /* Spacing tokens */
    --spacing-xs: 0.25rem;    /* 4px */
    --spacing-sm: 0.5rem;     /* 8px */
    --spacing-md: 1rem;       /* 16px */
    --spacing-lg: 1.5rem;     /* 24px */
    --spacing-xl: 2rem;       /* 32px */
    --spacing-2xl: 3rem;      /* 48px */
    --spacing-3xl: 4rem;      /* 64px */

    /* Typography tokens */
    --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;

    /* Font size tokens */
    --text-xs: 0.75rem;       /* 12px */
    --text-sm: 0.875rem;      /* 14px */
    --text-base: 1rem;        /* 16px */
    --text-lg: 1.125rem;      /* 18px */
    --text-xl: 1.25rem;       /* 20px */
    --text-2xl: 1.5rem;       /* 24px */
    --text-3xl: 1.875rem;     /* 30px */
    --text-4xl: 2.25rem;      /* 36px */

    /* Line height tokens */
    --leading-tight: 1.25;
    --leading-normal: 1.5;
    --leading-relaxed: 1.75;

    /* Border radius tokens */
    --radius-none: 0;
    --radius-sm: 0.125rem;    /* 2px */
    --radius-base: 0.25rem;   /* 4px */
    --radius-md: 0.375rem;    /* 6px */
    --radius-lg: 0.5rem;      /* 8px */
    --radius-xl: 0.75rem;     /* 12px */
    --radius-2xl: 1rem;       /* 16px */
    --radius-full: 9999px;

    /* Shadow tokens */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  }

  .dark {
    /* Dark mode shadow adjustments */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.25);
    --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.3);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.3), 0 8px 10px -6px rgb(0 0 0 / 0.3);
  }
}
```

### Update Tailwind Config with Tokens

```javascript
/** tailwind.config.js */
export default {
  // ... existing config
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)", ...theme.fontFamily.sans],
        mono: ["var(--font-mono)", ...theme.fontFamily.mono],
      },
      fontSize: {
        xs: ["var(--text-xs)", { lineHeight: "var(--leading-tight)" }],
        sm: ["var(--text-sm)", { lineHeight: "var(--leading-normal)" }],
        base: ["var(--text-base)", { lineHeight: "var(--leading-normal)" }],
        lg: ["var(--text-lg)", { lineHeight: "var(--leading-normal)" }],
        xl: ["var(--text-xl)", { lineHeight: "var(--leading-relaxed)" }],
        "2xl": ["var(--text-2xl)", { lineHeight: "var(--leading-relaxed)" }],
        "3xl": ["var(--text-3xl)", { lineHeight: "var(--leading-tight)" }],
        "4xl": ["var(--text-4xl)", { lineHeight: "var(--leading-tight)" }],
      },
      spacing: {
        xs: "var(--spacing-xs)",
        sm: "var(--spacing-sm)",
        md: "var(--spacing-md)",
        lg: "var(--spacing-lg)",
        xl: "var(--spacing-xl)",
        "2xl": "var(--spacing-2xl)",
        "3xl": "var(--spacing-3xl)",
      },
      borderRadius: {
        none: "var(--radius-none)",
        xs: "var(--radius-sm)",
        base: "var(--radius-base)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
        "2xl": "var(--radius-2xl)",
        full: "var(--radius-full)",
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        base: "var(--shadow-base)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
        xl: "var(--shadow-xl)",
      },
    },
  },
  plugins: [],
};
```

## Custom Component Creation

### Building a Custom Badge Component

```svelte
<!-- src/lib/components/ui/badge/Badge.svelte -->
<script lang="ts">
  import { cva } from "class-variance-authority";
  import { cn } from "$lib/utils";

  interface Props {
    variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning" | "info";
    size?: "sm" | "default" | "lg";
    class?: string;
    children: string;
  }

  let {
    variant = "default",
    size = "default",
    class: className,
    children,
  }: Props = $props();

  const badgeVariants = cva(
    "inline-flex items-center rounded-full font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
    {
      variants: {
        variant: {
          default:
            "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
          secondary:
            "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
          destructive:
            "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
          outline: "text-foreground border",
          success: "border-transparent bg-green-500 text-white hover:bg-green-600",
          warning: "border-transparent bg-yellow-500 text-white hover:bg-yellow-600",
          info: "border-transparent bg-blue-500 text-white hover:bg-blue-600",
        },
        size: {
          sm: "px-2 py-0.5 text-xs",
          default: "px-2.5 py-0.5 text-xs",
          lg: "px-3 py-1 text-sm",
        },
      },
      defaultVariants: {
        variant: "default",
        size: "default",
      },
    }
  );
</script>

<div class={cn(badgeVariants({ variant, size }), className)}>
  {children}
</div>
```

### Building a Custom Skeleton Component

```svelte
<!-- src/lib/components/ui/skeleton/Skeleton.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";

  interface Props {
    class?: string;
    width?: string;
    height?: string;
    circle?: boolean;
  }

  let {
    class: className,
    width,
    height,
    circle = false,
    ...restProps
  }: Props = $props();
</script>

<div
  class={cn(
    "animate-pulse rounded-md bg-muted",
    circle && "rounded-full",
    className
  )}
  style:width={width}
  style:height={height}
  {...restProps}
/>
```

## Animation Customization

### Custom Animations

Add custom animations to your CSS:

```css
/* src/app.css */
@layer utilities {
  /* Custom animations */
  .animate-fade-in {
    animation: fadeIn 0.3s ease-in-out;
  }

  .animate-slide-up {
    animation: slideUp 0.3s ease-out;
  }

  .animate-scale-in {
    animation: scaleIn 0.2s ease-out;
  }

  .animate-bounce-in {
    animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }

  /* Animation keyframes */
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideUp {
    from {
      transform: translateY(10px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes scaleIn {
    from {
      transform: scale(0.95);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  @keyframes bounceIn {
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
}
```

### Transition Variants

Create custom transition variants for components:

```svelte
<!-- src/lib/components/ui/transition/Transition.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";

  interface Props {
    show: boolean;
    enter?: string;
    enterFrom?: string;
    enterTo?: string;
    leave?: string;
    leaveFrom?: string;
    leaveTo?: string;
    duration?: number;
    children: any;
  }

  let {
    show,
    enter = "transition-all duration-300 ease-out",
    enterFrom = "opacity-0 transform translate-y-2",
    enterTo = "opacity-100 transform translate-y-0",
    leave = "transition-all duration-200 ease-in",
    leaveFrom = "opacity-100 transform translate-y-0",
    leaveTo = "opacity-0 transform -translate-y-2",
    duration = 300,
    children,
  }: Props = $props();

  let element: HTMLElement;
  let isShowing = show;
</script>

{#if show}
  <div
    bind:this={element}
    class={cn(
      enter,
      isShowing ? enterTo : enterFrom
    )}
    style="transition-duration: {duration}ms"
  >
    {@render children()}
  </div>
{/if}

{#if element && !show && isShowing}
  <div
    class={cn(leave, leaveFrom)}
    style="transition-duration: {duration}ms"
    on:transitionend={() => isShowing = false}
  >
    {@render children()}
  </div>
{/if}
```

## Responsive Customization

### Component Breakpoints

Create responsive variants for different screen sizes:

```svelte
<!-- src/lib/components/ui/responsive-card/ResponsiveCard.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  interface Props {
    class?: string;
    children: Snippet;
    variant?: "default" | "mobile-first" | "desktop-first";
  }

  let {
    class: className,
    children,
    variant = "default",
  }: Props = $props();

  const responsiveVariants = {
    default: "w-full max-w-md mx-auto sm:max-w-lg md:max-w-2xl lg:max-w-4xl",
    "mobile-first": "w-full sm:w-auto sm:min-w-96 md:w-full lg:w-3/4",
    "desktop-first": "w-full lg:w-3/4 xl:w-2/3"
  };
</script>

<div class={cn(responsiveVariants[variant], className)}>
  {@render children()}
</div>
```

### Responsive Typography

```css
/* Responsive typography tokens */
@layer base {
  :root {
    --fluid-text-sm: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
    --fluid-text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
    --fluid-text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.5rem);
    --fluid-text-xl: clamp(1.25rem, 1rem + 1.25vw, 2rem);
    --fluid-text-2xl: clamp(1.5rem, 1.1rem + 2vw, 3rem);
    --fluid-text-3xl: clamp(1.875rem, 1.2rem + 3.375vw, 4.5rem);
  }
}
```

## Performance Optimization

### CSS Purging with Custom Components

Ensure your custom components are properly purged in production:

```javascript
/** tailwind.config.js */
export default {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    "./src/lib/components/ui/**/*.{svelte,ts}"
  ],
  // ... rest of config
}
```

### Tree Shaking Custom Components

Use proper exports for tree shaking:

```typescript
// src/lib/components/ui/index.ts
// Export all components for tree shaking
export { Button } from './button';
export { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './card';
export { Input } from './input';
export { Badge } from './badge';
export { Skeleton } from './skeleton';

// Export types
export type { ButtonVariants } from './button/types';
```

### CSS Bundle Size Optimization

Create a separate CSS file for custom styles:

```css
/* src/lib/styles/components.css */
/* Only custom component styles */
@layer components {
  .custom-component {
    /* Custom styles */
  }
}

/* Import in your main CSS */
@import './components.css';
```

## Testing Custom Components

### Unit Testing Example

```svelte
<!-- Button.test.svelte -->
<script lang="ts">
  import { render, fireEvent } from '@testing-library/svelte';
  import { Button } from '$lib/components/ui/button';

  test('Custom button variant renders correctly', () => {
    const { getByRole } = render(Button, {
      props: {
        variant: 'success',
        children: 'Success Button'
      }
    });

    const button = getByRole('button');
    expect(button).toHaveClass('bg-green-500', 'text-white');
  });

  test('Custom size variant renders correctly', () => {
    const { getByRole } = render(Button, {
      props: {
        size: 'xs',
        children: 'Small Button'
      }
    });

    const button = getByRole('button');
    expect(button).toHaveClass('h-7', 'rounded', 'px-2', 'text-xs');
  });
</script>
```

### Visual Regression Testing

Use tools like Storybook or Chromatic for visual testing:

```svelte
<!-- Button.stories.svelte -->
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<Story name="Primary">
  <Button>Primary Button</Button>
</Story>

<Story name="Success">
  <Button variant="success">Success Button</Button>
</Story>

<Story name="Custom Size">
  <Button size="xs">Extra Small</Button>
</Story>
```

## Best Practices for Customization

### 1. **Use CSS Variables for Theming**
- Leverage HSL values for better color manipulation
- Create semantic color names for your brand
- Test both light and dark modes

### 2. **Follow the Component Pattern**
- Use `class-variance-authority` for variant management
- Implement proper TypeScript types
- Follow the established naming conventions

### 3. **Maintain Consistency**
- Use design tokens for spacing, typography, and colors
- Document your custom components
- Create component usage guidelines

### 4. **Performance Considerations**
- Minimize custom CSS in favor of Tailwind utilities
- Use tree shaking for component imports
- Test bundle size impact

### 5. **Accessibility**
- Maintain proper contrast ratios in custom themes
- Test keyboard navigation with custom components
- Ensure ARIA labels are properly implemented

## Next Steps

Now that you understand customization:

1. **Explore patterns**: Check our [examples and patterns guide](./shadcn-svelte-examples.md)
2. **Learn best practices**: Review our [best practices guide](./shadcn-svelte-best-practices.md)
3. **Build integrations**: See our [SvelteKit integration guide](./shadcn-svelte-integration.md)
4. **Advanced patterns**: Study our [component composition guide](./shadcn-svelte-composition.md)

---

*For more customization examples and advanced patterns, visit the [official shadcn-svelte documentation](https://www.shadcn-svelte.com/docs/theming).*