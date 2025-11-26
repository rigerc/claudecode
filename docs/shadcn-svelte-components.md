# Component Usage Guide

This comprehensive guide covers how to use shadcn-svelte components effectively in your Svelte applications. Learn about component patterns, props, styling, and best practices for building modern UIs.

## Understanding Component Structure

Every shadcn-svelte component follows a consistent structure:

```
src/lib/components/ui/[component]/
├── index.ts          # Barrel exports
├── [Component].svelte # Main component file
└── types.ts          # TypeScript definitions (optional)
```

### Import Patterns

#### Individual Component Import

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card } from '$lib/components/ui/card';
</script>
```

#### Multiple Components from UI Directory

```svelte
<script lang="ts">
  import { Button, Card, Input, Label } from '$lib/components/ui';
</script>
```

## Core Components

### Button Component

The Button component is one of the most versatile and commonly used components.

#### Basic Usage

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<Button>Click me</Button>
```

#### Variants

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<div class="flex gap-2">
  <Button>Default</Button>
  <Button variant="secondary">Secondary</Button>
  <Button variant="destructive">Destructive</Button>
  <Button variant="outline">Outline</Button>
  <Button variant="ghost">Ghost</Button>
  <Button variant="link">Link</Button>
</div>
```

#### Sizes

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<div class="flex gap-2 items-center">
  <Button size="sm">Small</Button>
  <Button size="default">Default</Button>
  <Button size="lg">Large</Button>
  <Button size="icon">
    <StarIcon class="h-4 w-4" />
  </Button>
</div>

<script lang="ts">
  import { StarIcon } from 'lucide-svelte';
</script>
```

#### With Icons

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { PlusIcon, TrashIcon, DownloadIcon } from 'lucide-svelte';
</script>

<div class="flex gap-2">
  <Button>
    <PlusIcon class="mr-2 h-4 w-4" />
    Add Item
  </Button>

  <Button variant="outline">
    <DownloadIcon class="mr-2 h-4 w-4" />
    Download
  </Button>

  <Button variant="destructive" size="icon">
    <TrashIcon class="h-4 w-4" />
  </Button>
</div>
```

#### Event Handling

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';

  function handleClick() {
    console.log('Button clicked!');
  }

  function handleCustomEvent(event: MouseEvent) {
    console.log('Custom event data:', event.detail);
  }
</script>

<div class="flex gap-2">
  <Button on:click={handleClick}>
    Click Handler
  </Button>

  <Button on:click={(e) => console.log('Inline handler', e)}>
    Inline Handler
  </Button>

  <Button disabled>
    Disabled Button
  </Button>
</div>
```

### Input Components

#### Text Input

```svelte
<script lang="ts">
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';

  let value = '';
</script>

<div class="grid w-full max-w-sm items-center gap-1.5">
  <Label for="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="Email"
    bind:value
  />
</div>
```

#### Form Validation

```svelte
<script lang="ts">
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';

  let email = '';
  let emailError = '';

  function validateEmail() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      emailError = 'Please enter a valid email address';
    } else {
      emailError = '';
    }
  }
</script>

<div class="grid w-full max-w-sm items-center gap-1.5">
  <Label for="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="Email"
    bind:value
    on:blur={validateEmail}
    class={emailError ? 'border-red-500' : ''}
  />
  {#if emailError}
    <p class="text-sm text-red-500">{emailError}</p>
  {/if}
</div>
```

#### Select Component

```svelte
<script lang="ts">
  import { Select } from '$lib/components/ui/select';

  let selectedValue = '';
</script>

<Select bind:value={selectedValue}>
  <Select.Trigger class="w-[180px]">
    <Select.Value placeholder="Select a fruit" />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="apple">Apple</Select.Item>
    <Select.Item value="banana">Banana</Select.Item>
    <Select.Item value="blueberry">Blueberry</Select.Item>
    <Select.Item value="grapes">Grapes</Select.Item>
    <Select.Item value="pineapple">Pineapple</Select.Item>
  </Select.Content>
</Select>

<p>Selected: {selectedValue}</p>
```

#### Checkbox and Radio

```svelte
<script lang="ts">
  import { Checkbox } from '$lib/components/ui/checkbox';
  import { RadioGroup, RadioGroupItem } from '$lib/components/ui/radio-group';

  let checked = false;
  let selectedFruit = '';
</script>

<!-- Checkbox -->
<div class="flex items-center space-x-2">
  <Checkbox id="terms" bind:checked />
  <label for="terms" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
    Accept terms and conditions
  </label>
</div>

<!-- Radio Group -->
<RadioGroup bind:value={selectedFruit}>
  <div class="flex items-center space-x-2">
    <RadioGroupItem value="apple" id="r1" />
    <label for="r1">Apple</label>
  </div>
  <div class="flex items-center space-x-2">
    <RadioGroupItem value="orange" id="r2" />
    <label for="r2">Orange</label>
  </div>
  <div class="flex items-center space-x-2">
    <RadioGroupItem value="peach" id="r3" />
    <label for="r3">Peach</label>
  </div>
</RadioGroup>
```

### Card Component

The Card component is perfect for grouping related content.

```svelte
<script lang="ts">
  import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Button } from '$lib/components/ui/button';
  import { Badge } from '$lib/components/ui/badge';
</script>

<Card class="w-[350px]">
  <CardHeader>
    <CardTitle>Create project</CardTitle>
    <CardDescription>Deploy your new project in one-click.</CardDescription>
  </CardHeader>
  <CardContent>
    <form>
      <div class="grid w-full items-center gap-4">
        <div class="flex flex-col space-y-1.5">
          <label for="name">Name</label>
          <Input id="name" placeholder="Name of your project" />
        </div>
        <div class="flex flex-col space-y-1.5">
          <label for="framework">Framework</label>
          <Select>
            <Select.Trigger>
              <Select.Value placeholder="Select" />
            </Select.Trigger>
            <Select.Content>
              <Select.Item value="next">Next.js</Select.Item>
              <Select.Item value="sveltekit">SvelteKit</Select.Item>
              <Select.Item value="astro">Astro</Select.Item>
              <Select.Item value="nuxt">Nuxt.js</Select.Item>
            </Select.Content>
          </Select>
        </div>
      </div>
    </form>
  </CardContent>
  <CardFooter class="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Deploy</Button>
  </CardFooter>
</Card>
```

### Dialog Component

Dialogs are great for modals, forms, and confirmations.

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';

  let open = false;
  let projectName = '';
</script>

<Dialog bind:open>
  <DialogTrigger asChild>
    <Button variant="outline">Edit Profile</Button>
  </DialogTrigger>
  <DialogContent class="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here. Click save when you're done.
      </DialogDescription>
    </DialogHeader>
    <div class="grid gap-4 py-4">
      <div class="grid grid-cols-4 items-center gap-4">
        <Label for="name" class="text-right">
          Name
        </Label>
        <Input
          id="name"
          placeholder="John Doe"
          class="col-span-3"
          bind:value={projectName}
        />
      </div>
      <div class="grid grid-cols-4 items-center gap-4">
        <Label for="username" class="text-right">
          Username
        </Label>
        <Input
          id="username"
          placeholder="@johndoe"
          class="col-span-3"
        />
      </div>
    </div>
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Alert Component

Alerts are perfect for notifications and important messages.

```svelte
<script lang="ts">
  import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
  import { TerminalIcon, AlertTriangleIcon, InfoIcon } from 'lucide-svelte';
</script>

<!-- Default Alert -->
<Alert>
  <TerminalIcon class="h-4 w-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components to your app using the cli.
  </AlertDescription>
</Alert>

<!-- Destructive Alert -->
<Alert variant="destructive">
  <AlertTriangleIcon class="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Your session has expired. Please log in again.
  </AlertDescription>
</Alert>
```

### Table Component

Tables for displaying structured data.

```svelte
<script lang="ts">
  import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '$lib/components/ui/table';
  import { Badge } from '$lib/components/ui/badge';

  const invoices = [
    {
      invoice: "INV001",
      paymentStatus: "Paid",
      totalAmount: "$250.00",
      paymentMethod: "Credit Card",
    },
    {
      invoice: "INV002",
      paymentStatus: "Pending",
      totalAmount: "$150.00",
      paymentMethod: "PayPal",
    },
    {
      invoice: "INV003",
      paymentStatus: "Unpaid",
      totalAmount: "$350.00",
      paymentMethod: "Bank Transfer",
    },
  ];
</script>

<Table>
  <TableHeader>
    <TableRow>
      <TableHead class="w-[100px]">Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead class="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {#each invoices as invoice (invoice.invoice)}
      <TableRow>
        <TableCell class="font-medium">{invoice.invoice}</TableCell>
        <TableCell>
          <Badge variant={invoice.paymentStatus === 'Paid' ? 'default' : 'secondary'}>
            {invoice.paymentStatus}
          </Badge>
        </TableCell>
        <TableCell>{invoice.paymentMethod}</TableCell>
        <TableCell class="text-right">{invoice.totalAmount}</TableCell>
      </TableRow>
    {/each}
  </TableBody>
</Table>
```

## Layout Components

### Tabs Component

Tabs for organizing content sections.

```svelte
<script lang="ts">
  import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
</script>

<Tabs defaultValue="account" class="w-[400px]">
  <TabsList class="grid w-full grid-cols-2">
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">
    <div class="space-y-4">
      <h3 class="text-lg font-semibold">Account Settings</h3>
      <p class="text-sm text-muted-foreground">
        Make changes to your account here. Click save when you're done.
      </p>
      <!-- Account form content -->
    </div>
  </TabsContent>
  <TabsContent value="password">
    <div class="space-y-4">
      <h3 class="text-lg font-semibold">Password</h3>
      <p class="text-sm text-muted-foreground">
        Change your password here. After saving, you'll be logged out.
      </p>
      <!-- Password form content -->
    </div>
  </TabsContent>
</Tabs>
```

### Separator Component

Visual separators for content organization.

```svelte
<script lang="ts">
  import { Separator } from '$lib/components/ui/separator';
</script>

<div class="space-y-1">
  <h4 class="text-sm font-medium leading-none">SvelteKit</h4>
  <p class="text-sm text-muted-foreground">
    The fastest way to build svelte apps.
  </p>
</div>
<Separator />
<div class="space-y-1">
  <h4 class="text-sm font-medium leading-none">shadcn-svelte</h4>
  <p class="text-sm text-muted-foreground">
    Beautifully designed components that you can copy and paste into your apps.
  </p>
</div>
```

## Advanced Usage Patterns

### Combining Components

Create complex UIs by combining multiple components:

```svelte
<script lang="ts">
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Button } from '$lib/components/ui/button';
  import { Badge } from '$lib/components/ui/badge';
  import { Progress } from '$lib/components/ui/progress';
  import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';

  let progress = 65;
</script>

<Card class="w-full max-w-md">
  <CardHeader>
    <div class="flex items-center justify-between">
      <div>
        <CardTitle>Project Dashboard</CardTitle>
        <CardDescription>Track your progress and tasks</CardDescription>
      </div>
      <Badge variant="secondary">Active</Badge>
    </div>
  </CardHeader>
  <CardContent>
    <Tabs defaultValue="overview" class="w-full">
      <TabsList class="grid w-full grid-cols-2">
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="tasks">Tasks</TabsTrigger>
      </TabsList>

      <TabsContent value="overview" class="space-y-4">
        <div>
          <div class="flex justify-between text-sm mb-2">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <Progress value={progress} />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <p class="text-sm font-medium">Tasks</p>
            <p class="text-2xl font-bold">24</p>
          </div>
          <div class="space-y-2">
            <p class="text-sm font-medium">Completed</p>
            <p class="text-2xl font-bold">18</p>
          </div>
        </div>
      </TabsContent>

      <TabsContent value="tasks" class="space-y-2">
        <div class="space-y-2">
          <div class="flex items-center justify-between p-2 border rounded">
            <span class="text-sm">Design homepage</span>
            <Badge variant="outline">In Progress</Badge>
          </div>
          <div class="flex items-center justify-between p-2 border rounded">
            <span class="text-sm">Setup database</span>
            <Badge variant="default">Completed</Badge>
          </div>
          <div class="flex items-center justify-between p-2 border rounded">
            <span class="text-sm">User authentication</span>
            <Badge variant="destructive">Blocked</Badge>
          </div>
        </div>
      </TabsContent>
    </Tabs>

    <div class="flex gap-2 mt-6">
      <Button class="flex-1">View Details</Button>
      <Button variant="outline">Export</Button>
    </div>
  </CardContent>
</Card>
```

### Form Patterns

Create complex forms with validation:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '$lib/components/ui/select';
  import { Textarea } from '$lib/components/ui/textarea';
  import { Checkbox } from '$lib/components/ui/checkbox';

  let formData = {
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    message: '',
    newsletter: false,
    plan: ''
  };

  let errors: Record<string, string> = {};

  function validateForm() {
    errors = {};

    if (!formData.firstName.trim()) {
      errors.firstName = 'First name is required';
    }

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Please enter a valid email';
    }

    if (!formData.plan) {
      errors.plan = 'Please select a plan';
    }

    return Object.keys(errors).length === 0;
  }

  function handleSubmit() {
    if (validateForm()) {
      console.log('Form submitted:', formData);
      // Handle form submission
    }
  }
</script>

<Card class="w-full max-w-2xl mx-auto">
  <CardHeader>
    <CardTitle>Contact Form</CardTitle>
    <CardDescription>
      Send us a message and we'll get back to you as soon as possible.
    </CardDescription>
  </CardHeader>
  <CardContent class="space-y-4">
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <Label for="firstName">First Name</Label>
          <Input
            id="firstName"
            placeholder="John"
            bind:value={formData.firstName}
            class={errors.firstName ? 'border-red-500' : ''}
          />
          {#if errors.firstName}
            <p class="text-sm text-red-500">{errors.firstName}</p>
          {/if}
        </div>

        <div class="space-y-2">
          <Label for="lastName">Last Name</Label>
          <Input
            id="lastName"
            placeholder="Doe"
            bind:value={formData.lastName}
          />
        </div>
      </div>

      <div class="space-y-2">
        <Label for="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="john@example.com"
          bind:value={formData.email}
          class={errors.email ? 'border-red-500' : ''}
        />
        {#if errors.email}
          <p class="text-sm text-red-500">{errors.email}</p>
        {/if}
      </div>

      <div class="space-y-2">
        <Label for="company">Company</Label>
        <Input
          id="company"
          placeholder="Acme Inc."
          bind:value={formData.company}
        />
      </div>

      <div class="space-y-2">
        <Label for="plan">Plan</Label>
        <Select bind:value={formData.plan}>
          <SelectTrigger class={errors.plan ? 'border-red-500' : ''}>
            <SelectValue placeholder="Select a plan" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="free">Free Plan</SelectItem>
            <SelectItem value="pro">Pro Plan</SelectItem>
            <SelectItem value="enterprise">Enterprise Plan</SelectItem>
          </SelectContent>
        </Select>
        {#if errors.plan}
          <p class="text-sm text-red-500">{errors.plan}</p>
        {/if}
      </div>

      <div class="space-y-2">
        <Label for="message">Message</Label>
        <Textarea
          id="message"
          placeholder="Your message here..."
          bind:value={formData.message}
          rows={4}
        />
      </div>

      <div class="flex items-center space-x-2">
        <Checkbox id="newsletter" bind:checked={formData.newsletter} />
        <Label for="newsletter" class="text-sm font-normal">
          Subscribe to our newsletter for updates and tips.
        </Label>
      </div>

      <div class="flex gap-2 pt-4">
        <Button type="submit" class="flex-1">Send Message</Button>
        <Button type="button" variant="outline">Cancel</Button>
      </div>
    </form>
  </CardContent>
</Card>
```

## Styling with Tailwind CSS

### Custom Styling

Add custom Tailwind classes to components:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
</script>

<!-- Custom button with additional Tailwind classes -->
<Button
  class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-2 px-6 rounded-full shadow-lg"
>
  Custom Styled Button
</Button>

<!-- Responsive design -->
<Button class="w-full sm:w-auto">
  Responsive Button
</Button>

<!-- Animation classes -->
<Button class="transition-all duration-300 hover:scale-105">
  Animated Button
</Button>
```

### Conditional Styling

Use Svelte's reactivity for conditional styling:

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';

  let isLoading = false;
  let isDisabled = false;

  async function handleClick() {
    isLoading = true;
    isDisabled = true;

    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 2000));

    isLoading = false;
    isDisabled = false;
  }
</script>

<Button
  on:click={handleClick}
  disabled={isDisabled}
  class="relative"
>
  {#if isLoading}
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
    </div>
  {/if}

  <span class={isLoading ? 'opacity-0' : ''}>
    {isLoading ? 'Loading...' : 'Submit'}
  </span>
</Button>
```

## Component States

### Loading States

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';

  let loading = false;
</script>

<Card class="w-[300px]">
  <CardHeader>
    <CardTitle>Component States</CardTitle>
  </CardHeader>
  <CardContent class="space-y-4">
    <Button
      on:click={() => loading = !loading}
      class="w-full"
    >
      Toggle Loading
    </Button>

    <div class="space-y-2">
      <p class="text-sm font-medium">Current State:</p>
      <div class="p-3 border rounded">
        {#if loading}
          <div class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
            <span class="text-sm">Loading...</span>
          </div>
        {:else}
          <span class="text-sm text-muted-foreground">Ready</span>
        {/if}
      </div>
    </div>
  </CardContent>
</Card>
```

### Error States

```svelte
<script lang="ts">
  import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
  import { Button } from '$lib/components/ui/button';
  import { AlertCircleIcon } from 'lucide-svelte';

  let hasError = false;
  let errorMessage = '';

  async function riskyOperation() {
    try {
      hasError = false;
      // Simulate potential error
      if (Math.random() > 0.5) {
        throw new Error('Something went wrong!');
      }
      // Success case
    } catch (error) {
      hasError = true;
      errorMessage = error instanceof Error ? error.message : 'Unknown error';
    }
  }
</script>

<div class="space-y-4">
  <Button on:click={riskyOperation}>
    Perform Risky Operation
  </Button>

  {#if hasError}
    <Alert variant="destructive">
      <AlertCircleIcon class="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <AlertDescription>{errorMessage}</AlertDescription>
    </Alert>
  {/if}
</div>
```

## Accessibility Best Practices

### ARIA Labels

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
</script>

<!-- Button with accessibility attributes -->
<Button
  aria-label="Close dialog"
  on:click={() => console.log('Closing dialog')}
>
  ×
</Button>

<!-- Input with proper labeling -->
<Input
  id="search"
  type="search"
  placeholder="Search..."
  aria-describedby="search-description"
  required
/>
<p id="search-description" class="sr-only">
  Search through available items by typing keywords
</p>
```

### Keyboard Navigation

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';

  let focusedIndex = 0;
  const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];

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
        event.preventDefault();
        console.log('Selected:', items[focusedIndex]);
        break;
    }
  }
</script>

<div
  class="border rounded p-2"
  tabindex="0"
  on:keydown={handleKeydown}
  role="listbox"
  aria-label="Selectable items"
>
  {#each items as item, index}
    <div
      class="p-2 rounded cursor-pointer"
      class:bg-primary={focusedIndex === index}
      class:text-primary-foreground={focusedIndex === index}
      role="option"
      aria-selected={focusedIndex === index}
    >
      {item}
    </div>
  {/each}
</div>
```

## Performance Tips

### Lazy Loading Components

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';

  let showHeavyComponent = false;

  // Lazy load heavy component
  const HeavyComponent = showHeavyComponent
    ? () => import('$lib/components/heavy-component.svelte')
    : null;
</script>

<Button on:click={() => showHeavyComponent = true}>
  Load Heavy Component
</Button>

{#if showHeavyComponent && HeavyComponent}
  <svelte:component this={HeavyComponent} />
{/if}
```

### Memoization

```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';

  let filterText = '';
  const items = Array.from({ length: 1000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`,
    value: Math.random() * 100
  }));

  // Memoize filtered items
  $: filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(filterText.toLowerCase())
  );
</script>

<div class="space-y-4">
  <Input
    placeholder="Filter items..."
    bind:value={filterText}
  />

  <div class="max-h-64 overflow-y-auto border rounded">
    {#each filteredItems as item (item.id)}
      <div class="p-2 border-b">
        {item.name} - {item.value.toFixed(2)}
      </div>
    {/each}
  </div>
</div>
```

## Testing Components

### Unit Testing Example

```svelte
<!-- Button.test.svelte -->
<script lang="ts">
  import { render, fireEvent } from '@testing-library/svelte';
  import { Button } from '$lib/components/ui/button';

  test('Button renders correctly', () => {
    const { getByText } = render(Button, {
      props: { children: 'Click me' }
    });

    expect(getByText('Click me')).toBeInTheDocument();
  });

  test('Button handles click events', async () => {
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
</script>
```

## Next Steps

Now that you understand how to use shadcn-svelte components:

1. **Explore more components**: Check the [official component documentation](https://www.shadcn-svelte.com/docs/components)
2. **Learn customization**: Read our [customization guide](./shadcn-svelte-customization.md)
3. **Study best practices**: Review our [best practices guide](./shadcn-svelte-best-practices.md)
4. **Build examples**: See our [examples and patterns guide](./shadcn-svelte-examples.md)

---

*For component-specific documentation and API reference, visit the [official shadcn-svelte documentation](https://www.shadcn-svelte.com).*