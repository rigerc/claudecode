# shadcn-svelte: Beautiful Svelte Components with Tailwind CSS

## Overview

**shadcn-svelte** is a comprehensive component library for Svelte applications that provides beautifully-designed, accessible UI components built with Tailwind CSS. It's the official Svelte port of the popular [shadcn/ui](https://ui.shadcn.com/) library, adapted specifically for the Svelte ecosystem.

### What Makes shadcn-svelte Special?

- **Component Library, Not Component Framework**: Unlike traditional UI libraries, shadcn-svelte provides components as source code that you copy into your project, giving you complete control over customization and implementation
- **Built on Proven Primitives**: Components are built on top of [Bits UI](https://bits-ui.com/), which provides the underlying accessibility and behavior primitives using Radix UI
- **Tailwind CSS Integration**: Full integration with Tailwind CSS for consistent, utility-first styling
- **TypeScript First**: Written entirely in TypeScript with excellent type safety and IntelliSense support
- **SvelteKit Optimized**: Designed to work seamlessly with SvelteKit's conventions and build process

### Key Features

#### 🎨 Beautiful Design
- Modern, clean design system that follows accessibility best practices
- Consistent spacing, typography, and color schemes
- Dark mode support built into every component
- Smooth animations and transitions

#### ♿ Accessibility First
- All components meet WCAG 2.1 AA standards
- Proper ARIA attributes and keyboard navigation
- Screen reader support
- Focus management and trapping for modals

#### 🛠 Developer Experience
- CLI tool for easy component installation and updates
- Full TypeScript support with comprehensive type definitions
- Excellent documentation with live examples
- VS Code and JetBrains extensions for enhanced development

#### 🔧 Complete Control
- Copy components directly into your project
- Customize any aspect of the components
- No runtime dependencies beyond what you choose
- Tree-shakable and bundle-friendly

### Relationship to shadcn/ui

shadcn-svelte is the official Svelte port of shadcn/ui, maintaining:
- **Design Consistency**: Same visual design language and component behavior
- **API Parity**: Similar component APIs where applicable, adapted for Svelte's reactivity model
- **Feature Compatibility**: Most features from the original React version are available
- **Community Alignment**: Regular updates to stay in sync with shadcn/ui improvements

### Why Use shadcn-svelte with Tailwind CSS?

#### 1. **Utility-First Styling**
Tailwind CSS provides the perfect foundation for shadcn-svelte's design system:

```svelte
<!-- Example: Button with Tailwind classes -->
<button class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors">
  Click me
</button>
```

#### 2. **Rapid Development**
- No need to write custom CSS
- Consistent design tokens across all components
- Easy customization through utility classes
- Responsive design built-in

#### 3. **Performance**
- Small bundle sizes with tree shaking
- No CSS runtime overhead
- Optimized for production builds
- Minimal JavaScript footprint

#### 4. **Maintainability**
- Predictable styling patterns
- Easy to modify and extend
- Clear separation of concerns
- Excellent TypeScript support

### Component Architecture

Each shadcn-svelte component follows a consistent structure:

```
src/lib/components/ui/
├── button/
│   ├── Button.svelte          # Main component
│   ├── index.ts              # Barrel export
│   └── types.ts              # Type definitions
```

This structure ensures:
- Clear separation of concerns
- Easy navigation and imports
- Consistent patterns across components
- TypeScript integration

### Supported Components

shadcn-svelte includes 40+ components covering all common UI patterns:

- **Form Controls**: Button, Input, Select, Checkbox, Radio, Switch
- **Navigation**: Tabs, Breadcrumb, Pagination, Menu
- **Feedback**: Alert, Toast, Dialog, Sheet, Drawer
- **Data Display**: Card, Table, Accordion, Collapsible
- **Layout**: Separator, ScrollArea, AspectRatio
- **Media**: Avatar, Badge, Progress

### Browser Support

shadcn-svelte supports all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### When to Use shadcn-svelte

#### Ideal For:
- New SvelteKit applications
- Projects requiring consistent design systems
- Teams that value accessibility
- Applications needing dark mode support
- Projects with custom styling requirements

#### Consider Alternatives When:
- You need a complete design system (consider Melt UI)
- You prefer zero-config setup (consider Skeleton UI)
- You need framework-specific components for other frameworks

### Community and Ecosystem

- **GitHub**: [shadcn-svelte](https://github.com/huntabyte/shadcn-svelte)
- **Documentation**: [shadcn-svelte.com](https://www.shadcn-svelte.com)
- **Discord**: Active community support
- **Contributing**: Open-source with regular updates

### License

shadcn-svelte is licensed under the MIT License, making it free for commercial and personal use.

## Next Steps

Ready to get started? Check out our guides:

- [**Quick Start**](./shadcn-svelte-quickstart.md) - Get up and running in 5 minutes
- [**Installation & Setup**](./shadcn-svelte-installation.md) - Detailed setup instructions
- [**Component Usage**](./shadcn-svelte-components.md) - Learn how to use components
- [**Customization**](./shadcn-svelte-customization.md) - Make components your own
- [**Best Practices**](./shadcn-svelte-best-practices.md) - Development patterns and tips

---

*This documentation covers shadcn-svelte with Tailwind CSS integration. For the most up-to-date information, visit the [official shadcn-svelte documentation](https://www.shadcn-svelte.com).*