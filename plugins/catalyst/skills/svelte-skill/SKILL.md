---
name: svelte-skill
description: Use when developing Svelte 5 applications with new runes syntax, reactive state management, or building modern component-based user interfaces.
tags: [svelte, frontend, reactive, components, web-development]
version: 5.x
framework: svelte
---

# Svelte Development Skill

Expert guidance for building modern web applications with Svelte 5, including new runes system, components, reactivity, and advanced development patterns.

## Quick Start

**Create a new Svelte project:**
```bash
npm create svelte@latest myapp
cd myapp
npm install
npm run dev
```

**Basic reactive component:**
```svelte
<script>
  let count = $state(0);
  function increment() => count++;
</script>
<button onclick={increment}>Clicks: {count}</button>
```

## Expert Guidance

- **Runes System**: New `$state`, `$derived`, `$effect` reactive patterns
- **Component Architecture**: File structure, props, and lifecycle
- **Template Syntax**: Conditionals, loops, snippets with new syntax
- **State Management**: Best practices for reactive data patterns
- **Forms & Binding**: Two-way data binding and form handling
- **Styling**: Scoped CSS, global styles, and theming

## Progressive Disclosure

Level 2 provides core concepts and examples. Level 3+ contains detailed implementation guides and patterns.

## See Also

- **references/components.md** - Complete component patterns
- **references/reactivity.md** - Runes, state, and effects
- **references/template-syntax.md** - Template control flow
- **references/forms.md** - Form binding and validation
- **references/migration.md** - Svelte 4 to 5 migration guide