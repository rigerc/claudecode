# Best Practices Guide

This comprehensive guide covers development patterns, architectural decisions, and best practices for building robust applications with shadcn-svelte and Tailwind CSS.

## Core Principles

### 1. Component-First Architecture

Build your application from the outside-in with reusable components:

```svelte
<!-- Good: Focused, reusable component -->
<!-- src/lib/components/ui/data-table/DataTable.svelte -->
<script lang="ts">
  import { createTable } from '@tanstack/svelte-table';
  import { cn } from '$lib/utils';
  import type { ColumnDef } from '@tanstack/table-core';

  interface Props {
    data: any[];
    columns: ColumnDef<any>[];
    class?: string;
  }

  let { data, columns, class: className }: Props = $props();

  const table = createTable({
    get data() {
      return data;
    },
    get columns() {
      return columns;
    },
  });
</script>

<div class={cn('rounded-md border', className)}>
  <table class="w-full">
    <thead>
      {#each table.getHeaderGroups() as headerGroup}
        <tr>
          {#each headerGroup.headers as header}
            <th class="border-b px-4 py-2 text-left font-medium">
              {!header.isPlaceholder && header.render()}
            </th>
          {/each}
        </tr>
      {/each}
    </thead>
    <tbody>
      {#each table.getRowModel().rows as row}
        <tr class="border-b">
          {#each row.getVisibleCells() as cell}
            <td class="px-4 py-2">
              {cell.render()}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
```

### 2. Semantic HTML Structure

Use proper HTML semantics for accessibility and SEO:

```svelte
<!-- Good: Proper semantic structure -->
<script lang="ts">
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Badge } from '$lib/components/ui/badge';
  import type { BlogPost } from '$lib/types/blog';
</script>

{#each posts as post (post.id)}
  <article class="group">
    <Card class="overflow-hidden transition-shadow hover:shadow-lg">
      <CardHeader>
        <div class="flex items-start justify-between">
          <div class="space-y-1">
            <CardTitle>
              <a href="/blog/{post.slug}" class="hover:text-primary">
                {post.title}
              </a>
            </CardTitle>
            <CardDescription>
              {post.excerpt}
            </CardDescription>
          </div>
          <Badge variant="secondary">
            {post.category}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <time datetime={post.publishedAt} class="text-sm text-muted-foreground">
          {new Date(post.publishedAt).toLocaleDateString()}
        </time>
        <footer class="mt-4">
          <a
            href="/blog/{post.slug}"
            class="inline-flex items-center text-sm font-medium text-primary hover:underline"
            aria-label={`Read more about ${post.title}`}
          >
            Read more
          </a>
        </footer>
      </CardContent>
    </Card>
  </article>
{/each}
```

### 3. Consistent Naming Conventions

Follow consistent naming patterns across your codebase:

```typescript
// ✅ Good: Descriptive, consistent naming
export interface UserProfile {
  id: string;
  fullName: string;
  emailAddress: string;
  profileImageUrl: string | null;
  isActive: boolean;
  lastLoginAt: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface BlogPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  content: string;
  authorId: string;
  categoryId: string;
  publishedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
}

// ❌ Bad: Inconsistent naming
export interface User {
  userId: string;
  name: string;
  email: string;
  avatar_url: string | null;
  active: boolean;
  last_login: Date;
  created_at: Date;
  updated_at: Date;
}
```

## Component Architecture Patterns

### 1. Composition Over Inheritance

Build complex components by composing smaller, focused components:

```svelte
<!-- Good: Composed component -->
<!-- src/lib/components/complex/DashboardCard.svelte -->
<script lang="ts">
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Badge } from '$lib/components/ui/badge';
  import { Button } from '$lib/components/ui/button';
  import { TrendingUpIcon, TrendingDownIcon, MoreHorizontalIcon } from 'lucide-svelte';

  interface Props {
    title: string;
    description?: string;
    value: string | number;
    change?: number;
    changeLabel?: string;
    trend?: 'up' | 'down' | 'neutral';
    badge?: string;
    action?: {
      label: string;
      onClick: () => void;
    };
    class?: string;
  }

  let {
    title,
    description,
    value,
    change = 0,
    changeLabel,
    trend = change > 0 ? 'up' : change < 0 ? 'down' : 'neutral',
    badge,
    action,
    class: className,
  }: Props = $props();

  $: trendIcon = trend === 'up' ? TrendingUpIcon : trend === 'down' ? TrendingDownIcon : null;
  $: trendColor = trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600';
</script>

<Card class={className}>
  <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
    <div class="space-y-1">
      <CardTitle class="text-sm font-medium">{title}</CardTitle>
      {#if description}
        <CardDescription>{description}</CardDescription>
      {/if}
    </div>
    <div class="flex items-center space-x-2">
      {#if badge}
        <Badge variant="secondary">{badge}</Badge>
      {/if}
      {#if action}
        <Button variant="ghost" size="sm" on:click={action.onClick}>
          <MoreHorizontalIcon class="h-4 w-4" />
        </Button>
      {/if}
    </div>
  </CardHeader>
  <CardContent>
    <div class="text-2xl font-bold">{value}</div>
    {#if change !== 0}
      <div class="flex items-center space-x-1 text-sm {trendColor}">
        {#if trendIcon}
          <svelte:component this={trendIcon} class="h-4 w-4" />
        {/if}
        <span>
          {Math.abs(change)}% {changeLabel || 'from last period'}
        </span>
      </div>
    {/if}
  </CardContent>
</Card>
```

### 2. Compound Components

Use compound component patterns for complex interactions:

```svelte
<!-- Good: Compound component pattern -->
<!-- src/lib/components/ui/tabs/Tabs.svelte -->
<script lang="ts">
  import { setContext, onMount } from 'svelte';
  import { cn } from '$lib/utils';
  import { writable } from 'svelte/store';

  // Create context for tabs
  const TabsContext = Symbol('TabsContext');

  interface Props {
    value?: string;
    defaultValue?: string;
    onValueChange?: (value: string) => void;
    class?: string;
    children: any;
  }

  let {
    value: controlledValue,
    defaultValue = '',
    onValueChange,
    class: className,
    children,
  }: Props = $props();

  const selectedTab = writable(controlledValue || defaultValue);

  // Set up context for child components
  setContext(TabsContext, {
    selectedTab,
    onValueChange: (newValue: string) => {
      selectedTab.set(newValue);
      onValueChange?.(newValue);
    }
  });

  // Sync controlled value
  $: if (controlledValue !== undefined && $selectedTab !== controlledValue) {
    selectedTab.set(controlledValue);
  }
</script>

<div class={className}>
  {@render children()}
</div>

<!-- TabsList.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  import { cn } from '$lib/utils';

  const TabsContext = Symbol('TabsContext');
  const { selectedTab } = getContext(TabsContext);

  interface Props {
    class?: string;
    children: any;
  }

  let { class: className, children }: Props = $props();
</script>

<div
  role="tablist"
  class={cn(
    "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
    className
  )}
>
  {@render children()}
</div>

<!-- TabsTrigger.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  import { cn } from '$lib/utils';

  const TabsContext = Symbol('TabsContext');
  const { selectedTab, onValueChange } = getContext(TabsContext);

  interface Props {
    value: string;
    class?: string;
    children: any;
  }

  let { value, class: className, children }: Props = $props();
</script>

<button
  role="tab"
  class={cn(
    "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    $selectedTab === value
      ? "bg-background text-foreground shadow-sm"
      : "transparent hover:bg-background/50",
    className
  )}
  on:click={() => onValueChange(value)}
  aria-selected={$selectedTab === value}
>
  {@render children()}
</button>
```

### 3. Slot-Based Components

Use Svelte's slot system for flexible component composition:

```svelte
<!-- Good: Slot-based component -->
<!-- src/lib/components/ui/layout/FormField.svelte -->
<script lang="ts">
  import { Label } from '$lib/components/ui/label';
  import { cn } from '$lib/utils';

  interface Props {
    id?: string;
    label?: string;
    description?: string;
    error?: string;
    required?: boolean;
    class?: string;
    children: any;
  }

  let {
    id,
    label,
    description,
    error,
    required = false,
    class: className,
    children,
  }: Props = $props();

  // Generate unique ID if not provided
  $: fieldId = id || `field-${Math.random().toString(36).substr(2, 9)}`;
</script>

<div class={cn('space-y-2', className)}>
  {#if label}
    <Label for={fieldId} class="text-sm font-medium">
      {label}
      {#if required}
        <span class="text-red-500 ml-1">*</span>
      {/if}
    </Label>
  {/if}

  <!-- Slot for form input -->
  <div class="relative">
    {@render children({ id: fieldId, 'aria-describedby': description ? `${fieldId}-description` : undefined, 'aria-invalid': !!error })}
  </div>

  {#if description}
    <p id={`${fieldId}-description`} class="text-sm text-muted-foreground">
      {description}
    </p>
  {/if}

  {#if error}
    <p id={`${fieldId}-error`} class="text-sm text-red-500">
      {error}
    </p>
  {/if}
</div>
```

## State Management Patterns

### 1. Local Component State

For simple component interactions, use Svelte's reactive statements:

```svelte
<!-- Good: Simple local state -->
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';

  let searchTerm = '';
  let filteredItems = [];
  let selectedItems = new Set();

  const items = [
    { id: 1, name: 'Apple', category: 'fruit' },
    { id: 2, name: 'Carrot', category: 'vegetable' },
    { id: 3, name: 'Banana', category: 'fruit' },
    { id: 4, name: 'Broccoli', category: 'vegetable' },
  ];

  // Reactive filtering
  $: filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  function toggleSelection(itemId: number) {
    const newSelection = new Set(selectedItems);
    if (newSelection.has(itemId)) {
      newSelection.delete(itemId);
    } else {
      newSelection.add(itemId);
    }
    selectedItems = newSelection;
  }

  function clearSelection() {
    selectedItems = new Set();
  }
</script>

<Card>
  <CardHeader>
    <CardTitle>Select Items</CardTitle>
    <CardDescription>Choose items from the list below</CardDescription>
  </CardHeader>
  <CardContent class="space-y-4">
    <div class="space-y-2">
      <Input
        placeholder="Search items..."
        bind:value={searchTerm}
      />
      {#if selectedItems.size > 0}
        <div class="flex items-center justify-between">
          <span class="text-sm text-muted-foreground">
            {selectedItems.size} item{selectedItems.size !== 1 ? 's' : ''} selected
          </span>
          <Button variant="outline" size="sm" on:click={clearSelection}>
            Clear
          </Button>
        </div>
      {/if}
    </div>

    <div class="space-y-2">
      {#each filteredItems as item (item.id)}
        <div
          class="flex items-center space-x-2 p-2 rounded border cursor-pointer hover:bg-muted"
          class:bg-muted={selectedItems.has(item.id)}
          on:click={() => toggleSelection(item.id)}
          role="option"
          aria-selected={selectedItems.has(item.id)}
        >
          <input
            type="checkbox"
            checked={selectedItems.has(item.id)}
            on:change={() => toggleSelection(item.id)}
          />
          <span>{item.name}</span>
          <Badge variant="secondary">{item.category}</Badge>
        </div>
      {/each}
    </div>
  </CardContent>
</Card>
```

### 2. Store-Based State

For complex state shared across components, use Svelte stores:

```typescript
// src/lib/stores/auth.ts
import { writable, derived } from 'svelte/store';
import type { User } from '$lib/types/user';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    isLoading: false,
    error: null,
  });

  // Derived stores
  const isAuthenticated = derived(
    subscribe,
    $state => $state.user !== null
  );

  const userRole = derived(
    subscribe,
    $state => $state.user?.role || 'guest'
  );

  return {
    subscribe,
    set,
    update,
    isAuthenticated,
    userRole,

    // Actions
    login: async (email: string, password: string) => {
      update(state => ({ ...state, isLoading: true, error: null }));

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
          throw new Error('Login failed');
        }

        const { user } = await response.json();
        set({ user, isLoading: false, error: null });
      } catch (error) {
        update(state => ({
          ...state,
          isLoading: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        }));
      }
    },

    logout: () => {
      set({ user: null, isLoading: false, error: null });
    },

    clearError: () => {
      update(state => ({ ...state, error: null }));
    },
  };
}

export const auth = createAuthStore();
```

### 3. Form State Management

Use libraries like `zod` and `sveltekit-superforms` for complex forms:

```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms/client';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Alert, AlertDescription } from '$lib/components/ui/alert';
  import { AlertCircleIcon } from 'lucide-svelte';

  const schema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters'),
    email: z.string().email('Invalid email address'),
    company: z.string().optional(),
    message: z.string().min(10, 'Message must be at least 10 characters'),
  });

  const { form, errors, message, enhance, submitting } = superForm(zodClient(schema), {
    onResult: ({ result }) => {
      if (result.type === 'success') {
        // Handle success
        console.log('Form submitted successfully');
      }
    },
  });
</script>

<Card class="w-full max-w-2xl">
  <CardHeader>
    <CardTitle>Contact Form</CardTitle>
    <CardDescription>
      Send us a message and we'll get back to you as soon as possible.
    </CardDescription>
  </CardHeader>
  <CardContent>
    <form method="POST" use:enhance class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <Label for="name">Name *</Label>
          <Input
            id="name"
            name="name"
            bind:value={$form.name}
            class={errors.name ? 'border-red-500' : ''}
            aria-invalid={!!errors.name}
            aria-describedby="name-error"
          />
          {#if errors.name}
            <p id="name-error" class="text-sm text-red-500">
              {errors.name}
            </p>
          {/if}
        </div>

        <div class="space-y-2">
          <Label for="email">Email *</Label>
          <Input
            id="email"
            name="email"
            type="email"
            bind:value={$form.email}
            class={errors.email ? 'border-red-500' : ''}
            aria-invalid={!!errors.email}
            aria-describedby="email-error"
          />
          {#if errors.email}
            <p id="email-error" class="text-sm text-red-500">
              {errors.email}
            </p>
          {/if}
        </div>
      </div>

      <div class="space-y-2">
        <Label for="company">Company</Label>
        <Input
          id="company"
          name="company"
          bind:value={$form.company}
        />
      </div>

      <div class="space-y-2">
        <Label for="message">Message *</Label>
        <textarea
          id="message"
          name="message"
          bind:value={$form.message}
          class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          class:border-red-500={errors.message}
          aria-invalid={!!errors.message}
          aria-describedby="message-error"
        ></textarea>
        {#if errors.message}
          <p id="message-error" class="text-sm text-red-500">
            {errors.message}
          </p>
        {/if}
      </div>

      {#if message}
        <Alert variant={message.type === 'success' ? 'default' : 'destructive'}>
          <AlertCircleIcon class="h-4 w-4" />
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      {/if}

      <Button type="submit" disabled={$submitting} class="w-full">
        {$submitting ? 'Sending...' : 'Send Message'}
      </Button>
    </form>
  </CardContent>
</Card>
```

## Performance Patterns

### 1. Lazy Loading Components

Load components only when needed to reduce bundle size:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';

  let showHeavyComponent = false;
  let HeavyComponent: any = null;

  async function loadHeavyComponent() {
    if (!HeavyComponent) {
      const module = await import('$lib/components/heavy/HeavyComponent.svelte');
      HeavyComponent = module.default;
    }
    showHeavyComponent = true;
  }
</script>

<Card>
  <CardHeader>
    <CardTitle>Lazy Loading Example</CardTitle>
  </CardHeader>
  <CardContent class="space-y-4">
    <Button on:click={loadHeavyComponent}>
      Load Heavy Component
    </Button>

    {#if showHeavyComponent && HeavyComponent}
      <div class="border rounded-lg p-4">
        <svelte:component this={HeavyComponent} />
      </div>
    {/if}
  </CardContent>
</Card>
```

### 2. Memoization

Use Svelte's reactivity carefully to avoid unnecessary computations:

```svelte
<script lang="ts">
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Input } from '$lib/components/ui/input';

  let searchTerm = '';
  const items = Array.from({ length: 1000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`,
    value: Math.random() * 100,
    category: ['A', 'B', 'C'][i % 3],
  }));

  // ❌ Bad: Runs on every render
  // const filteredItems = items.filter(item =>
  //   item.name.toLowerCase().includes(searchTerm.toLowerCase())
  // );

  // ✅ Good: Memoized with reactive statement
  $: filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // ✅ Better: Computed expensive operations separately
  $: searchLower = searchTerm.toLowerCase();
  $: filteredItemsOptimized = items.filter(item =>
    item.name.toLowerCase().includes(searchLower)
  );
</script>

<Card>
  <CardHeader>
    <CardTitle>Performance Example</CardTitle>
  </CardHeader>
  <CardContent class="space-y-4">
    <Input
      placeholder="Search items..."
      bind:value={searchTerm}
    />

    <div class="space-y-2 max-h-64 overflow-y-auto">
      {#each filteredItemsOptimized as item (item.id)}
        <div class="p-2 border rounded">
          <div class="flex justify-between">
            <span>{item.name}</span>
            <Badge variant="secondary">{item.category}</Badge>
          </div>
          <div class="text-sm text-muted-foreground">
            Value: {item.value.toFixed(2)}
          </div>
        </div>
      {/each}
    </div>
  </CardContent>
</Card>
```

### 3. Virtual Scrolling

For large lists, implement virtual scrolling:

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';

  // Generate large dataset
  const items = Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`,
    value: Math.random() * 100,
  }));

  let containerHeight = 400;
  let itemHeight = 40;
  let scrollTop = 0;
  let containerElement: HTMLElement;

  $: visibleCount = Math.ceil(containerHeight / itemHeight) + 2;
  $: startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - 1);
  $: endIndex = Math.min(items.length, startIndex + visibleCount);
  $: visibleItems = items.slice(startIndex, endIndex);

  function handleScroll() {
    if (containerElement) {
      scrollTop = containerElement.scrollTop;
    }
  }
</script>

<Card>
  <CardHeader>
    <CardTitle>Virtual Scrolling ({items.length} items)</CardTitle>
  </CardHeader>
  <CardContent>
    <div
      class="border rounded overflow-hidden"
      style="height: {containerHeight}px"
      bind:this={containerElement}
      on:scroll={handleScroll}
    >
      <div style="height: {items.length * itemHeight}px; position: relative;">
        <div style="transform: translateY({startIndex * itemHeight}px);">
          {#each visibleItems as item (item.id)}
            <div
              class="flex items-center px-4 border-b hover:bg-muted"
              style="height: {itemHeight}px;"
            >
              <span class="font-medium">{item.name}</span>
              <span class="ml-auto text-sm text-muted-foreground">
                {item.value.toFixed(2)}
              </span>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </CardContent>
</Card>
```

## Accessibility Patterns

### 1. ARIA Labels and Descriptions

Ensure all interactive elements have proper accessibility attributes:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { SearchIcon, XIcon } from 'lucide-svelte';

  let searchValue = '';
  let searchId = 'search-input';
</script>

<div class="relative">
  <SearchIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />

  <Input
    id={searchId}
    type="search"
    placeholder="Search..."
    bind:value={searchValue}
    class="pl-10 pr-10"
    aria-label="Search through items"
    aria-describedby="search-description"
  />

  {#if searchValue}
    <Button
      variant="ghost"
      size="sm"
      class="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0"
      on:click={() => searchValue = ''}
      aria-label="Clear search"
    >
      <XIcon class="h-4 w-4" />
    </Button>
  {/if}
</div>

<p id="search-description" class="sr-only">
  Search through available items by typing keywords
</p>
```

### 2. Keyboard Navigation

Implement proper keyboard navigation for custom components:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';

  const items = [
    { id: 1, name: 'Option 1', description: 'Description for option 1' },
    { id: 2, name: 'Option 2', description: 'Description for option 2' },
    { id: 3, name: 'Option 3', description: 'Description for option 3' },
    { id: 4, name: 'Option 4', description: 'Description for option 4' },
  ];

  let focusedIndex = 0;
  let selectedItems = new Set<number>();

  function handleKeydown(event: KeyboardEvent) {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        focusedIndex = (focusedIndex + 1) % items.length;
        break;
      case 'ArrowUp':
        event.preventDefault();
        focusedIndex = focusedIndex === 0 ? items.length - 1 : focusedIndex - 1;
        break;
      case 'Enter':
      case ' ':
        event.preventDefault();
        toggleSelection(items[focusedIndex].id);
        break;
      case 'Home':
        event.preventDefault();
        focusedIndex = 0;
        break;
      case 'End':
        event.preventDefault();
        focusedIndex = items.length - 1;
        break;
    }
  }

  function toggleSelection(itemId: number) {
    const newSelection = new Set(selectedItems);
    if (newSelection.has(itemId)) {
      newSelection.delete(itemId);
    } else {
      newSelection.add(itemId);
    }
    selectedItems = newSelection;
  }

  function handleClick(itemId: number) {
    focusedIndex = items.findIndex(item => item.id === itemId);
    toggleSelection(itemId);
  }
</script>

<Card>
  <CardHeader>
    <CardTitle>Keyboard Navigation Example</CardTitle>
  </CardHeader>
  <CardContent>
    <div
      class="border rounded-lg p-2"
      role="listbox"
      aria-label="Selectable options"
      aria-multiselectable="true"
      on:keydown={handleKeydown}
      tabindex="0"
    >
      {#each items as item, index (item.id)}
        <div
          class="flex items-center space-x-3 p-3 rounded cursor-pointer"
          class:bg-muted={focusedIndex === index}
          class:ring-2={focusedIndex === index}
          class:ring-primary={focusedIndex === index}
          role="option"
          aria-selected={selectedItems.has(item.id)}
          on:click={() => handleClick(item.id)}
        >
          <input
            type="checkbox"
            checked={selectedItems.has(item.id)}
            tabindex="-1"
            aria-hidden="true"
          />
          <div>
            <div class="font-medium">{item.name}</div>
            <div class="text-sm text-muted-foreground">{item.description}</div>
          </div>
        </div>
      {/each}
    </div>

    {#if selectedItems.size > 0}
      <div class="mt-4">
        <Button variant="outline" on:click={() => selectedItems = new Set()}>
          Clear Selection ({selectedItems.size})
        </Button>
      </div>
    {/if}
  </CardContent>
</Card>
```

### 3. Focus Management

Manage focus properly for modals and dynamic content:

```svelte
<script lang="ts">
  import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '$lib/components/ui/dialog';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { onMount, onDestroy } from 'svelte';

  let open = false;
  let focusTrapElement: HTMLElement;
  let previousFocus: HTMLElement | null = null;

  // Store previously focused element
  function storePreviousFocus() {
    previousFocus = document.activeElement as HTMLElement;
  }

  // Restore focus when closing
  function restoreFocus() {
    if (previousFocus && typeof previousFocus.focus === 'function') {
      previousFocus.focus();
    }
  }

  // Handle focus trap
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      open = false;
      restoreFocus();
    }

    if (event.key === 'Tab') {
      const focusableElements = focusTrapElement?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusableElements && focusableElements.length > 0) {
        const firstElement = focusableElements[0] as HTMLElement;
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

        if (event.shiftKey && document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        } else if (!event.shiftKey && document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    }
  }

  $: if (open) {
    storePreviousFocus();
    setTimeout(() => {
      const firstInput = focusTrapElement?.querySelector('input');
      if (firstInput) {
        firstInput.focus();
      }
    }, 0);
  }
</script>

<Dialog bind:open>
  <DialogTrigger asChild>
    <Button on:click={() => storePreviousFocus()}>
      Open Modal
    </Button>
  </DialogTrigger>
  <DialogContent
    bind:this={focusTrapElement}
    on:keydown={handleKeydown}
    on:mouseleave={() => restoreFocus()}
  >
    <DialogHeader>
      <DialogTitle>Focus Management Example</DialogTitle>
    </DialogHeader>
    <div class="space-y-4 py-4">
      <div class="space-y-2">
        <Label for="name">Name</Label>
        <Input id="name" placeholder="Enter your name" />
      </div>
      <div class="space-y-2">
        <Label for="email">Email</Label>
        <Input id="email" type="email" placeholder="Enter your email" />
      </div>
      <div class="space-y-2">
        <Label for="message">Message</Label>
        <textarea
          id="message"
          class="w-full p-2 border rounded"
          rows={3}
          placeholder="Your message..."
        ></textarea>
      </div>
    </div>
    <div class="flex justify-end space-x-2">
      <Button variant="outline" on:click={() => { open = false; restoreFocus(); }}>
        Cancel
      </Button>
      <Button on:click={() => { open = false; restoreFocus(); }}>
        Submit
      </Button>
    </div>
  </DialogContent>
</Dialog>
```

## Testing Patterns

### 1. Component Testing

Write focused tests for individual components:

```typescript
// Button.test.ts
import { render, fireEvent } from '@testing-library/svelte';
import { vi } from 'vitest';
import { Button } from '$lib/components/ui/button';

describe('Button Component', () => {
  test('renders with default props', () => {
    const { getByRole } = render(Button, {
      props: {
        children: 'Click me'
      }
    });

    const button = getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-primary', 'text-primary-foreground');
  });

  test('applies variant classes correctly', () => {
    const { getByRole } = render(Button, {
      props: {
        variant: 'destructive',
        children: 'Delete'
      }
    });

    const button = getByRole('button');
    expect(button).toHaveClass('bg-destructive', 'text-destructive-foreground');
  });

  test('handles click events', async () => {
    const handleClick = vi.fn();
    const { getByRole } = render(Button, {
      props: {
        children: 'Click me',
        onclick: handleClick
      }
    });

    const button = getByRole('button');
    await fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('can be disabled', () => {
    const { getByRole } = render(Button, {
      props: {
        disabled: true,
        children: 'Disabled'
      }
    });

    const button = getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveClass('disabled:opacity-50');
  });
});
```

### 2. Integration Testing

Test component interactions and state management:

```typescript
// FormIntegration.test.ts
import { render, fireEvent, waitFor } from '@testing-library/svelte';
import { vi } from 'vitest';
import ContactForm from '$lib/components/ContactForm.svelte';

describe('Contact Form Integration', () => {
  test('validates form fields correctly', async () => {
    const { getByLabelText, getByRole, getByText } = render(ContactForm);

    const submitButton = getByRole('button', { name: 'Send Message' });

    // Try to submit empty form
    await fireEvent.click(submitButton);

    // Should show validation errors
    expect(getByText('Name is required')).toBeInTheDocument();
    expect(getByText('Email is required')).toBeInTheDocument();
    expect(getByText('Message is required')).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    const mockSubmit = vi.fn();
    const { getByLabelText, getByRole } = render(ContactForm, {
      props: {
        onSubmit: mockSubmit
      }
    });

    // Fill out form
    await fireEvent.change(getByLabelText('Name'), {
      target: { value: 'John Doe' }
    });
    await fireEvent.change(getByLabelText('Email'), {
      target: { value: 'john@example.com' }
    });
    await fireEvent.change(getByLabelText('Message'), {
      target: { value: 'This is a test message' }
    });

    // Submit form
    await fireEvent.click(getByRole('button', { name: 'Send Message' }));

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
        message: 'This is a test message'
      });
    });
  });
});
```

### 3. E2E Testing

Use Playwright for end-to-end testing:

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('displays dashboard correctly', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('[data-testid="stats-cards"]')).toBeVisible();
  });

  test('can navigate between sections', async ({ page }) => {
    await page.click('[data-testid="analytics-tab"]');
    await expect(page.locator('[data-testid="analytics-content"]')).toBeVisible();

    await page.click('[data-testid="reports-tab"]');
    await expect(page.locator('[data-testid="reports-content"]')).toBeVisible();
  });

  test('responsive design works on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    // Mobile navigation should be collapsed
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
    await expect(page.locator('[data-testid="desktop-menu"]')).not.toBeVisible();

    // Should be able to open mobile menu
    await page.click('[data-testid="mobile-menu-button"]');
    await expect(page.locator('[data-testid="mobile-nav-items"]')).toBeVisible();
  });
});
```

## Code Organization

### 1. File Structure

Organize your components and utilities logically:

```
src/
├── lib/
│   ├── components/
│   │   ├── ui/                 # shadcn-svelte components
│   │   │   ├── button/
│   │   │   ├── card/
│   │   │   └── index.ts
│   │   ├── forms/              # Form components
│   │   │   ├── ContactForm.svelte
│   │   │   └── UserForm.svelte
│   │   ├── layout/             # Layout components
│   │   │   ├── Header.svelte
│   │   │   ├── Sidebar.svelte
│   │   │   └── Footer.svelte
│   │   └── features/           # Feature-specific components
│   │       ├── auth/
│   │       ├── dashboard/
│   │       └── profile/
│   ├── stores/                # State management
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   └── theme.ts
│   ├── types/                 # TypeScript definitions
│   │   ├── user.ts
│   │   ├── api.ts
│   │   └── ui.ts
│   ├── utils/                 # Utility functions
│   │   ├── api.ts
│   │   ├── validation.ts
│   │   └── format.ts
│   ├── styles/                # Custom styles
│   │   ├── components.css
│   │   └── animations.css
│   └── hooks/                 # Custom Svelte actions
│       ├── useClickOutside.ts
│       └── useKeyboard.ts
```

### 2. Barrel Exports

Use barrel exports to simplify imports:

```typescript
// src/lib/components/ui/index.ts
export { Button } from './button';
export { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './card';
export { Input } from './input';
export { Label } from './label';
export { Badge } from './badge';
export { Alert, AlertDescription, AlertTitle } from './alert';
export { Tabs, TabsContent, TabsList, TabsTrigger } from './tabs';

// Export types
export type { ButtonVariants } from './button/types';
```

### 3. Constants and Configuration

Centralize configuration and constants:

```typescript
// src/lib/config/constants.ts
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    LOGOUT: '/api/auth/logout',
    REGISTER: '/api/auth/register',
    REFRESH: '/api/auth/refresh',
  },
  USER: {
    PROFILE: '/api/user/profile',
    PREFERENCES: '/api/user/preferences',
  },
} as const;

export const VALIDATION_RULES = {
  PASSWORD_MIN_LENGTH: 8,
  USERNAME_MIN_LENGTH: 3,
  MAX_UPLOAD_SIZE: 5 * 1024 * 1024, // 5MB
} as const;

export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
} as const;

export type Theme = typeof THEMES[keyof typeof THEMES];
```

## Security Patterns

### 1. Content Security Policy

Implement proper CSP headers:

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  // Add CSP headers
  response.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self' data:",
      "connect-src 'self' https://api.example.com",
    ].join('; ')
  );

  return response;
};
```

### 2. Input Sanitization

Always sanitize user inputs:

```typescript
// src/lib/utils/sanitization.ts
import DOMPurify from 'dompurify';

export function sanitizeHtml(html: string): string {
  if (typeof window === 'undefined') {
    // Server-side sanitization
    return html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/<[^>]*>/g, '');
  }

  // Client-side sanitization
  return DOMPurify.sanitize(html);
}

export function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

### 3. Rate Limiting

Implement rate limiting for API endpoints:

```typescript
// src/lib/utils/rate-limit.ts
import { RateLimiterMemory } from 'rate-limiter-flexible';

const rateLimiter = new RateLimiterMemory({
  keyPrefix: 'api_limit',
  points: 100, // Number of requests
  duration: 60, // Per 60 seconds
});

export async function rateLimit(identifier: string): Promise<boolean> {
  try {
    await rateLimiter.consume(identifier);
    return true;
  } catch {
    return false;
  }
}
```

## Monitoring and Error Handling

### 1. Error Boundaries

Implement error boundaries for graceful error handling:

```svelte
<!-- src/lib/components/ErrorBoundary.svelte -->
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
  import { AlertTriangleIcon } from 'lucide-svelte';

  interface Props {
    children: any;
    fallback?: (error: Error) => any;
  }

  let { children, fallback }: Props = $props();

  let error: Error | null = null;
  let errorInfo: string = '';

  function handleError(err: Error, info: string) {
    error = err;
    errorInfo = info;
    console.error('Error caught by boundary:', err, info);

    // Log to monitoring service
    if (typeof window !== 'undefined' && window.Sentry) {
      window.Sentry.captureException(err);
    }
  }

  function reset() {
    error = null;
    errorInfo = '';
  }
</script>

{#if error}
  {#if fallback}
    {@render fallback(error)}
  {:else}
    <Alert variant="destructive" class="m-4">
      <AlertTriangleIcon class="h-4 w-4" />
      <AlertTitle>Something went wrong</AlertTitle>
      <AlertDescription>
        An unexpected error occurred. Please try refreshing the page.
        <details class="mt-2">
          <summary>Error details</summary>
          <pre class="mt-2 text-xs bg-background p-2 rounded overflow-auto">
            {error.message}
            {errorInfo}
          </pre>
        </details>
      </AlertDescription>
    </Alert>
    <div class="p-4">
      <Button on:click={reset}>Try Again</Button>
    </div>
  {/if}
{:else}
  {@render children()}
{/if}
```

### 2. Performance Monitoring

Monitor component performance:

```typescript
// src/lib/utils/performance.ts
export function measureComponentRender<T>(
  componentName: string,
  renderFunction: () => T
): T {
  const start = performance.now();
  const result = renderFunction();
  const end = performance.now();

  // Log slow renders
  if (end - start > 16) { // More than one frame
    console.warn(`Slow render detected: ${componentName} took ${end - start}ms`);
  }

  // Send to monitoring service
  if (typeof window !== 'undefined' && window.analytics) {
    window.analytics.track('Component Render', {
      component: componentName,
      duration: end - start,
    });
  }

  return result;
}

// Usage in component
export function createPerformanceStore() {
  let measurements = $state<Record<string, number>>({});

  return {
    subscribe: measurements.subscribe,
    record: (name: string, duration: number) => {
      measurements = { ...measurements, [name]: duration };
    },
    clear: () => {
      measurements = {};
    },
  };
}

export const performanceStore = createPerformanceStore();
```

## Next Steps

Now that you understand best practices:

1. **Study examples**: Check our [examples and patterns guide](./shadcn-svelte-examples.md)
2. **Learn integration**: Review our [SvelteKit integration guide](./shadcn-svelte-integration.md)
3. **Quick start**: Use our [quick start guide](./shadcn-svelte-quickstart.md)
4. **Advanced patterns**: Explore our [component composition guide](./shadcn-svelte-composition.md)

## Additional Resources

- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn-svelte Official Docs](https://www.shadcn-svelte.com/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Performance Best Practices](https://web.dev/performance/)

---

*For more advanced patterns and examples, visit the [official shadcn-svelte documentation](https://www.shadcn-svelte.com).*