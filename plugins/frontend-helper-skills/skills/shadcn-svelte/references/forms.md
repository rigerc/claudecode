# shadcn-svelte Forms Integration

## Superforms + Formsnap Setup

### Dependencies
```bash
npm install sveltekit-superforms zod sveltekit-superforms/adapters formsnap
```

### Basic Form Implementation
```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import * as Form from "$lib/components/ui/form";
  import * as Card from "$lib/components/ui/card";
  import { Alert } from "$lib/components/ui/alert";

  // Define schema
  const schema = z.object({
    email: z.string().email({ message: "Please enter a valid email address" }),
    password: z.string().min(8, { message: "Password must be at least 8 characters" }),
    confirmPassword: z.string()
  }).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  });

  // Initialize form
  const { form, enhance, errors, message, submitting } = superForm(zodClient(schema), {
    onResult: ({ result }) => {
      if (result.type === 'success') {
        // Handle successful submission
        return { message: 'Form submitted successfully!' };
      }
    },
    onError: ({ result }) => {
      return { message: 'Submission failed. Please try again.' };
    }
  });
</script>

<Card class="w-full max-w-md mx-auto">
  <Card.Header>
    <Card.Title>Create Account</Card.Title>
    <Card.Description>
      Enter your information to create an account.
    </Card.Description>
  </Card.Header>
  <Card.Content>
    <form method="POST" use:enhance class="space-y-4">
      <!-- Email Field -->
      <Form.Field {form} name="email">
        <Form.Label>Email</Form.Label>
        <Form.Control>
          <Input
            type="email"
            placeholder="Enter your email"
            aria-invalid={$errors.email ? 'true' : undefined}
            aria-describedby={$errors.email ? 'email-error' : undefined}
          />
        </Form.Control>
        <Form.Description>
          We'll never share your email with anyone else.
        </Form.Description>
        <Form.ErrorMessage name="email" />
      </Form.Field>

      <!-- Password Field -->
      <Form.Field {form} name="password">
        <Form.Label>Password</Form.Label>
        <Form.Control>
          <Input
            type="password"
            placeholder="Enter your password"
            aria-invalid={$errors.password ? 'true' : undefined}
            aria-describedby={$errors.password ? 'password-error' : undefined}
          />
        </Form.Control>
        <Form.ErrorMessage name="password" />
      </Form.Field>

      <!-- Confirm Password Field -->
      <Form.Field {form} name="confirmPassword">
        <Form.Label>Confirm Password</Form.Label>
        <Form.Control>
          <Input
            type="password"
            placeholder="Confirm your password"
            aria-invalid={$errors.confirmPassword ? 'true' : undefined}
            aria-describedby={$errors.confirmPassword ? 'confirm-password-error' : undefined}
          />
        </Form.Control>
        <Form.ErrorMessage name="confirmPassword" />
      </Form.Field>

      <!-- Form Message -->
      {#if $message}
        <Alert variant={message.type === 'success' ? 'default' : 'destructive'}>
          <AlertDescription>{$message}</AlertDescription>
        </Alert>
      {/if}

      <!-- Submit Button -->
      <Button type="submit" class="w-full" disabled={$submitting}>
        {$submitting ? 'Creating Account...' : 'Create Account'}
      </Button>
    </form>
  </Card.Content>
</Card>
```

## Advanced Form Patterns

### Multi-Step Form
```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import * as Steps from "$lib/components/ui/steps";

  const personalInfoSchema = z.object({
    firstName: z.string().min(1, 'First name is required'),
    lastName: z.string().min(1, 'Last name is required'),
    email: z.string().email('Please enter a valid email'),
  });

  const accountSchema = z.object({
    username: z.string().min(3, 'Username must be at least 3 characters'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
  });

  const preferencesSchema = z.object({
    newsletter: z.boolean().default(true),
    notifications: z.boolean().default(true),
  });

  let currentStep = $state(1);
  const totalSteps = 3;

  const { form, enhance, errors, submitting } = superForm(zodClient(personalInfoSchema));

  const nextStep = () => {
    if (currentStep < totalSteps) {
      currentStep++;
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      currentStep--;
    }
  };
</script>

<Card class="w-full max-w-2xl mx-auto">
  <Card.Header>
    <Steps.Root current-step={currentStep} total-steps={totalSteps}>
      <Steps.Step step={1} title="Personal Info" />
      <Steps.Step step={2} title="Account Setup" />
      <Steps.Step step={3} title="Preferences" />
    </Steps.Root>
  </Card.Header>
  <Card.Content>
    <form method="POST" use:enhance>
      {#if currentStep === 1}
        <!-- Personal Information Step -->
        <div class="space-y-4">
          <Form.Field {form} name="firstName">
            <Form.Label>First Name</Form.Label>
            <Form.Control>
              <Input placeholder="John" />
            </Form.Control>
            <Form.ErrorMessage name="firstName" />
          </Form.Field>

          <Form.Field {form} name="lastName">
            <Form.Label>Last Name</Form.Label>
            <Form.Control>
              <Input placeholder="Doe" />
            </Form.Control>
            <Form.ErrorMessage name="lastName" />
          </Form.Field>

          <Form.Field {form} name="email">
            <Form.Label>Email</Form.Label>
            <Form.Control>
              <Input type="email" placeholder="john@example.com" />
            </Form.Control>
            <Form.ErrorMessage name="email" />
          </Form.Field>
        </div>
      {:else if currentStep === 2}
        <!-- Account Setup Step -->
        <div class="space-y-4">
          <Form.Field {form} name="username">
            <Form.Label>Username</Form.Label>
            <Form.Control>
              <Input placeholder="johndoe" />
            </Form.Control>
            <Form.ErrorMessage name="username" />
          </Form.Field>

          <Form.Field {form} name="password">
            <Form.Label>Password</Form.Label>
            <Form.Control>
              <Input type="password" placeholder="Enter password" />
            </Form.Control>
            <Form.ErrorMessage name="password" />
          </Form.Field>
        </div>
      {:else if currentStep === 3}
        <!-- Preferences Step -->
        <div class="space-y-4">
          <Form.Field {form} name="newsletter">
            <div class="flex items-center space-x-2">
              <Form.Control>
                <input type="checkbox" class="form-checkbox" />
              </Form.Control>
              <Form.Label>Subscribe to newsletter</Form.Label>
            </div>
            <Form.Description>
              Get updates about new features and releases.
            </Form.Description>
          </Form.Field>

          <Form.Field {form} name="notifications">
            <div class="flex items-center space-x-2">
              <Form.Control>
                <input type="checkbox" class="form-checkbox" />
              </Form.Control>
              <Form.Label>Email notifications</Form.Label>
            </div>
            <Form.Description>
              Receive important account updates via email.
            </Form.Description>
          </Form.Field>
        </div>
      {/if}

      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-6">
        <Button
          type="button"
          variant="outline"
          onclick={prevStep}
          disabled={currentStep === 1}
        >
          Previous
        </Button>

        {#if currentStep === totalSteps}
          <Button type="submit" disabled={submitting}>
            {submitting ? 'Creating Account...' : 'Complete Setup'}
          </Button>
        {:else}
          <Button type="button" onclick={nextStep}>
            Next
          </Button>
        {/if}
      </div>
    </form>
  </Card.Content>
</Card>
```

### Search Form with Filtering
```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Select } from "$lib/components/ui/select";
  import * as Form from "$lib/components/ui/form";
  import * as Card from "$lib/components/ui/card";

  const searchSchema = z.object({
    query: z.string().optional(),
    category: z.string().optional(),
    status: z.enum(['all', 'active', 'inactive']).default('all'),
    sortBy: z.enum(['name', 'created', 'updated']).default('name'),
    order: z.enum(['asc', 'desc']).default('asc'),
  });

  const { form, enhance, errors } = superForm(zodClient(searchSchema), {
    resetForm: false, // Keep form values after submission
    onResult: ({ result }) => {
      // Handle search results
      console.log('Search results:', result.data);
    }
  });

  let searchResults = $state([]);
  let isSearching = $state(false);
</script>

<Card class="w-full max-w-4xl mx-auto">
  <Card.Header>
    <Card.Title>Advanced Search</Card.Title>
    <Card.Description>
      Search and filter through your data.
    </Card.Description>
  </Card.Header>
  <Card.Content>
    <form method="GET" use:enhance class="space-y-4">
      <!-- Search Query -->
      <Form.Field {form} name="query">
        <Form.Label>Search</Form.Label>
        <Form.Control>
          <Input
            type="search"
            placeholder="Search by name, description, or keywords..."
          />
        </Form.Control>
      </Form.Field>

      <!-- Filters Row -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Form.Field {form} name="category">
          <Form.Label>Category</Form.Label>
          <Form.Control>
            <Select>
              <Select.Trigger>
                <Select.Value placeholder="All categories" />
              </Select.Trigger>
              <Select.Content>
                <Select.Item value="">All categories</Select.Item>
                <Select.Item value="development">Development</Select.Item>
                <Select.Item value="design">Design</Select.Item>
                <Select.Item value="marketing">Marketing</Select.Item>
                <Select.Item value="sales">Sales</Select.Item>
              </Select.Content>
            </Select>
          </Form.Control>
        </Form.Field>

        <Form.Field {form} name="status">
          <Form.Label>Status</Form.Label>
          <Form.Control>
            <Select>
              <Select.Trigger>
                <Select.Value placeholder="All status" />
              </Select.Trigger>
              <Select.Content>
                <Select.Item value="all">All status</Select.Item>
                <Select.Item value="active">Active</Select.Item>
                <Select.Item value="inactive">Inactive</Select.Item>
              </Select.Content>
            </Select>
          </Form.Control>
        </Form.Field>

        <Form.Field {form} name="sortBy">
          <Form.Label>Sort by</Form.Label>
          <Form.Control>
            <Select>
              <Select.Trigger>
                <Select.Value placeholder="Sort by" />
              </Select.Trigger>
              <Select.Content>
                <Select.Item value="name">Name</Select.Item>
                <Select.Item value="created">Created date</Select.Item>
                <Select.Item value="updated">Updated date</Select.Item>
              </Select.Content>
            </Select>
          </Form.Control>
        </Form.Field>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2">
        <Button type="submit" disabled={isSearching}>
          {#if isSearching}
            Searching...
          {:else}
            Search
          {/if}
        </Button>

        <Button
          type="button"
          variant="outline"
          onclick={() => {
            form.reset();
            searchResults = [];
          }}
        >
          Clear
        </Button>
      </div>
    </form>
  </Card.Content>

  <!-- Search Results -->
  {#if searchResults.length > 0}
    <div class="mt-6 border-t pt-6">
      <Card.Title class="text-lg">Results ({searchResults.length})</Card.Title>
      <div class="mt-4 space-y-2">
        {#each searchResults as result}
          <div class="p-4 border rounded-lg hover:bg-accent">
            <h3 class="font-medium">{result.name}</h3>
            <p class="text-sm text-muted-foreground">{result.description}</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</Card>
```

## Form Validation Patterns

### Custom Validation
```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  const customSchema = z.object({
    age: z.number()
      .min(18, 'You must be at least 18 years old')
      .max(120, 'Please enter a valid age'),
    website: z.string().url('Please enter a valid URL').optional().or(z.literal('')),
    phone: z.string().regex(/^\+?[\d\s\-\(\)]+$/, 'Please enter a valid phone number'),
    customField: z.string().refine((value) => {
      // Custom validation logic
      return value.startsWith('CUSTOM_');
    }, {
      message: 'Field must start with "CUSTOM_"'
    })
  });

  const { form, enhance, errors } = superForm(zodClient(customSchema));
</script>
```

### Conditional Validation
```svelte
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import { z } from 'zod';

  let accountType = $state('personal');

  const schema = $derived(
    z.object({
      accountType: z.enum(['personal', 'business']),
      firstName: z.string().min(1, 'First name is required'),
      companyName: z.string().optional(),
      taxId: z.string().optional(),
    }).refine((data) => {
      if (data.accountType === 'business') {
        return !!data.companyName && !!data.taxId;
      }
      return true;
    }, {
      message: "Company name and Tax ID are required for business accounts",
      path: ['companyName']
    })
  );

  const { form, enhance, errors } = superForm(zodClient(schema));
</script>

<form method="POST" use:enhance>
  <Form.Field {form} name="accountType">
    <Form.Label>Account Type</Form.Label>
    <Form.Control>
      <select bind:value={$form.accountType}>
        <option value="personal">Personal</option>
        <option value="business">Business</option>
      </select>
    </Form.Control>
  </Form.Field>

  <Form.Field {form} name="firstName">
    <Form.Label>First Name</Form.Label>
    <Form.Control>
      <Input placeholder="Enter your first name" />
    </Form.Control>
    <Form.ErrorMessage name="firstName" />
  </Form.Field>

  {#if $form.accountType === 'business'}
    <Form.Field {form} name="companyName">
      <Form.Label>Company Name</Form.Label>
      <Form.Control>
        <Input placeholder="Enter company name" />
      </Form.Control>
      <Form.ErrorMessage name="companyName" />
    </Form.Field>

    <Form.Field {form} name="taxId">
      <Form.Label>Tax ID</Form.Label>
      <Form.Control>
        <Input placeholder="Enter tax ID" />
      </Form.Control>
      <Form.ErrorMessage name="taxId" />
    </Form.Field>
  {/if}

  <Button type="submit">Submit</Button>
</form>
```

## Accessibility Best Practices

### Form Labels and Descriptions
```svelte
<!-- Good: Proper labeling -->
<Form.Field {form} name="email">
  <Form.Label for="email-input">Email Address</Form.Label>
  <Form.Description id="email-description">
    We'll never share your email with anyone else.
  </Form.Description>
  <Form.Control>
    <Input
      id="email-input"
      type="email"
      placeholder="Enter your email"
      aria-describedby="email-description"
      aria-invalid={$errors.email ? 'true' : undefined}
    />
  </Form.Control>
  <Form.ErrorMessage name="email" />
</Form.Field>

<!-- Bad: Missing proper labeling -->
<div>
  <label>Email</label>
  <input type="email" placeholder="Enter your email" />
</div>
```

### Error Handling
```svelte
<script lang="ts">
  // Ensure errors are properly announced to screen readers
  $: hasErrors = Object.keys($errors).length > 0;
</script>

<!-- Announce errors to screen readers -->
{#if hasErrors}
  <div role="alert" aria-live="polite" class="sr-only">
    Form has validation errors. Please review and correct the highlighted fields.
  </div>
{/if}

<!-- Visual error indicators with proper ARIA -->
<Form.Field {form} name="email">
  <Form.Label>Email</Form.Label>
  <Form.Control>
    <Input
      aria-invalid={$errors.email ? 'true' : undefined}
      aria-describedby={$errors.email ? 'email-error' : undefined}
      class={$errors.email ? 'border-destructive focus:ring-destructive' : ''}
    />
  </Form.Control>
  {#if $errors.email}
    <Form.ErrorMessage name="email" id="email-error" />
  {/if}
</Form.Field>
```

### Keyboard Navigation
```svelte
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function handleKeydown(event: KeyboardEvent) {
    // Handle form keyboard shortcuts
    if (event.key === 'Enter' && event.ctrlKey) {
      dispatch('submit');
    } else if (event.key === 'Escape') {
      dispatch('cancel');
    }
  }
</script>

<form on:keydown={handleKeydown}>
  <!-- Form content -->
</form>
```

## Testing Forms

### Unit Testing with Vitest
```typescript
// src/lib/components/forms/UserForm.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import { superForm } from 'sveltekit-superforms';
import UserForm from './UserForm.svelte';

// Mock superForm
vi.mock('sveltekit-superforms', () => ({
  superForm: vi.fn(() => ({
    form: {
      subscribe: vi.fn().mockReturnValue({ email: '', password: '' })
    },
    enhance: vi.fn(),
    errors: { subscribe: vi.fn().mockReturnValue({}) }
  }))
}));

describe('UserForm', () => {
  it('renders form fields correctly', () => {
    render(UserForm);

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('shows validation errors for invalid input', async () => {
    render(UserForm);

    const emailInput = screen.getByLabelText('Email');
    const submitButton = screen.getByRole('button', { name: 'Submit' });

    // Submit empty form
    fireEvent.click(submitButton);

    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
    });
  });

  it('handles successful submission', async () => {
    const mockSubmit = vi.fn();

    render(UserForm, {
      props: {
        onSubmit: mockSubmit
      }
    });

    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: 'Submit' });

    // Fill form
    await fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.change(passwordInput, { target: { value: 'password123' } });

    // Submit form
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });
});
```

### E2E Testing with Playwright
```typescript
// tests/e2e/user-form.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Registration Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
  });

  test('should register a new user successfully', async ({ page }) => {
    // Fill out the registration form
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'securePassword123');
    await page.fill('[data-testid="confirm-password-input"]', 'securePassword123');

    // Submit the form
    await page.click('[data-testid="submit-button"]');

    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Account created successfully');
  });

  test('should show validation errors for invalid email', async ({ page }) => {
    // Fill form with invalid email
    await page.fill('[data-testid="email-input"]', 'invalid-email');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');

    // Submit the form
    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Please enter a valid email');
  });

  test('should support keyboard navigation', async ({ page }) => {
    // Navigate form using keyboard
    await page.keyboard.press('Tab'); // Focus email input
    await expect(page.locator('[data-testid="email-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus password input
    await expect(page.locator('[data-testid="password-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus confirm password input
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus submit button
    await expect(page.locator('[data-testid="submit-button"]')).toBeFocused();
  });
});
```