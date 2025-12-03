# shadcn-svelte Testing Guide

## Unit Testing with Vitest

### Setup
```bash
npm install -D vitest @testing-library/svelte @testing-library/jest-dom jsdom
```

### Vitest Configuration
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true
  }
});
```

### Test Setup
```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { beforeAll, afterAll } from 'vitest';

// Mock window.matchMedia for dark mode tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

### Component Testing Examples

#### Button Component Test
```typescript
// src/lib/components/ui/button/Button.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button.svelte';

describe('Button', () => {
  it('renders with default props', () => {
    render(Button, {
      children: 'Click me'
    });

    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-primary', 'text-primary-foreground');
  });

  it('applies variant classes correctly', () => {
    const { rerender } = render(Button, {
      variant: 'destructive',
      children: 'Delete'
    });

    let button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');

    rerender({ variant: 'outline', children: 'Cancel' });
    button = screen.getByRole('button');
    expect(button).toHaveClass('border');
  });

  it('applies size classes correctly', () => {
    const { rerender } = render(Button, {
      size: 'sm',
      children: 'Small'
    });

    let button = screen.getByRole('button');
    expect(button).toHaveClass('h-9');

    rerender({ size: 'lg', children: 'Large' });
    button = screen.getByRole('button');
    expect(button).toHaveClass('h-11');
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(Button, {
      children: 'Click me',
      onclick: handleClick
    });

    const button = screen.getByRole('button');
    await user.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('supports keyboard navigation', async () => {
    const handleClick = vi.fn();
    render(Button, {
      children: 'Click me',
      onclick: handleClick
    });

    const button = screen.getByRole('button');

    // Enter key
    await fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalledTimes(1);

    // Space key
    await fireEvent.keyDown(button, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  it('can be disabled', () => {
    render(Button, {
      children: 'Disabled',
      disabled: true
    });

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-disabled', 'true');
  });

  it('supports custom CSS classes', () => {
    render(Button, {
      children: 'Custom',
      class: 'custom-class another-class'
    });

    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-class', 'another-class');
  });

  it('renders as different HTML elements', () => {
    render(Button, {
      children: 'Link',
      asChild: true
    }, {
      target: document.body,
      props: {
        $$slots: {
          default: () => '<a href="/test">Link</a>'
        }
      }
    });

    const link = screen.getByRole('link');
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', '/test');
  });
});
```

#### Card Component Test
```typescript
// src/lib/components/ui/card/Card.test.ts
import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import * as Card from './index.js';

describe('Card', () => {
  it('renders complete card structure', () => {
    render(Card.Root, {}, {
      $$slots: {
        default: `
          ${Card.Header}
            ${Card.Title}Card Title${/Card.Title}
            ${Card.Description}Card description${/Card.Description}
          ${/Card.Header}
          ${Card.Content}
            <p>Card content here</p>
          ${/Card.Content}
          ${Card.Footer}
            <button>Action</button>
          ${/Card.Footer}
        `
      }
    });

    expect(screen.getByText('Card Title')).toBeInTheDocument();
    expect(screen.getByText('Card description')).toBeInTheDocument();
    expect(screen.getByText('Card content here')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Action' })).toBeInTheDocument();
  });

  it('applies correct CSS classes', () => {
    render(Card.Root);

    const card = screen.getByRole('article');
    expect(card).toHaveClass('bg-card', 'text-card-foreground', 'rounded-lg', 'shadow-sm', 'border');
  });

  it('supports custom classes', () => {
    render(Card.Root, {
      class: 'custom-card'
    });

    const card = screen.getByRole('article');
    expect(card).toHaveClass('custom-card');
  });
});
```

#### Input Component Test
```typescript
// src/lib/components/ui/input/Input.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Input from './Input.svelte';

describe('Input', () => {
  it('renders with basic props', () => {
    render(Input, {
      type: 'text',
      placeholder: 'Enter text'
    });

    const input = screen.getByPlaceholderText('Enter text');
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('type', 'text');
  });

  it('handles value changes', async () => {
    let value = '';
    const user = userEvent.setup();

    render(Input, {
      type: 'text',
      placeholder: 'Enter text',
      bind:value
    });

    const input = screen.getByPlaceholderText('Enter text');
    await user.type(input, 'Hello World');

    expect(value).toBe('Hello World');
  });

  it('supports validation states', () => {
    render(Input, {
      type: 'email',
      placeholder: 'Enter email',
      'aria-invalid': 'true',
      'aria-describedby': 'email-error'
    });

    const input = screen.getByPlaceholderText('Enter email');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby', 'email-error');
  });

  it('handles keyboard events', async () => {
    const handleKeydown = vi.fn();
    render(Input, {
      type: 'text',
      placeholder: 'Type here',
      onkeydown: handleKeydown
    });

    const input = screen.getByPlaceholderText('Type here');
    await fireEvent.keyDown(input, { key: 'Enter' });

    expect(handleKeydown).toHaveBeenCalledWith(
      expect.objectContaining({ key: 'Enter' })
    );
  });

  it('can be disabled', () => {
    render(Input, {
      type: 'text',
      placeholder: 'Disabled input',
      disabled: true
    });

    const input = screen.getByPlaceholderText('Disabled input');
    expect(input).toBeDisabled();
  });
});
```

### Form Testing Examples

#### Form Integration Test
```typescript
// src/lib/components/forms/UserForm.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { superForm } from 'sveltekit-superforms';
import UserForm from './UserForm.svelte';

// Mock superForm
vi.mock('sveltekit-superforms', () => ({
  superForm: vi.fn(() => ({
    form: {
      subscribe: vi.fn().mockReturnValue({
        email: '',
        password: '',
        errors: { email: '', password: '' }
      })
    },
    enhance: vi.fn(),
    errors: {
      subscribe: vi.fn().mockReturnValue({})
    },
    submitting: {
      subscribe: vi.fn().mockReturnValue(false)
    }
  }))
}));

describe('UserForm', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(UserForm);

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('shows validation errors for empty fields', async () => {
    const mockEnhance = vi.fn();
    vi.mocked(superForm).mockReturnValue({
      form: {
        subscribe: vi.fn().mockReturnValue({
          email: '',
          password: '',
          errors: { email: 'Email is required', password: 'Password is required' }
        })
      },
      enhance: mockEnhance,
      errors: {
        subscribe: vi.fn().mockReturnValue({
          email: 'Email is required',
          password: 'Password is required'
        })
      },
      submitting: {
        subscribe: vi.fn().mockReturnValue(false)
      }
    });

    render(UserForm);

    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
      expect(screen.getByText('Password is required')).toBeInTheDocument();
    });
  });

  it('handles form submission successfully', async () => {
    const user = userEvent.setup();
    let submittedData = null;

    vi.mocked(superForm).mockReturnValue({
      form: {
        subscribe: vi.fn().mockReturnValue({
          email: 'test@example.com',
          password: 'password123',
          errors: { email: '', password: '' }
        })
      },
      enhance: vi.fn((form) => {
        // Simulate successful submission
        form.addEventListener('submit', (e) => {
          e.preventDefault();
          const formData = new FormData(form);
          submittedData = {
            email: formData.get('email'),
            password: formData.get('password')
          };
        });
      }),
      errors: {
        subscribe: vi.fn().mockReturnValue({})
      },
      submitting: {
        subscribe: vi.fn().mockReturnValue(false)
      }
    });

    render(UserForm);

    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: 'Submit' });

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    await waitFor(() => {
      expect(submittedData).toEqual({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });

  it('shows loading state during submission', async () => {
    vi.mocked(superForm).mockReturnValue({
      form: {
        subscribe: vi.fn().mockReturnValue({
          email: 'test@example.com',
          password: 'password123',
          errors: { email: '', password: '' }
        })
      },
      enhance: vi.fn(),
      errors: {
        subscribe: vi.fn().mockReturnValue({})
      },
      submitting: {
        subscribe: vi.fn().mockReturnValue(true)
      }
    });

    render(UserForm);

    const submitButton = screen.getByRole('button', { name: 'Submitting...' });
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent('Submitting...');
  });
});
```

## E2E Testing with Playwright

### Setup
```bash
npm install -D @playwright/test
```

### Playwright Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run build && npm run preview',
    port: 4173,
  },
});
```

### Component E2E Tests

#### Button E2E Test
```typescript
// tests/e2e/button.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button Component', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should render button with correct text', async ({ page }) => {
    await page.goto('/components/button');

    const button = page.getByRole('button', { name: 'Click me' });
    await expect(button).toBeVisible();
    await expect(button).toContainText('Click me');
  });

  test('should handle click events', async ({ page }) => {
    await page.goto('/components/button');

    const button = page.getByRole('button', { name: 'Click me' });
    const clickCount = page.locator('#click-count');

    await button.click();
    await expect(clickCount).toContainText('1');

    await button.click();
    await expect(clickCount).toContainText('2');
  });

  test('should show loading state', async ({ page }) => {
    await page.goto('/components/button');

    const loadButton = page.getByRole('button', { name: 'Load Data' });
    const loadingText = page.locator('#loading-text');

    await loadButton.click();
    await expect(loadingText).toBeVisible();
    await expect(loadingText).toContainText('Loading...');
  });

  test('should be keyboard accessible', async ({ page }) => {
    await page.goto('/components/button');

    // Focus button with keyboard
    await page.keyboard.press('Tab');
    const button = page.getByRole('button', { name: 'Click me' });
    await expect(button).toBeFocused();

    // Activate with Enter key
    await page.keyboard.press('Enter');
    await expect(page.locator('#click-count')).toContainText('1');

    // Activate with Space key
    await page.keyboard.press('Space');
    await expect(page.locator('#click-count')).toContainText('2');
  });

  test('should respect disabled state', async ({ page }) => {
    await page.goto('/components/button');

    const disabledButton = page.getByRole('button', { name: 'Disabled Button' });
    await expect(disabledButton).toBeDisabled();
    await expect(disabledButton).toHaveAttribute('aria-disabled', 'true');

    // Clicks should not work
    await disabledButton.click();
    await expect(page.locator('#click-count')).toContainText('0');
  });
});
```

#### Form E2E Test
```typescript
// tests/e2e/form.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Registration Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
  });

  test('should register user successfully', async ({ page }) => {
    // Fill form with valid data
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'securePassword123');
    await page.fill('[data-testid="confirm-password-input"]', 'securePassword123');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Account created successfully');

    // Verify redirection
    await expect(page).toHaveURL('/dashboard');
  });

  test('should show validation errors for invalid email', async ({ page }) => {
    // Fill form with invalid email
    await page.fill('[data-testid="email-input"]', 'invalid-email');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Please enter a valid email address');

    // Verify no redirection
    await expect(page).toHaveURL('/register');
  });

  test('should show error when passwords do not match', async ({ page }) => {
    // Fill form with mismatched passwords
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'differentPassword');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="confirm-password-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-error"]')).toContainText('Passwords do not match');
  });

  test('should support keyboard navigation', async ({ page }) => {
    // Navigate through form using Tab
    await page.keyboard.press('Tab'); // Focus email input
    await expect(page.locator('[data-testid="email-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus password input
    await expect(page.locator('[data-testid="password-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus confirm password input
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeFocused();

    await page.keyboard.press('Tab'); // Focus submit button
    await expect(page.locator('[data-testid="submit-button"]')).toBeFocused();

    // Submit form with Enter key
    await page.keyboard.press('Enter');

    // Verify validation errors appear (empty form)
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
  });

  test('should handle form submission with loading state', async ({ page }) => {
    // Fill form with valid data
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');

    // Mock slow network response
    await page.route('/api/register', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ success: true })
      });
    });

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify loading state
    await expect(page.locator('[data-testid="submit-button"]')).toBeDisabled();
    await expect(page.locator('[data-testid="submit-button"]')).toContainText('Creating account...');

    // Verify completion
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });
});
```

### Accessibility Testing

#### Accessibility Assertions
```typescript
// tests/e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y } from 'axe-playwright';

test.describe('Accessibility Tests', () => {
  test.beforeEach(async ({ page }) => {
    await injectAxe(page);
  });

  test('should meet accessibility standards', async ({ page }) => {
    await page.goto('/');
    await checkA11y(page);
  });

  test('should have proper ARIA labels', async ({ page }) => {
    await page.goto('/components/form');

    // Check form labels
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();

    // Check button descriptions
    const submitButton = page.getByRole('button', { name: 'Submit form' });
    await expect(submitButton).toBeVisible();
    await expect(submitButton).toHaveAttribute('aria-label', 'Submit form');
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/components/navigation');

    // Navigate through tabs
    await page.keyboard.press('Tab');
    await expect(page.getByRole('tab', { name: 'Profile' })).toBeFocused();

    await page.keyboard.press('ArrowRight');
    await expect(page.getByRole('tab', { name: 'Settings' })).toBeFocused();

    // Activate tab with Enter
    await page.keyboard.press('Enter');
    await expect(page.getByRole('tabpanel', { name: 'Settings content' })).toBeVisible();
  });

  test('should announce errors to screen readers', async ({ page }) => {
    await page.goto('/components/form');

    // Submit empty form to trigger errors
    await page.getByRole('button', { name: 'Submit form' }).click();

    // Check for live regions
    await expect(page.locator('[role="alert"]')).toBeVisible();
    await expect(page.locator('[aria-live="polite"]')).toBeVisible();

    // Verify error announcements
    await expect(page.getByText('Form has validation errors')).toBeVisible();
  });

  test('should maintain focus management', async ({ page }) => {
    await page.goto('/components/dialog');

    // Open dialog
    await page.getByRole('button', { name: 'Open Dialog' }).click();

    // Check focus is trapped in dialog
    await expect(page.getByRole('dialog')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Close' })).toBeFocused();

    // Try to tab outside dialog
    await page.keyboard.press('Tab');
    await expect(page.getByRole('dialog')).toBeFocused();

    // Close dialog with Escape
    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Open Dialog' })).toBeFocused();
  });
});
```

## Testing Utilities

### Custom Testing Helpers
```typescript
// src/test/utils.ts
import { render, RenderOptions } from '@testing-library/svelte';
import { ComponentType } from 'svelte';

// Custom render function with theme support
export const renderWithTheme = <Props extends object>(
  component: ComponentType<Props>,
  options?: RenderOptions<Props> & { theme?: 'light' | 'dark' }
) => {
  const { theme = 'light', ...renderOptions } = options || {};

  // Mock CSS variables for testing
  const themeStyles = theme === 'dark'
    ? 'color-scheme: dark; --background: 222.2 84% 4.9%; --foreground: 210 40% 98%;'
    : 'color-scheme: light; --background: 0 0% 100%; --foreground: 222.2 84% 4.9%;';

  Object.defineProperty(document.documentElement, 'style', {
    value: themeStyles,
    writable: true
  });

  return render(component, renderOptions);
};

// Helper to test accessibility
export const testAccessibility = async (container: HTMLElement) => {
  const axe = await import('axe-core');
  const results = await axe.run(container);

  expect(results.violations).toHaveLength(0);
  return results;
};

// Helper to test keyboard navigation
export const testKeyboardNavigation = async (
  container: HTMLElement,
  expectedFocusOrder: string[]
) => {
  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  expect(focusableElements.length).toBe(expectedFocusOrder.length);

  for (let i = 0; i < focusableElements.length; i++) {
    (focusableElements[i] as HTMLElement).focus();
    expect(document.activeElement).toBe(focusableElements[i]);
    expect(document.activeElement).toHaveAttribute('data-testid', expectedFocusOrder[i]);
  }
};

// Helper to test form validation
export const testFormValidation = async (
  formElement: HTMLFormElement,
  invalidFields: string[]
) => {
  // Trigger form validation
  const submitEvent = new Event('submit', { cancelable: true });
  formElement.dispatchEvent(submitEvent);

  // Check invalid fields
  invalidFields.forEach(fieldName => {
    const field = formElement.querySelector(`[name="${fieldName}"]`) as HTMLInputElement;
    expect(field.validity.valid).toBe(false);
    expect(field).toHaveAttribute('aria-invalid', 'true');
  });
};
```

### Mock Components
```typescript
// src/test/mocks.ts
import { vi } from 'vitest';

// Mock Lucide icons
export const mockIcons = {
  Plus: vi.fn(() => 'mock-plus-icon'),
  Trash2: vi.fn(() => 'mock-trash-icon'),
  Settings: vi.fn(() => 'mock-settings-icon'),
};

// Mock window API
export const mockWindow = {
  matchMedia: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
  localStorage: {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  },
};

// Mock form submission
export const mockFormSubmission = vi.fn().mockResolvedValue({
  type: 'success',
  data: { id: '1', email: 'test@example.com' }
});
```

### Test Scenarios

#### Component States Test
```typescript
// src/test/scenarios/component-states.test.ts
import { render, screen } from '@testing-library/svelte';
import { testAccessibility } from '../utils';
import { describe, it, expect } from 'vitest';
import Button from '../../components/ui/button/Button.svelte';

describe('Button Component States', () => {
  const scenarios = [
    {
      name: 'default primary button',
      props: { children: 'Primary Button' },
      expectedClasses: ['bg-primary', 'text-primary-foreground']
    },
    {
      name: 'destructive button',
      props: { variant: 'destructive', children: 'Delete' },
      expectedClasses: ['bg-destructive', 'text-destructive-foreground']
    },
    {
      name: 'outline button',
      props: { variant: 'outline', children: 'Cancel' },
      expectedClasses: ['border', 'bg-background']
    },
    {
      name: 'small button',
      props: { size: 'sm', children: 'Small' },
      expectedClasses: ['h-9', 'rounded-md', 'px-3']
    },
    {
      name: 'large button',
      props: { size: 'lg', children: 'Large' },
      expectedClasses: ['h-11', 'rounded-md', 'px-8']
    }
  ];

  scenarios.forEach(({ name, props, expectedClasses }) => {
    it(`should render ${name} correctly`, () => {
      render(Button, props);

      const button = screen.getByRole('button');

      expectedClasses.forEach(className => {
        expect(button).toHaveClass(className);
      });

      testAccessibility(button.parentElement!);
    });
  });
});
```

This comprehensive testing guide covers unit testing with Vitest, E2E testing with Playwright, accessibility testing, and testing utilities for shadcn-svelte components.