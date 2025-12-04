# Spatial Composition & Layout Patterns

Advanced layout techniques including asymmetry, overlap, diagonal flows, and grid-breaking.

## Asymmetric Grid Patterns

### Unequal Column Split (30/70)
```css
.asymmetric-layout {
  display: grid;
  grid-template-columns: 1fr 2.5fr;
  gap: 4rem;
  align-items: center;
}

/* Alternative: mobile-aware */
.asymmetric-layout {
  display: grid;
  grid-template-columns: clamp(200px, 30%, 350px) 1fr;
  gap: 3rem;
}
```
**Visual effect**: Small, focused element + large, dominant element creates hierarchy.

**Use case**: Product showcase (text left, image right), team bio (small avatar, large name/bio), feature callout (icon left, description right)

### Offset Column Grid
```css
.offset-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

/* First row: offset right */
.item:nth-child(1) {
  grid-column: 1 / 2;
  margin-top: 0;
}

.item:nth-child(2) {
  grid-column: 2 / 3;
  margin-top: 4rem; /* Creates vertical offset */
}
```
**Visual effect**: Staggered arrangement prevents predictable alignment.

## Overlapping Cards with Z-Index Layering

### Card Stack (3D Effect)
```css
.card-stack {
  position: relative;
  height: 500px;
  perspective: 1000px;
}

.card {
  position: absolute;
  width: 320px;
  height: 400px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  background: white;
}

.card:nth-child(1) {
  left: 0;
  top: 0;
  z-index: 3;
  transform: rotate(-2deg);
}

.card:nth-child(2) {
  left: 50px;
  top: 40px;
  z-index: 2;
  transform: rotate(1deg);
}

.card:nth-child(3) {
  left: 100px;
  top: 80px;
  z-index: 1;
  transform: rotate(-1deg);
}
```
**Use cases**: Portfolio showcases, team member cards, service feature cards, process flow visualization, image gallery displays

### Image + Text Overlap
```css
.overlap-section {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  position: relative;
  align-items: center;
  gap: -2rem; /* Allows overlap */
}

.image {
  grid-column: 1;
  width: 100%;
  z-index: 2;
  margin-right: -2rem; /* Overlap into text */
}

.text {
  grid-column: 2;
  background: white;
  padding: 3rem;
  border-radius: 8px;
  z-index: 1;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```
**Result**: Image extends into text container, creating visual depth.

## Diagonal Flow with Transform

### Skewed Container
```css
.diagonal-section {
  position: relative;
  padding: 6rem 4rem;
  background: linear-gradient(135deg, #f5f5f5, #ffffff);
  overflow: hidden;
}

.diagonal-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: var(--accent-color);
  opacity: 0.05;
  transform: skew(-15deg) rotate(-10deg);
  z-index: 0;
}

.diagonal-content {
  position: relative;
  z-index: 1;
}
```

### Rotated Elements
```css
.element {
  transform: rotate(-3deg);
}

.element:nth-child(even) {
  transform: rotate(3deg);
}

/* For stronger effect */
.element-strong {
  transform: rotate(-8deg) skewX(-2deg);
}
```
**Timing**: Keep rotation between ±2deg for readability, ±5deg for bold effect.

## Advanced Layout Patterns

### Asymmetric Two-Column Contrast
Unequal column widths creating dynamic visual balance (e.g., 30/70 or 40/60 split).

**Use cases**: Product showcase pages, feature comparisons, team bios with photos, article with featured imagery, before/after demonstrations

**Responsive**: Collapses to single column at breakpoint (< 768px typically), then stacks vertically maintaining visual emphasis

### Grid Break-Out with Absolute Positioning
Container-constrained grid with elements breaking out of boundaries using absolute positioning.

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  position: relative;
  margin: 4rem;
}

/* Standard grid items */
.grid-item {
  grid-column: span 4;
  position: relative;
}

/* Breaking out of grid bounds */
.breakout-large {
  position: absolute;
  width: 150%;
  height: 120%;
  top: -10%;
  left: -25%;
  z-index: 10;
}
```
**Use cases**: Magazine-style layouts, featured content sections, image galleries with emphasis, design showcase presentations, portfolio hero sections

### Circular/Organic Grid Layout
Non-rectangular grid arrangement using radial positioning and organic shapes.

```css
.circular-grid {
  position: relative;
  width: 600px;
  height: 600px;
}

.item {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Center item */
.item:nth-child(1) {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) scale(1.2);
  z-index: 10;
}

/* Orbit positioning formula: rotate(angle) translateX(radius) */
.item:nth-child(2) { transform: translate(-50%, -50%) rotate(0deg) translateX(150px) rotate(0deg); }
.item:nth-child(3) { transform: translate(-50%, -50%) rotate(72deg) translateX(150px) rotate(-72deg); }
```
**Use cases**: Service category showcases, team member directories, skill/capability mapping, process workflows, feature comparison wheels

### Masonry with Variable Heights
Irregular grid where items have varying heights creating interlocked visual pattern.

```css
/* CSS Grid Masonry */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: 250px;
  gap: 2rem;
  grid-auto-flow: dense; /* Fills gaps efficiently */
}

/* Size variations */
.item:nth-child(2n) {
  grid-row: span 2;
}

.item:nth-child(3n) {
  grid-column: span 2;
}
```
**Use cases**: Photo galleries, portfolio item showcases, blog post grids, product catalogs, image-heavy content displays

**Responsive**: Desktop: 3-4 columns with variable heights. Tablet: 2 columns with reduced variation. Mobile: single column, variable heights maintained

### Split-Screen with Scroll Offset
Two-column layout where right content scrolls at different rate creating parallax effect.

```css
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  overflow: hidden;
}

.left-pane {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  background: var(--bg-left);
}

.right-pane {
  overflow-y: auto;
  height: 100vh;
  background: var(--bg-right);
}
```
**Use cases**: Documentation with live preview, code editor interfaces, before/after comparisons, story-telling layouts, product comparison pages

**Responsive**: Desktop: side-by-side with independent scrolling. Tablet/Mobile: stacked vertically with synchronized scroll, parallax reduced or disabled

## Directional Flow Patterns

### Left-Heavy (Content Left, Visual Right)
```css
.left-heavy {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;
  align-items: center;
}
```
Draws eye left first, then right. Natural reading direction in LTR.

### Right-Heavy (Visual Left, Content Right)
```css
.right-heavy {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 3rem;
  align-items: center;
}
```
Creates emphasis on right side. Works for CTAs and emphasis.

## Implementation Checklist

- [ ] No perfect 50/50 columns (use 30/70, 35/65, 40/60)
- [ ] Vertical stagger on grid rows (offset every other row)
- [ ] Overlap creates depth (z-index + negative margins)
- [ ] Rotation between ±2-5deg (subtle, not disorienting)
- [ ] Color/shadow defines layering hierarchy
- [ ] Asymmetry serves content hierarchy (not just decoration)
- [ ] Mobile resets to single column or symmetric layout
