# Color Themes & Palettes

Comprehensive guide to color selection, IDE theme inspiration, and gradient techniques.

## Professional Color Palettes

Based on popular IDE/code editor themes that have been scientifically designed for accessibility and extended use:

### Dracula Official
**Mood**: Dark purple/pink, high contrast, optimized for extended sessions
- Background: `#282a36`
- Foreground: `#f8f8f2`
- Accent Colors: `#ff5555` (red), `#ffb86c` (orange), `#f1fa8c` (yellow), `#50fa7b` (green), `#8be9fd` (cyan), `#bd93f9` (blue), `#ff79c6` (purple)
- Use: Dark mode applications, developer tools, modern web interfaces

### Nord
**Mood**: Arctic blue-based, cool and calming, inspired by Nordic landscapes
- Palette: `#2e3440`, `#3b4252`, `#434c5e`, `#4c566a` (dark grays)
- Colors: `#8fbcbb`, `#88c0d0`, `#81a1c1`, `#5e81ac` (blues)
- Accents: `#bf616a` (red), `#d08770` (orange), `#ebcb8b` (yellow), `#a3be8c` (green), `#b48ead` (purple)
- Use: Professional applications, technical documentation, long-duration use

### Monokai Pro
**Mood**: Vibrant syntax highlighting with modern dark theme
- Background: `#2d2a2e`
- Foreground: `#fcfcfa`
- Colors: `#ffd866` (string), `#a1efe4` (number), `#fd9353` (boolean), `#a9dc76` (function), `#ff6188` (keyword)
- Use: Creative coding, high-visibility syntax highlighting, modern development

### Solarized Dark
**Mood**: Scientifically designed precision colors for machines and people
- Base: `#002b36`, `#073642`, `#839496`, `#93a1a1`
- Colors: `#268bd2` (blue), `#2aa198` (cyan), `#859900` (green), `#b58900` (yellow), `#cb4b16` (orange), `#dc322f` (red)
- Use: Research projects, long-form coding, accessibility-first design

### One Dark Pro
**Mood**: Warm and professional dark theme (Atom One Dark adapted)
- Background: `#282c34`
- Foreground: `#abb2bf`
- Colors: `#e06c75` (red), `#d19a66` (orange), `#e5c07b` (yellow), `#98c379` (green), `#56b6c2` (cyan), `#61afef` (blue), `#c678dd` (purple)
- Use: Daily development, general-purpose coding, comfortable extended use

### GitHub Dark
**Mood**: Official GitHub dark theme, professional and consistent
- Background: `#0d1117`
- Foreground: `#c9d1d9`
- Border: `#30363d`
- Colors: `#f85149` (red), `#fb8500` (orange), `#d29922` (yellow), `#3fb950` (green), `#58a6ff` (blue), `#bc8ef0` (purple)
- Use: Code collaboration platforms, developer communities, GitHub integrations

### Gruvbox Dark
**Mood**: Retro groove color scheme, warm and pleasant
- Background: `#282828`
- Foreground: `#ebdbb2`
- Colors: `#cc241d` (red), `#98971a` (green), `#d79921` (yellow), `#458588` (blue), `#b16286` (purple), `#689d6a` (aqua), `#d65d0e` (orange)
- Use: Terminal environments, minimalist editors, nostalgic interfaces

### JetBrains Darcula
**Mood**: Sophisticated enterprise-grade IDE theme
- Background: `#2b2d30`
- Foreground: `#a9b1d6`
- Colors: `#ff5f5f` (red), `#ffb86c` (orange), `#f1fa8c` (yellow), `#51cf66` (green), `#80d4ff` (blue), `#bb86fc` (purple)
- Use: Enterprise development, Java/Kotlin projects, professional environments

## Gradient Techniques

### Layered Gradient (Color + Darkness)
```css
.layered-two {
  background:
    linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)),
    linear-gradient(45deg, #1e293b, #0f172a);
  background-attachment: fixed;
}
```
**Effect**: Accent color fade over dark base. Creates depth without solid colors.

### Three-Layer Gradient (Color + Texture + Dark)
```css
.layered-three {
  background:
    radial-gradient(circle at 20% 80%, rgba(244, 114, 182, 0.15), transparent 50%),
    linear-gradient(135deg, rgba(99, 102, 241, 0.6), rgba(59, 130, 246, 0.6)),
    linear-gradient(45deg, #1e293b, #0f172a);
  background-attachment: fixed;
}
```
**Effect**: Soft accent glow + color layer + dark base = atmospheric depth.

### Gradient Mesh (4-Point)
```css
.gradient-mesh {
  background:
    radial-gradient(circle at 20% 30%, rgba(244, 114, 182, 0.4), transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.3), transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(34, 197, 94, 0.2), transparent 60%),
    linear-gradient(135deg, #0f172a, #1e293b);
}
```
**Effect**: Multiple color nodes blend organically. Complex, sophisticated appearance.

## Radial Gradients for Depth

### Vignette (Dark Edges)
```css
.vignette {
  background:
    radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.7) 100%),
    linear-gradient(135deg, #1e293b, #0f172a);
}
```
**Use case**: Draw focus to center. Emphasize central content.

### Spotlight Effect
```css
.spotlight {
  background:
    radial-gradient(circle at 40% 60%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #1e293b, #0f172a);
}
```
**Use case**: Highlight specific region. Create focal point without text.

## CSS Noise Texture

### SVG Noise Filter
```css
.texture-noise {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  position: relative;
}

.texture-noise::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="n"><feTurbulence baseFrequency=".9" numOctaves="4"/></filter><rect width="100%" height="100%" filter="url(%23n)" opacity=".05"/></svg>');
  pointer-events: none;
  z-index: 1;
}
```
**Effect**: Subtle grain adds tactile quality. Reduces harsh gradients.

## Copy-Paste Ready Examples

### Premium Dark Mode
```css
background:
  radial-gradient(circle at 15% 25%, rgba(139, 92, 246, 0.25), transparent 50%),
  linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
background-attachment: fixed;
```

### Ocean Atmosphere
```css
background:
  radial-gradient(ellipse at 50% 0%, rgba(59, 130, 246, 0.3), transparent 60%),
  linear-gradient(180deg, #164e63 0%, #0c2340 100%);
```

### Forest Depth
```css
background:
  radial-gradient(circle at 30% 50%, rgba(34, 197, 94, 0.2), transparent 50%),
  radial-gradient(circle at 70% 30%, rgba(99, 102, 241, 0.15), transparent 50%),
  linear-gradient(135deg, #1e293b, #0f172a);
background-attachment: fixed;
```

## Anti-Patterns to Avoid

### Cliché Color Schemes
- Material Design Trinity: Blue, Red, Green as primary, secondary, accent
- Default SaaS Colors: Cool blues (#0099ff, #0066cc) everywhere
- Rainbow Palette: Every color at full saturation
- Pure Grays: #999999, #CCCCCC without personality
- Inverted Black/White: No mid-tones or color

### Monochrome Everything
```css
/* AVOID */
background: #f5f5f5;
color: #333333;
accent: #0099ff;
```
**Result**: Feels corporate and soulless.

### Oversaturated Accent Colors
- Neon colors at 100% saturation
- Colors that don't exist in real life
- Accents that compete with content

## Implementation Tips

- Use `background-attachment: fixed` for parallax effect on scroll
- Limit to 3-4 layers max for performance
- Test on mobile before shipping
- Reduce opacity (0.1-0.3) for subtle effects
- Layer light gradients over dark base for better composition
- Always test text contrast on finished gradient
