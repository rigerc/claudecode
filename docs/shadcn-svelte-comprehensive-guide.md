# shadcn-svelte: Complete Developer Guide

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation & Setup](#installation--setup)
- [Component Library](#component-library)
- [Architecture](#architecture)
- [Advanced Usage](#advanced-usage)
- [Customization](#customization)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Community & Resources](#community--resources)

## Overview

**shadcn-svelte** is the official Svelte port of the popular [shadcn/ui](https://ui.shadcn.com/) component library. It provides beautifully designed, accessible UI components built with Tailwind CSS and designed specifically for the Svelte ecosystem.

### Key Characteristics

- **Component Library, Not Framework**: Copy components as source code into your project
- **Built on Bits UI**: Underlying accessibility primitives powered by Radix UI
- **Tailwind CSS Integration**: Utility-first styling with consistent design system
- **TypeScript First**: Complete type safety and IntelliSense support
- **SvelteKit Optimized**: Seamlessly works with SvelteKit conventions
- **Accessibility Compliant**: WCAG 2.1 AA standards with proper ARIA support

### What Makes shadcn-svelte Special?

#### 🎨 Design Excellence
- Modern, clean design system following accessibility best practices
- Consistent spacing, typography, and color schemes
- Built-in dark mode support for all components
- Smooth animations and transitions

#### ♿ Accessibility First
- All components meet WCAG 2.1 AA standards
- Proper ARIA attributes and keyboard navigation
- Screen reader support and focus management
- Modal focus trapping and proper escape handling

#### 🛠 Developer Experience
- CLI tool for easy component installation (`shadcn-svelte@latest add <component>`)
- Full TypeScript support with comprehensive type definitions
- Excellent documentation with live examples
- VS Code and JetBrains extensions for enhanced development

#### 🔧 Complete Control
- Copy components directly into your project for full ownership
- Customize any aspect without breaking updates
- No runtime dependencies beyond what you explicitly choose
- Tree-shakable and production-optimized builds

## Quick Start

### Prerequisites

- Node.js 18+
- A Svelte or SvelteKit project
- Tailwind CSS configured (recommended)

### 5-Minute Setup

1. **Initialize shadcn-svelte**:
```bash
npx shadcn-svelte@latest init
```

2. **Install your first component**:
```bash
npx shadcn-svelte@latest add button
```

3. **Use the component**:
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<Button>Click me</Button>
```

### Essential Commands

```bash
# Initialize shadcn-svelte in your project
npx shadcn-svelte@latest init

# Add components
npx shadcn-svelte@latest add button card input

# List available components
npx shadcn-svelte@latest add --help

# Update components
npx shadcn-svelte@latest add button --overwrite
```

## Installation & Setup

### Project Setup

#### 1. New SvelteKit Project (Recommended)

```bash
# Create new SvelteKit project
npm create svelte@latest my-app
cd my-app

# Install shadcn-svelte
npx shadcn-svelte@latest init
```

#### 2. Existing Svelte/SvelteKit Project

```bash
# Navigate to your project
cd your-svelte-app

# Initialize shadcn-svelte
npx shadcn-svelte@latest init
```

### Manual Installation

If you prefer manual setup instead of the CLI:

1. **Install dependencies**:
```bash
npm install tailwind-variants clsx tailwind-merge tw-animate-css @lucide/svelte bits-ui
```

2. **Configure Tailwind CSS**:
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
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))"
        },
        // ... more color definitions
      }
    }
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;

export default config;
```

3. **Create CSS variables**:
```css
/* src/app.css or similar */
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
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 47.4% 11.2%;
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

4. **Create utils file**:
```typescript
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Framework-Specific Setup

#### Astro Integration

```bash
# Install shadcn-svelte
npx shadcn-svelte@latest init

# Add components
npx shadcn-svelte@latest add button
```

Use client directives for interactive components:

```astro
---
import { Button } from "$lib/components/ui/button";
---
<Button client:load>Click me</Button>
```

## Component Library

### Available Components

shadcn-svelte includes 40+ components covering all common UI patterns:

#### Form Controls
- **Button** - Versatile button with variants and sizes
- **Input** - Text input with validation states
- **Select** - Dropdown select component
- **Checkbox** - Multi-select checkbox
- **Radio Group** - Single selection radio buttons
- **Switch** - Toggle switch component
- **Textarea** - Multi-line text input
- **Label** - Form label with accessibility

#### Navigation
- **Tabs** - Tabbed content switching
- **Breadcrumb** - Navigation breadcrumb trail
- **Pagination** - Page navigation controls
- **Navigation Menu** - Complex navigation with dropdowns
- **Menubar** - Application menu bar

#### Feedback & Overlays
- **Alert** - Informational alerts
- **Toast** - Notification messages
- **Dialog** - Modal dialogs
- **Sheet** - Slide-out panels
- **Drawer** - Bottom drawer component
- **AlertDialog** - Confirmation dialogs
- **Hover Card** - Contextual hover information

#### Data Display
- **Card** - Content cards with headers and actions
- **Table** - Data tables with sorting and filtering
- **Accordion** - Collapsible content sections
- **Collapsible** - Single collapsible section
- **Skeleton** - Loading placeholders
- **Progress** - Progress indicators
- **Badge** - Status badges and labels

#### Layout
- **Separator** - Visual dividers
- **ScrollArea** - Custom scrollable areas
- **AspectRatio** - Fixed aspect ratio containers
- **Sheet** - Side panels

#### Media
- **Avatar** - User avatars with fallbacks
- **Image** - Optimized image component
- **Carousel** - Image/content carousels

### Component Structure

Each component follows a consistent structure:

```
src/lib/components/ui/
├── button/
│   ├── Button.svelte          # Main component implementation
│   ├── index.ts              # Barrel exports
│   └── types.ts              # TypeScript definitions
├── card/
│   ├── Card.svelte
│   ├── index.ts
│   └── types.ts
└── ...
```

### Basic Usage Examples

#### Button Component

```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<!-- Different variants -->
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

<!-- Different sizes -->
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>

<!-- With icons -->
<Button>
  <PlusIcon class="w-4 h-4 mr-2" />
  Add Item
</Button>
```

#### Card Component

```svelte
<script lang="ts">
  import { Card } from "$lib/components/ui/card";
</script>

<Card>
  <Card.Header>
    <Card.Title>Card Title</Card.Title>
    <Card.Description>Card description goes here</Card.Description>
  </Card.Header>
  <Card.Content>
    <p>Card content area</p>
  </Card.Content>
  <Card.Footer>
    <Button>Card Action</Button>
  </Card.Footer>
</Card>
```

#### Form with Input and Button

```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";

  let email = "";
</script>

<form class="space-y-4">
  <div>
    <Label for="email">Email</Label>
    <Input
      id="email"
      type="email"
      placeholder="Enter your email"
      bind:value={email}
    />
  </div>
  <Button type="submit">Submit</Button>
</form>
```

#### Alert Component

```svelte
<script lang="ts">
  import { Alert } from "$lib/components/ui/alert";
  import { AlertCircle } from "@lucide/svelte";
</script>

<Alert>
  <AlertCircle class="h-4 w-4" />
  <Alert.Title>Heads up!</Alert.Title>
  <Alert.Description>
    You can add components to your app using the CLI.
  </Alert.Description>
</Alert>
```

## Architecture

### Component Design Philosophy

#### 1. Copy-Paste Architecture
Unlike traditional component libraries, shadcn-svelte uses a "copy-paste" approach:

- **Full Ownership**: Components live in your codebase
- **Complete Customization**: Modify any aspect without restrictions
- **No Lock-in**: Never tied to library updates or breaking changes
- **Bundle Control**: Only ship what you actually use

#### 2. Headless Primitives
Components are built on top of [Bits UI](https://bits-ui.com/):

- **Accessibility First**: Built-in ARIA support and keyboard navigation
- **Behavior Separation**: Logic separated from styling
- **Cross-Platform Consistency**: Works across browsers and devices
- **Extensible**: Easy to extend with custom functionality

#### 3. Tailwind CSS Integration
Styling is handled through Tailwind CSS:

- **Utility-First**: Consistent styling patterns
- **Design System**: Shared colors, spacing, and typography
- **Theme Support**: Built-in light/dark mode
- **Responsive**: Mobile-first responsive design

### Component API Design

#### Consistent Props Pattern
```typescript
// Most components follow this pattern
interface ComponentProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  class?: string; // Custom CSS classes
  children?: Snippet; // Svelte 5 snippet
}
```

#### Accessibility Props
```typescript
// Accessibility is built-in
interface AccessibleProps {
  disabled?: boolean;
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-expanded'?: boolean;
}
```

#### Event Handling
```typescript
// Consistent event handling
interface InteractiveProps {
  onclick?: (event: MouseEvent) => void;
  onkeydown?: (event: KeyboardEvent) => void;
  onsubmit?: (event: SubmitEvent) => void;
}
```

### State Management

#### Using Svelte 5 Features
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Dialog from "$lib/components/ui/dialog";

  let open = $state(false);

  function handleOpen() {
    open = true;
  }

  function handleClose() {
    open = false;
  }
</script>

<Dialog.Root bind:open={open}>
  <Dialog.Trigger>
    <Button onclick={handleOpen}>Open Dialog</Button>
  </Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Title>Dialog Title</Dialog.Title>
    <Dialog.Description>
      This is a dialog description.
    </Dialog.Description>
    <Dialog.Close>
      <Button variant="outline">Close</Button>
    </Dialog.Close>
  </Dialog.Content>
</Dialog.Root>
```

## Advanced Usage

### Form Integration with Superforms

shadcn-svelte integrates seamlessly with [Superforms](https://superforms.rocks) and [Formsnap](https://formsnap.dev):

```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import * as Form from "$lib/components/ui/form";

  const schema = z.object({
    email: z.string().email(),
    password: z.string().min(8)
  });

  const { form, enhance } = superForm(zodClient(schema), {
    onResult: ({ result }) => {
      // Handle form submission
    }
  });
</script>

<form method="POST" use:enhance>
  <Form.Field {form} name="email">
    <Form.Label>Email</Form.Label>
    <Form.Control>
      <Input type="email" placeholder="Enter your email" />
    </Form.Control>
    <Form.Description>
      We'll never share your email with anyone else.
    </Form.Description>
    <Form.ErrorMessage />
  </Form.Field>

  <Form.Field {form} name="password">
    <Form.Label>Password</Form.Label>
    <Form.Control>
      <Input type="password" placeholder="Enter your password" />
    </Form.Control>
    <Form.ErrorMessage />
  </Form.Field>

  <Button type="submit">Submit</Button>
</form>
```

### Data Table Component

Advanced data table with sorting, filtering, and pagination:

```svelte
<script lang="ts">
  import { DataTable } from "$lib/components/ui/data-table";
  import { Button } from "$lib/components/ui/button";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";

  // Column definitions
  const columns = [
    {
      accessorKey: "name",
      header: "Name",
      cell: ({ row }) => {
        const name = row.getValue("name");
        return `<div class="font-medium">${name}</div>`;
      }
    },
    {
      accessorKey: "email",
      header: "Email",
      cell: ({ row }) => row.getValue("email")
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status");
        return `<Badge variant="secondary">${status}</Badge>`;
      }
    },
    {
      id: "actions",
      enableHiding: false,
      cell: ({ row }) => {
        return `
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <Button variant="ghost" class="h-8 w-8 p-0">
                <MoreHorizontal class="h-4 w-4" />
              </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content>
              <DropdownMenu.Item>Copy email</DropdownMenu.Item>
              <DropdownMenu.Separator />
              <DropdownMenu.Item>Delete user</DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        `;
      }
    }
  ];

  // Sample data
  const data = [
    { id: 1, name: "John Doe", email: "john@example.com", status: "Active" },
    { id: 2, name: "Jane Smith", email: "jane@example.com", status: "Inactive" },
    // ... more data
  ];
</script>

<DataTable columns={columns} data={data} />
```

### Chart Component Integration

shadcn-svelte works with charting libraries like Recharts:

```svelte
<script lang="ts">
  import { ChartContainer } from "$lib/components/ui/chart";
  import { Bar, BarChart, XAxis, YAxis } from "recharts";

  const data = [
    { name: "Jan", revenue: 4000, profit: 2400 },
    { name: "Feb", revenue: 3000, profit: 1398 },
    { name: "Mar", revenue: 2000, profit: 9800 },
    // ... more data
  ];

  const chartConfig = {
    revenue: {
      label: "Revenue",
      color: "hsl(var(--chart-1))"
    },
    profit: {
      label: "Profit",
      color: "hsl(var(--chart-2))"
    }
  };
</script>

<ChartContainer config={chartConfig} class="h-[400px] w-full">
  <BarChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Bar dataKey="revenue" fill="var(--color-revenue)" />
    <Bar dataKey="profit" fill="var(--color-profit)" />
  </BarChart>
</ChartContainer>
```

### Custom Component Creation

Create your own components following shadcn-svelte patterns:

```svelte
<!-- src/lib/components/ui/custom-card.svelte -->
<script lang="ts">
  import { cn } from "$lib/utils";
  import type { HTMLAttributes } from "svelte/elements";

  interface Props extends HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "elevated" | "outlined";
  }

  let {
    variant = "default",
    class: className,
    children,
    ...restProps
  }: Props = $props();

  const variants = {
    default: "bg-card text-card-foreground rounded-lg shadow-sm border",
    elevated: "bg-card text-card-foreground rounded-lg shadow-lg border-0",
    outlined: "bg-transparent text-foreground rounded-lg border-2"
  };
</script>

<div
  class={cn(variants[variant], className)}
  {...restProps}
>
  {@render children()}
</div>
```

## Customization

### Theme Customization

#### Custom Colors
```css
/* Extend the color system in your CSS */
:root {
  /* Custom brand colors */
  --brand: 142 76% 36%;
  --brand-foreground: 355 100% 97%;

  /* Additional semantic colors */
  --info: 199 89% 48%;
  --info-foreground: 210 40% 98%;
  --warning: 38 92% 50%;
  --warning-foreground: 48 96% 89%;
}

.dark {
  --brand: 142 70% 45%;
  --brand-foreground: 144 61% 20%;
  --info: 199 89% 68%;
  --warning: 48 96% 89%;
}
```

#### Custom Spacing & Sizing
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
      },
    },
  },
}
```

### Component Styling

#### Variant Customization
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { cn } from "$lib/utils";
</script>

<!-- Custom button with additional styles -->
<Button
  class={cn(
    "bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0",
    "hover:from-purple-600 hover:to-pink-600 transition-all duration-200"
  )}
>
  Custom Gradient Button
</Button>
```

#### Component Composition
```svelte
<script lang="ts">
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
</script>

<Card class="overflow-hidden">
  <div class="h-24 bg-gradient-to-r from-blue-500 to-purple-500"></div>
  <Card.Content class="pt-0">
    <div class="flex flex-col items-center -mt-12">
      <Avatar class="h-24 w-24 border-4 border-background">
        <AvatarImage src="/avatar.jpg" />
        <AvatarFallback>JD</AvatarFallback>
      </Avatar>
      <Card.Title class="mt-4 text-xl">John Doe</Card.Title>
      <Card.Description className="text-center">
        Software Developer at TechCorp
      </Card.Description>
      <div class="flex gap-2 mt-4">
        <Badge variant="secondary">React</Badge>
        <Badge variant="secondary">TypeScript</Badge>
        <Badge variant="secondary">Node.js</Badge>
      </div>
      <div class="flex gap-2 mt-6 w-full">
        <Button variant="outline" class="flex-1">Message</Button>
        <Button class="flex-1">Follow</Button>
      </div>
    </div>
  </Card.Content>
</Card>
```

### Creating Component Variants

#### Using Tailwind Variants
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
        // Custom variant
        gradient: "bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
        // Custom size
        xl: "h-12 rounded-lg px-10 text-base",
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

### Dark Mode Implementation

#### Theme Provider
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

#### Theme Toggle
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
>
  {#if isDark}
    <Sun class="h-4 w-4" />
  {:else}
    <Moon class="h-4 w-4" />
  {/if}
</Button>
```

## Best Practices

### Development Patterns

#### 1. Component Organization
```
src/lib/components/
├── ui/                    # shadcn-svelte components
│   ├── button/
│   ├── card/
│   └── ...
├── forms/                  # Form-specific components
│   ├── user-form.svelte
│   └── search-form.svelte
├── layout/                 # Layout components
│   ├── header.svelte
│   ├── sidebar.svelte
│   └── footer.svelte
└── features/               # Feature components
    ├── user-profile.svelte
    └── dashboard.svelte
```

#### 2. Import Strategies
```typescript
// Barrel exports for clean imports
// src/lib/components/ui/index.ts
export * from './button';
export * from './card';
export * from './input';

// Usage in components
import { Button, Card, Input } from "$lib/components/ui";
```

#### 3. Type Safety
```svelte
<script lang="ts">
  import type { ComponentType } from "svelte";
  import { Button } from "$lib/components/ui/button";

  interface ButtonProps {
    variant?: "default" | "destructive";
    size?: "sm" | "default" | "lg";
    disabled?: boolean;
    onclick?: () => void;
  }

  // Generic reusable button component
  const createButton = (props: ButtonProps): ComponentType<ButtonProps> => {
    return Button;
  };
</script>
```

### Performance Optimization

#### 1. Bundle Optimization
```javascript
// vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  optimizeDeps: {
    exclude: ['@lucide/svelte'] // Tree-shake icons individually
  }
});
```

#### 2. Dynamic Imports
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";

  // Lazy load heavy components
  let ChartComponent: ComponentType | null = null;

  async function loadChart() {
    const module = await import("$lib/components/ui/chart");
    ChartComponent = module.Chart;
  }
</script>

<Button onclick={loadChart}>Load Chart</Button>
{#if ChartComponent}
  <svelte:component this={ChartComponent} />
{/if}
```

#### 3. Icon Optimization
```svelte
<script lang="ts">
  // Import specific icons instead of the whole library
  import Plus from "@lucide/svelte/icons/plus";
  import Trash2 from "@lucide/svelte/icons/trash-2";
</script>

<Button>
  <Plus class="h-4 w-4 mr-2" />
  Add Item
</Button>
```

### Accessibility Best Practices

#### 1. Semantic HTML
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Label } from "$lib/components/ui/label";
</script>

<!-- Good: Semantic association -->
<Label for="email-input">Email Address</Label>
<Input id="email-input" type="email" />

<!-- Bad: No semantic association -->
<div>Email Address</div>
<Input type="email" />
```

#### 2. ARIA Attributes
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<!-- Descriptive button for screen readers -->
<Button
  aria-label="Delete item from list"
  aria-describedby="delete-confirmation"
>
  <Trash2 class="h-4 w-4" />
</Button>

<div id="delete-confirmation" class="sr-only">
  This will permanently remove the item
</div>
```

#### 3. Keyboard Navigation
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";

  let isOpen = $state(false);

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      isOpen = false;
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<Button
  onclick={() => isOpen = true}
  aria-expanded={isOpen}
  aria-haspopup="true"
>
  Open Menu
</Button>

{#if isOpen}
  <div
    class="absolute top-full mt-2 bg-popover border rounded-md shadow-lg"
    on:keydown|stopPropagation
  >
    <!-- Menu content -->
  </div>
{/if}
```

### Testing with shadcn-svelte

#### Component Testing
```typescript
// src/lib/components/ui/button/Button.test.ts
import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import Button from './Button.svelte';

describe('Button', () => {
  it('renders with default props', () => {
    render(Button, { children: 'Click me' });
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(Button, {
      children: 'Click me',
      onclick: handleClick
    });

    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant classes correctly', () => {
    render(Button, {
      children: 'Destructive',
      variant: 'destructive'
    });

    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });
});
```

#### E2E Testing with Playwright
```typescript
// tests/e2e/button.spec.ts
import { test, expect } from '@playwright/test';

test('button interactions', async ({ page }) => {
  await page.goto('/');

  // Test button click
  const button = page.getByRole('button', { name: 'Submit' });
  await button.click();

  // Test disabled state
  await expect(page.getByRole('button', { name: 'Disabled' })).toBeDisabled();

  // Test keyboard navigation
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Focused' })).toBeFocused();
});
```

## Troubleshooting

### Common Issues

#### 1. Tailwind CSS Not Working

**Problem**: Components don't have proper styling.

**Solution**:
```bash
# Check Tailwind configuration
npx tailwindcss --help

# Verify CSS is being imported
# src/app.css should include:
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Verify in `svelte.config.js`**:
```javascript
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter()
  }
};

export default config;
```

#### 2. TypeScript Errors

**Problem**: Type errors for component props.

**Solution**: Ensure proper type definitions:
```typescript
// src/lib/components/ui/button/types.ts
export interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  class?: string;
  disabled?: boolean;
  onclick?: (event: MouseEvent) => void;
}
```

#### 3. Dark Mode Not Working

**Problem**: Dark mode styles not applying.

**Solution**: Check CSS variables and class application:
```css
/* Ensure CSS variables are properly defined */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

**Verify dark class is applied to HTML element**:
```javascript
// In your layout or app component
import { browser } from '$app/environment';
import { onMount } from 'svelte';

onMount(() => {
  if (browser) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.classList.toggle('dark', prefersDark);
  }
});
```

#### 4. Icons Not Displaying

**Problem**: Lucide icons not showing up.

**Solution**: Install and import correctly:
```bash
npm install @lucide/svelte
```

```svelte
<script lang="ts">
  // Import specific icons
  import Plus from "@lucide/svelte/icons/plus";
  import { Menu } from "@lucide/svelte"; // Tree-shakable
</script>
```

#### 5. Build Errors

**Problem**: Production build failing due to CSS or JS issues.

**Solution**: Check bundle analyzer and dependencies:
```bash
# Analyze bundle size
npm run build -- --analyze

# Check for missing dependencies
npm ls tailwind-variants clsx tailwind-merge tw-animate-css
```

### Debugging Techniques

#### 1. Component Props Debugging
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";

  let debugProps = {
    variant: "default",
    size: "lg",
    class: "custom-class"
  };

  $: console.log('Button props:', debugProps);
</script>

<Button {...debugProps}>
  Debug Button
</Button>
```

#### 2. CSS Class Inspection
```svelte
<script lang="ts">
  import { cn } from "$lib/utils";

  let buttonClasses = cn(
    "base-class",
    "conditional-class" && true,
    "another-class"
  );

  $: console.log('Applied classes:', buttonClasses);
</script>
```

#### 3. State Debugging
```svelte
<script lang="ts">
  let isOpen = $state(false);

  function toggle() {
    isOpen = !isOpen;
    console.log('State changed:', isOpen);
  }
</script>

<Button onclick={toggle}>
  Toggle (currently: {isOpen ? 'open' : 'closed'})
</Button>
```

### Performance Issues

#### 1. Large Bundle Size

**Diagnose**:
```bash
# Analyze bundle
npm run build
npx vite-bundle-analyzer .svelte-kit/output/client
```

**Solutions**:
```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['@lucide/svelte', 'bits-ui'],
          ui: ['./src/lib/components/ui']
        }
      }
    }
  }
});
```

#### 2. Slow Component Rendering

**Use Svelte 5 Features**:
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";

  // Use $derived for computed values
  let items = $state([]);
  let filteredItems = $derived(
    items.filter(item => item.active)
  );

  // Use $effect for side effects
  $effect(() => {
    console.log('Items changed:', items.length);
  });
</script>
```

## Community & Resources

### Official Resources

- **Documentation**: [shadcn-svelte.com](https://www.shadcn-svelte.com)
- **GitHub Repository**: [github.com/huntabyte/shadcn-svelte](https://github.com/huntabyte/shadcn-svelte)
- **Component Examples**: [shadcn-svelte.com/docs/components](https://www.shadcn-svelte.com/docs/components)
- **Discord Community**: [Join the discussion](https://discord.gg/shadcn-svelte)

### Related Projects

- **Bits UI**: [bits-ui.com](https://bits-ui.com) - Underlying headless primitives
- **shadcn/ui**: [ui.shadcn.com](https://ui.shadcn.com) - Original React version
- **Tailwind CSS**: [tailwindcss.com](https://tailwindcss.com) - Utility-first CSS framework
- **Lucide**: [lucide.dev](https://lucide.dev) - Icon library
- **Superforms**: [superforms.rocks](https://superforms.rocks) - Form validation library

### Learning Resources

#### Tutorials & Guides
- [Official Getting Started Guide](https://www.shadcn-svelte.com/docs/getting-started)
- [Component Customization Guide](https://www.shadcn-svelte.com/docs/customization)
- [Svelte 5 Migration Guide](https://www.shadcn-svelte.com/docs/migration/svelte-5)

#### Video Content
- [shadcn-svelte YouTube Channel](https://youtube.com/@shadcn-svelte)
- [Svelte Masterclass](https://svelte.dev/tutorial) - Learn Svelte fundamentals
- [Tailwind CSS Course](https://tailwindcss.com/course) - Master utility-first CSS

#### Blog Posts & Articles
- ["Building Beautiful Apps with shadcn-svelte"](https://dev.to/shadcn-svelte)
- ["Accessibility Best Practices with Svelte"](https://svelte.dev/blog/accessibility)
- ["Performance Optimization in SvelteKit"](https://kit.svelte.dev/docs/adapter)

### Contributing

#### How to Contribute
1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/new-component`
3. **Make your changes** following the contribution guidelines
4. **Test thoroughly** including accessibility and browser compatibility
5. **Submit a pull request** with detailed description

#### Component Contribution Guidelines
- Follow the established component structure and patterns
- Ensure full TypeScript support with proper types
- Include comprehensive documentation and examples
- Test accessibility with keyboard navigation and screen readers
- Maintain consistency with existing design system

#### Bug Reports
- Use the GitHub issue tracker for bug reports
- Include reproduction steps, browser information, and expected behavior
- Provide minimal reproduction examples when possible
- Tag issues appropriately (bug, enhancement, documentation)

### Professional Support

#### Commercial Support
- **Priority Support**: Direct access to maintainers
- **Custom Development**: Bespoke component development
- **Team Training**: Onboarding and best practices workshops
- **Code Review**: Professional review of your implementations

#### Consulting Services
- **Architecture Design**: System architecture with shadcn-svelte
- **Performance Optimization**: Bundle optimization and runtime performance
- **Accessibility Audits**: WCAG compliance and accessibility improvements
- **Design System Implementation**: Custom design system development

---

## Conclusion

shadcn-svelte provides a powerful, flexible foundation for building beautiful, accessible Svelte applications. By following the patterns and best practices outlined in this guide, you can create maintainable, performant applications that provide excellent user experiences.

Key takeaways:

1. **Copy-Paste Architecture** gives you complete ownership and control
2. **Accessibility First** ensures your applications work for everyone
3. **Tailwind Integration** provides consistent, maintainable styling
4. **TypeScript Support** catches errors at development time
5. **Svelte 5 Features** enable reactive, performant applications
6. **Community Ecosystem** provides support and continuous improvement

Ready to start building? Check out the [Quick Start](#quick-start) section and explore the [Component Library](#component-library) to see what's possible.

---

*This guide covers shadcn-svelte as of version 1.0. For the most up-to-date information, visit the [official shadcn-svelte documentation](https://www.shadcn-svelte.com).*

## License

shadcn-svelte is licensed under the MIT License, making it free for commercial and personal use. See the [GitHub repository](https://github.com/huntabyte/shadcn-svelte/blob/main/LICENSE) for the full license text.