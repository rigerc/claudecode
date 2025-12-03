# shadcn-svelte Components Reference

## Component Categories

### Form Controls
- **Button** - Versatile button with variants and sizes
- **Input** - Text input with validation states
- **Select** - Dropdown select component
- **Checkbox** - Multi-select checkbox
- **Radio Group** - Single selection radio buttons
- **Switch** - Toggle switch component
- **Textarea** - Multi-line text input
- **Label** - Form label with accessibility

### Navigation
- **Tabs** - Tabbed content switching
- **Breadcrumb** - Navigation breadcrumb trail
- **Pagination** - Page navigation controls
- **Navigation Menu** - Complex navigation with dropdowns
- **Menubar** - Application menu bar

### Feedback & Overlays
- **Alert** - Informational alerts
- **Toast** - Notification messages
- **Dialog** - Modal dialogs
- **Sheet** - Slide-out panels
- **Drawer** - Bottom drawer component
- **AlertDialog** - Confirmation dialogs
- **Hover Card** - Contextual hover information

### Data Display
- **Card** - Content cards with headers and actions
- **Table** - Data tables with sorting and filtering
- **Accordion** - Collapsible content sections
- **Collapsible** - Single collapsible section
- **Skeleton** - Loading placeholders
- **Progress** - Progress indicators
- **Badge** - Status badges and labels

### Layout
- **Separator** - Visual dividers
- **ScrollArea** - Custom scrollable areas
- **AspectRatio** - Fixed aspect ratio containers

### Media
- **Avatar** - User avatars with fallbacks
- **Image** - Optimized image component
- **Carousel** - Image/content carousels

## Component Usage Examples

### Button
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
</script>

<!-- Variants -->
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

<!-- Sizes -->
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>

<!-- With icons -->
<Button>
  <PlusIcon class="w-4 h-4 mr-2" />
  Add Item
</Button>
```

### Card
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

### Input with Form
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

### Alert
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

### Dialog
```svelte
<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Dialog from "$lib/components/ui/dialog";

  let open = $state(false);
</script>

<Dialog.Root bind:open>
  <Dialog.Trigger>
    <Button>Open Dialog</Button>
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

### Tabs
```svelte
<script lang="ts">
  import * as Tabs from "$lib/components/ui/tabs";
</script>

<Tabs.Root defaultValue="account" class="w-[400px]">
  <Tabs.List class="grid w-full grid-cols-2">
    <Tabs.Trigger value="account">Account</Tabs.Trigger>
    <Tabs.Trigger value="password">Password</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="account">
    <p>Account settings content</p>
  </Tabs.Content>
  <Tabs.Content value="password">
    <p>Password change content</p>
  </Tabs.Content>
</Tabs.Root>
```

## Component Patterns

### Consistent Props
Most components follow this pattern:
```typescript
interface ComponentProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  class?: string;
  children?: Snippet;
}
```

### Accessibility Features
- Proper ARIA attributes
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- High contrast support

### Styling Integration
- Tailwind CSS classes
- CSS variables for theming
- Responsive design
- Dark mode support