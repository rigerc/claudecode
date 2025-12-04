# Frontend Designer Skill

Expert frontend design guidance using a proven 5-dimension framework to create intentional, non-generic designs.

## Overview

This skill helps you avoid generic AI-generated design patterns and create distinctive, intentional frontend interfaces. It's based on a comprehensive design system extracted from industry best practices, professional design tools, and proven aesthetic frameworks.

## The 5 Design Dimensions

1. **Typography Dimension**
   - Font selection and pairing strategies
   - Weight extremes (300/700/900 instead of mid-range)
   - Size scales with 3x+ jumps (not incremental 1.5x)
   - Anti-patterns: Inter, Roboto, Open Sans as defaults

2. **Color & Theme Dimension**
   - IDE-inspired professional color palettes (Dracula, Nord, Monokai Pro, etc.)
   - Layered gradient techniques for atmospheric depth
   - Avoiding Material Design color trinity (blue/red/green)

3. **Motion Dimension**
   - Orchestrated CSS and Framer Motion animations
   - Easing functions (not linear timing)
   - Page load choreography, scroll triggers, hover surprises

4. **Spatial Composition Dimension**
   - Asymmetric layouts (30/70 splits, not centered)
   - Overlapping elements with z-index layering
   - Diagonal flows and grid break-outs

5. **Backgrounds & Visual Details Dimension**
   - Subtle gradients and noise textures
   - Atmospheric backgrounds (not flat white/black)
   - Micro-interactions and visual polish

## When to Use This Skill

- Designing user interfaces, landing pages, or web applications
- Creating brand-differentiated design systems
- Implementing responsive layouts with visual hierarchy
- Adding motion and animation to interfaces
- Selecting color palettes and typography
- Avoiding generic "AI-generated" aesthetic patterns

## Design Thinking Workflow

Before implementing any design, this skill guides you through 4 critical questions:

1. **Purpose**: What problem are we solving? Who are the users?
2. **Tone**: What emotional response do we want?
3. **Constraints**: What are the technical, temporal, or business limits?
4. **Differentiation**: What one unforgettable element makes this distinctly ours?

## Structure

- `SKILL.md` - Main skill instructions (Level 2: quick reference)
- `references/` - Detailed documentation loaded as needed (Level 3)
  - `design-thinking.md` - Pre-design workflow and planning
  - `typography.md` - Font selection, pairing, weights, sizes
  - `color-themes.md` - IDE palettes, gradients, techniques
  - `motion.md` - CSS/Framer Motion animation patterns
  - `spatial-composition.md` - Layout patterns and techniques
  - `aesthetics-framework.md` - Complete 5-dimension deep dive
  - `anti-patterns.md` - Common mistakes to avoid

## Quick Example

```css
/* Avoid: Generic AI design */
body {
  font-family: Inter;
  background: white;
}
h1 {
  font-size: 32px;
  font-weight: 600;
}

/* Better: Intentional design with 5 dimensions */
body {
  /* Typography: Distinctive pairing */
  font-family: 'IBM Plex Sans', sans-serif;

  /* Color: Layered atmospheric gradient */
  background: radial-gradient(circle at 20% 50%, rgba(99,102,241,0.1), transparent 50%),
              linear-gradient(135deg, #1e293b, #0f172a);
  background-attachment: fixed;
}

h1 {
  /* Typography: Serif display + extreme size (5.5x body) */
  font-family: 'Playfair Display', serif;
  font-size: 88px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;

  /* Motion: Orchestrated entrance */
  animation: slideInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Spatial: Asymmetric layout (30/70 split) */
.hero {
  display: grid;
  grid-template-columns: 1fr 2.5fr;
  gap: 4rem;
  align-items: center;
}
```

## Anti-Generic AI Checklist

Use this checklist to ensure your design is intentional, not generic:

- [ ] Rejected Inter/Roboto/Open Sans as primary fonts
- [ ] Used 3x+ size jumps between typography levels
- [ ] Avoided Material Design color trinity (blue/red/green)
- [ ] Created asymmetrical layouts (not centered/symmetrical)
- [ ] Added easing functions to animations (not linear)
- [ ] Used subtle gradients/textures (not flat backgrounds)

## Design Sources

This skill draws from:

- Professional IDE/code editor themes (Dracula, Nord, Monokai Pro, Solarized, One Dark Pro, GitHub Dark, Gruvbox, JetBrains Darcula)
- Advanced typography theory and progressive size scales
- Modern web animation patterns (CSS and Framer Motion)
- Contemporary layout techniques (asymmetry, overlap, masonry, split-screen)
- Gradient and texture design principles

## Usage

This skill is automatically discovered by Claude when relevant to the task. You can also explicitly invoke it using the Skill tool.

## Progressive Disclosure

This skill follows progressive disclosure best practices:

- **Level 1 (Metadata)**: Concise description for skill discovery (~21 tokens)
- **Level 2 (SKILL.md)**: Quick reference with core principles (~263 tokens)
- **Level 3 (References)**: Detailed documentation loaded as needed (unlimited)
