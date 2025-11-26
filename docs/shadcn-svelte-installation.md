# Installation & Setup Guide

This comprehensive guide walks you through setting up shadcn-svelte with Tailwind CSS in your Svelte projects. We'll cover everything from creating a new project to configuring all necessary dependencies.

## Prerequisites

Before you begin, ensure you have:

- **Node.js** 18.0 or higher
- **npm**, **yarn**, or **pnpm** package manager
- Basic familiarity with **Svelte** and **SvelteKit**
- Optional: **VS Code** with recommended extensions for better development experience

## Quick Installation

If you want to get started quickly, run this command in your terminal:

```bash
npx sv create my-app --template minimal
cd my-app
npm install
npx shadcn-svelte@latest init
```

For detailed setup instructions, continue reading below.

## Step-by-Step Installation

### 1. Create a New SvelteKit Project

#### Option A: Using `sv` (Recommended)

```bash
# Create a new SvelteKit project with minimal template
npx sv create my-app --template minimal

# Navigate to your project directory
cd my-app

# Install dependencies
npm install
```

#### Option B: Using SvelteKit CLI

```bash
# Create a new SvelteKit project
npm create svelte@latest my-app

# Follow the prompts:
# ✔ Which Svelte app template? › Skeleton project
# ✔ Add type checking with TypeScript? › Yes
# ✔ Add ESLint for code linting? › Yes
# ✔ Add Prettier for code formatting? › Yes

cd my-app
npm install
```

### 2. Install and Configure Tailwind CSS

shadcn-svelte requires Tailwind CSS for styling. Here's how to set it up:

```bash
# Install Tailwind CSS and its dependencies
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind CSS configuration
npx tailwindcss init -p
```

#### Configure Tailwind CSS

Create or update your `tailwind.config.js`:

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

#### Create CSS Variables File

Create `src/app.css` with the necessary CSS variables:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
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

#### Import CSS in Your App

In your `src/routes/+layout.svelte`, import the CSS:

```svelte
<script lang="ts">
  import '../app.css';
</script>

<slot />
```

### 3. Install shadcn-svelte CLI

```bash
# Install the CLI globally
npm install -g shadcn-svelte

# Or use npx to run it without installation
npx shadcn-svelte@latest init
```

### 4. Initialize shadcn-svelte

Run the initialization command:

```bash
npx shadcn-svelte@latest init
```

You'll be prompted with several questions:

```
✔ Would you like to use TypeScript? … Yes
✔ Which style would you like to use? › Default
✔ Which color would you like to use as base color? › Slate
✔ Would you like to use CSS variables for colors? … Yes
```

#### What the init command does:

1. **Creates component structure**: Sets up `src/lib/components/ui/` directory
2. **Installs dependencies**: Adds necessary packages like `class-variance-authority`, `clsx`, `tailwind-merge`, and `lucide-svelte`
3. **Creates utility files**: Sets up `src/lib/utils.ts` for className merging
4. **Configures SvelteKit**: Updates `app.html` with necessary scripts and meta tags

### 5. Verify Installation

Your project structure should now include:

```
src/
├── lib/
│   ├── components/
│   │   └── ui/
│   │       └── index.ts      # Component exports
│   └── utils.ts              # Utility functions
├── app.css                   # CSS variables and base styles
└── routes/
    └── +layout.svelte        # Main layout
```

Key files that should exist:
- `src/lib/utils.ts` - Contains `cn()` utility function
- `src/app.css` - Contains CSS variables for theming
- `tailwind.config.js` - Tailwind configuration with custom theme
- `vite.config.ts` - May have been updated with necessary aliases

### 6. Install Your First Component

Let's install a Button component to test everything works:

```bash
npx shadcn-svelte@latest add button
```

This will:
- Create `src/lib/components/ui/button/` directory
- Add `Button.svelte`, `index.ts`, and `types.ts` files
- Install any additional dependencies if needed

#### Test the Button Component

Create a simple test in `src/routes/+page.svelte`:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<div class="container mx-auto p-8">
  <h1 class="text-3xl font-bold mb-6">shadcn-svelte Test</h1>

  <div class="flex gap-4 flex-wrap">
    <Button>Default Button</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="destructive">Destructive</Button>
    <Button variant="outline">Outline</Button>
    <Button variant="ghost">Ghost</Button>
  </div>
</div>
```

Run your development server:

```bash
npm run dev
```

Navigate to `http://localhost:5173` and you should see the buttons rendered with proper styling.

## Manual Installation (Alternative)

If you prefer manual setup without the CLI, here's what you need to do:

### 1. Install Dependencies

```bash
# Core dependencies
npm install class-variance-authority clsx tailwind-merge lucide-svelte

# Icons (if needed)
npm install @radix-ui/react-icons
```

### 2. Create Utility Function

Create `src/lib/utils.ts`:

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 3. Create Component Structure

```bash
mkdir -p src/lib/components/ui/button
```

### 4. Create Button Component

Create `src/lib/components/ui/button/Button.svelte`:

```svelte
<script lang="ts">
  import { cn } from "$lib/utils";
  import { type Snippet } from "svelte";
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

  const buttonVariants = tv({
    base: "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
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
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  });
</script>

<button
  class={cn(buttonVariants({ variant, size, className }))}
  on:click
  on:keydown
>
  {@render children()}
</button>
```

### 5. Create Type Definitions

Create `src/lib/components/ui/button/types.ts`:

```typescript
export interface ButtonVariants {
  variant: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size: "default" | "sm" | "lg" | "icon";
}
```

### 6. Create Index Export

Create `src/lib/components/ui/button/index.ts`:

```typescript
import Button from "./Button.svelte";
import type { ButtonVariants } from "./types";

export { Button };
export type { ButtonVariants };
```

## Common Installation Issues

### Issue: CSS Variables Not Working

**Problem**: Components don't have the correct colors or styling.

**Solution**:
1. Ensure `src/app.css` is imported in your root layout
2. Check that CSS variables are properly defined
3. Verify Tailwind CSS is processing your CSS

### Issue: Component Imports Not Found

**Problem**: TypeScript cannot find component imports.

**Solution**:
1. Check that `tsconfig.json` has the correct paths:
```json
{
  "compilerOptions": {
    "paths": {
      "$lib": ["./src/lib"],
      "$lib/*": ["./src/lib/*"]
    }
  }
}
```

### Issue: Tailwind Classes Not Applying

**Problem**: Tailwind classes aren't being applied to components.

**Solution**:
1. Verify `tailwind.config.js` content array includes your component paths
2. Check that PostCSS configuration is correct
3. Ensure CSS import is working in your layout

### Issue: Build Errors

**Problem**: Production build fails with component-related errors.

**Solution**:
1. Check that all dependencies are properly installed
2. Verify TypeScript configuration
3. Ensure all component files have correct exports

## Next Steps

Now that you have shadcn-svelte installed and configured:

1. **Explore Components**: Browse the [available components](https://www.shadcn-svelte.com/docs/components)
2. **Add More Components**: Use `npx shadcn-svelte@latest add [component-name]`
3. **Customize Theme**: Modify CSS variables in `app.css`
4. **Learn Patterns**: Check our [best practices guide](./shadcn-svelte-best-practices.md)

## IDE Extensions

### VS Code

Install these extensions for better development experience:

```bash
code --install-extension svelte.svelte-vscode
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
```

### JetBrains IDEs

- Svelte plugin
- Tailwind CSS plugin
- Official shadcn-svelte plugin (if available)

---

*Having trouble with installation? Check the [troubleshooting guide](https://www.shadcn-svelte.com/docs/troubleshooting) or open an issue on the [GitHub repository](https://github.com/huntabyte/shadcn-svelte/issues).*