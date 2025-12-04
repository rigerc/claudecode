---
name: frontend-designer
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Frontend design expert using 5-dimension framework to create intentional non-generic designs. Use for UI/UX design tasks.
---

# Frontend Designer

Expert guidance for intentional, non-generic frontend designs using a 5-dimension framework.

## Quick Start

```css
/* 5-dimension framework example */
body {
  font-family: 'IBM Plex Sans', sans-serif; /* Typography */
  background: radial-gradient(circle at 20% 50%, rgba(99,102,241,0.1), transparent 50%),
              linear-gradient(135deg, #1e293b, #0f172a); /* Color */
}
h1 {
  font-family: 'Playfair Display', serif; /* Typography: serif + extreme size */
  font-size: 88px; font-weight: 700;
  animation: slideInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1); /* Motion */
}
```

## The 5 Dimensions

1. **Typography** - Font pairing, extreme weights (300/700/900), 3x+ size jumps
2. **Color** - IDE-inspired palettes, layered gradients (avoid Material defaults)
3. **Motion** - Orchestrated animations with easing (CSS/Framer Motion)
4. **Spatial** - Asymmetric layouts (30/70 splits, overlaps, z-index)
5. **Details** - Subtle gradients, textures, atmospheric backgrounds

## Pre-Design Workflow

Answer before coding (see `design-thinking.md`):
1. **Purpose** - Problem? Users?
2. **Tone** - Emotional response?
3. **Constraints** - Technical limits?
4. **Differentiation** - What makes this ours?

## Anti-Generic Checklist

- [ ] Rejected Inter/Roboto/Open Sans | [ ] 3x+ size jumps
- [ ] Avoided blue/red/green trinity | [ ] Asymmetric layouts
- [ ] Added easing functions (not linear)

## References

- `design-thinking.md` `typography.md` `color-themes.md` `motion.md` `spatial-composition.md` `aesthetics-framework.md` `anti-patterns.md`
