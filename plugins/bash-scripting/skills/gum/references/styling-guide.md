# Gum Styling Guide

Comprehensive guide to theming, customization, and styling in gum.

## Styling Overview

Gum uses [Lip Gloss](https://github.com/charmbracelet/lipgloss) for styling, which provides a declarative, CSS-like approach to terminal formatting. All gum commands support customization through:

1. **Command-line flags** - Direct styling options
2. **Environment variables** - Persistent configuration with `GUM_*` prefix
3. **Themes** - Pre-defined color schemes (for format command)

## Color Specification

### Color Formats

Gum accepts colors in multiple formats:

```bash
# ANSI color codes (0-255)
gum style --foreground 212 "Text"

# Hex colors
gum style --foreground "#FF00FF" "Text"

# Named colors
gum style --foreground "pink" "Text"
```

### Common ANSI Colors

| Code | Color | Code | Color |
|------|-------|------|-------|
| 0 | Black | 8 | Bright Black |
| 1 | Red | 9 | Bright Red |
| 2 | Green | 10 | Bright Green |
| 3 | Yellow | 11 | Bright Yellow |
| 4 | Blue | 12 | Bright Blue |
| 5 | Magenta | 13 | Bright Magenta |
| 6 | Cyan | 14 | Bright Cyan |
| 7 | White | 15 | Bright White |

Popular accent colors:
- `212` - Pink/Magenta
- `57` - Purple
- `99` - Purple/Blue
- `240` - Gray

## Environment Variables

### Configuration Pattern

All gum commands can be configured using environment variables with the pattern:

```
GUM_<COMMAND>_<PROPERTY>="value"
```

Flags always override environment variables.

### Common Variables by Command

#### `gum input`

```bash
export GUM_INPUT_CURSOR_FOREGROUND="#FF0"
export GUM_INPUT_PROMPT_FOREGROUND="#0FF"
export GUM_INPUT_PLACEHOLDER="Enter text..."
export GUM_INPUT_PROMPT="> "
export GUM_INPUT_WIDTH=80
export GUM_INPUT_PASSWORD=false
```

#### `gum choose`

```bash
export GUM_CHOOSE_CURSOR="> "
export GUM_CHOOSE_CURSOR_FOREGROUND=212
export GUM_CHOOSE_SELECTED_FOREGROUND=212
export GUM_CHOOSE_HEIGHT=10
export GUM_CHOOSE_LIMIT=1
```

#### `gum filter`

```bash
export GUM_FILTER_INDICATOR="→ "
export GUM_FILTER_MATCH_FOREGROUND=212
export GUM_FILTER_PLACEHOLDER="Search..."
export GUM_FILTER_HEADER="Select items:"
export GUM_FILTER_HEIGHT=20
```

#### `gum confirm`

```bash
export GUM_CONFIRM_SELECTED_FOREGROUND=212
export GUM_CONFIRM_UNSELECTED_FOREGROUND=240
export GUM_CONFIRM_PROMPT="Are you sure?"
export GUM_CONFIRM_AFFIRMATIVE="Yes"
export GUM_CONFIRM_NEGATIVE="No"
```

#### `gum write`

```bash
export GUM_WRITE_WIDTH=80
export GUM_WRITE_HEIGHT=10
export GUM_WRITE_PLACEHOLDER="Enter text..."
export GUM_WRITE_CHAR_LIMIT=0
export GUM_WRITE_SHOW_CURSOR_LINE=false
```

#### `gum spin`

```bash
export GUM_SPIN_SPINNER="dot"
export GUM_SPIN_TITLE="Loading..."
export GUM_SPIN_SHOW_OUTPUT=false
export GUM_SPIN_ALIGN="left"
```

## Styling Commands

### `gum style` - Complete Styling Reference

#### Text Colors

```bash
# Foreground color
gum style --foreground 212 "Colored text"

# Background color
gum style --background 240 "With background"

# Both
gum style --foreground 212 --background 240 "Full colors"
```

#### Text Formatting

```bash
# Bold
gum style --bold "Bold text"

# Italic
gum style --italic "Italic text"

# Underline
gum style --underline "Underlined text"

# Strikethrough
gum style --strikethrough "Struck text"

# Combine multiple
gum style --bold --italic --underline "All styles"
```

#### Borders

Border styles: `none`, `hidden`, `normal`, `rounded`, `thick`, `double`

```bash
# Basic border
gum style --border rounded "Bordered text"

# With border color
gum style --border double --border-foreground 212 "Colored border"

# Individual border sides
gum style --border normal \
          --border.top true \
          --border.bottom true \
          --border.left false \
          --border.right false \
          "Top and bottom only"
```

#### Layout and Spacing

```bash
# Width and height
gum style --width 50 --height 10 "Fixed size"

# Alignment (left, center, right)
gum style --align center --width 50 "Centered"

# Padding (top/bottom left/right)
gum style --padding "2 4" "Padded text"

# Margin (top/bottom left/right)
gum style --margin "1 2" "With margin"
```

#### Complete Example

```bash
gum style \
  --foreground 212 \
  --border-foreground 212 \
  --border double \
  --align center \
  --width 50 \
  --margin "1 2" \
  --padding "2 4" \
  --bold \
  'Bubble Gum (1¢)' \
  'So sweet and so fresh!'
```

### `gum format` - Theming

#### Available Themes

```bash
# Markdown themes
gum format --theme dark < document.md
gum format --theme light < document.md
gum format --theme dracula < document.md
gum format --theme monokai < document.md
gum format --theme nord < document.md
gum format --theme tokyo-night < document.md
```

#### Code Syntax Highlighting

```bash
# Auto-detect language
cat code.go | gum format -t code

# Specify language
gum format --language go --theme monokai < code.go
gum format --language python --theme dracula < script.py
gum format --language javascript --theme nord < app.js
```

## Creating Themed Scripts

### Method 1: Environment Variables

Create a theme configuration file:

```bash
# theme.sh
export GUM_INPUT_CURSOR_FOREGROUND="#FF00FF"
export GUM_INPUT_PROMPT_FOREGROUND="#00FFFF"
export GUM_CHOOSE_CURSOR_FOREGROUND=212
export GUM_CHOOSE_SELECTED_FOREGROUND=212
export GUM_FILTER_MATCH_FOREGROUND=212
export GUM_CONFIRM_SELECTED_FOREGROUND=212
export GUM_STYLE_FOREGROUND=212
export GUM_STYLE_BORDER_FOREGROUND=212
```

Use in script:

```bash
#!/bin/bash
source theme.sh

NAME=$(gum input --placeholder "Your name")
CHOICE=$(gum choose "Option 1" "Option 2" "Option 3")
```

### Method 2: Helper Functions

```bash
#!/bin/bash

# Define color palette
PRIMARY=212
SECONDARY=57
ACCENT=99
MUTED=240

# Helper function for styled boxes
styled_box() {
  gum style \
    --border rounded \
    --border-foreground "$PRIMARY" \
    --padding "1 2" \
    --margin "1" \
    "$@"
}

# Helper function for headers
header() {
  gum style \
    --foreground "$PRIMARY" \
    --bold \
    --margin "1 0" \
    "$@"
}

# Use helpers
header "Welcome to My App"
styled_box "This is a styled message"
```

## Component-Specific Styling

### Input Components

#### `gum input` Styling

```bash
# Minimal style
gum input \
  --placeholder "Enter text..." \
  --prompt "> " \
  --width 60

# Colorful style
gum input \
  --cursor.foreground "#FF00FF" \
  --prompt.foreground "#00FFFF" \
  --placeholder "Type something..." \
  --prompt "➜ " \
  --width 80
```

#### `gum write` Styling

```bash
# Simple text area
gum write \
  --width 80 \
  --height 15 \
  --placeholder "Enter your text..."

# With styling
gum write \
  --base-style "foreground:212" \
  --cursor-line-number-style "foreground:240" \
  --line-number-style "foreground:240" \
  --show-cursor-line \
  --show-line-numbers
```

### Selection Components

#### `gum choose` Styling

```bash
# Custom cursor and colors
gum choose \
  --cursor "→ " \
  --cursor.foreground 212 \
  --selected.foreground 212 \
  --unselected.foreground 240 \
  --height 10 \
  "Option 1" "Option 2" "Option 3"
```

#### `gum filter` Styling

```bash
# Styled fuzzy finder
gum filter \
  --indicator "→ " \
  --indicator.foreground 212 \
  --match.foreground 212 \
  --selected-indicator.foreground 212 \
  --placeholder "Search..." \
  --placeholder.foreground 240 \
  --header "Select file:" \
  --header.foreground 99
```

### Display Components

#### `gum table` Styling

```bash
# Styled table
gum table \
  --border rounded \
  --border.foreground 212 \
  --cell.foreground 240 \
  --header.foreground 212 \
  --selected.foreground 212 \
  --columns "Name,Age,City" \
  --widths 20,10,15 \
  < data.csv
```

#### `gum pager` Styling

```bash
# Styled pager
gum pager \
  --border rounded \
  --border.foreground 212 \
  --line-number.foreground 240 \
  --match-style "foreground:212,bold" \
  --match-highlight-style "foreground:212,bold,underline" \
  --show-line-numbers \
  < document.md
```

### Logging Styles

#### `gum log` Styling

```bash
# Custom log styling
gum log \
  --level.foreground 212 \
  --message.foreground 240 \
  --message.bold true \
  --level info "Log message"

# Structured with colors
gum log \
  --structured \
  --level error \
  --level.foreground 9 \
  --key.foreground 240 \
  --value.foreground 212 \
  "Error occurred" \
  file "config.json" \
  line 42
```

## Layout Composition

### Using `gum join`

#### Horizontal Layouts

```bash
# Side-by-side boxes
LEFT=$(gum style --border rounded --border-foreground 212 --padding "1 2" "Left")
RIGHT=$(gum style --border rounded --border-foreground 57 --padding "1 2" "Right")
gum join --horizontal "$LEFT" "$RIGHT"
```

#### Vertical Layouts

```bash
# Stacked sections
HEADER=$(gum style --bold --foreground 212 --align center --width 50 "Header")
BODY=$(gum style --foreground 240 --align left --width 50 "Body content")
FOOTER=$(gum style --italic --foreground 240 --align center --width 50 "Footer")
gum join --vertical "$HEADER" "$BODY" "$FOOTER"
```

#### Grid Layouts

```bash
# Create a 2x2 grid
TL=$(gum style --border rounded --border-foreground 212 --padding "1 2" "Top Left")
TR=$(gum style --border rounded --border-foreground 57 --padding "1 2" "Top Right")
BL=$(gum style --border rounded --border-foreground 99 --padding "1 2" "Bottom Left")
BR=$(gum style --border rounded --border-foreground 240 --padding "1 2" "Bottom Right")

TOP_ROW=$(gum join --horizontal "$TL" "$TR")
BOTTOM_ROW=$(gum join --horizontal "$BL" "$BR")
gum join --vertical "$TOP_ROW" "$BOTTOM_ROW"
```

## Best Practices

### Color Consistency

```bash
# Define colors at the top of your script
PRIMARY_COLOR=212
SECONDARY_COLOR=57
ACCENT_COLOR=99
MUTED_COLOR=240
ERROR_COLOR=9
SUCCESS_COLOR=10
WARNING_COLOR=11

# Use consistently throughout
gum style --foreground "$PRIMARY_COLOR" "Important"
gum choose --cursor.foreground "$PRIMARY_COLOR" "Option 1" "Option 2"
```

### Responsive Widths

```bash
# Get terminal width
TERM_WIDTH=$(tput cols)

# Use percentage of terminal width
INPUT_WIDTH=$((TERM_WIDTH * 80 / 100))
gum input --width "$INPUT_WIDTH" --placeholder "Enter text..."
```

### Accessible Design

```bash
# Use sufficient contrast
gum style --foreground 15 --background 0 "High contrast"

# Avoid relying solely on color
gum style --bold --foreground 9 "❌ Error" # Icon + color + bold
gum style --bold --foreground 10 "✓ Success" # Icon + color + bold
```

### Consistent Spacing

```bash
# Standard padding for boxes
PADDING="1 2"  # 1 vertical, 2 horizontal

# Standard margin for sections
MARGIN="1 0"   # 1 vertical, 0 horizontal

gum style --padding "$PADDING" --margin "$MARGIN" "Content"
```

## Complete Themed Example

```bash
#!/bin/bash

# Color Palette
PRIMARY=212
SECONDARY=57
ACCENT=99
MUTED=240

# Theme Configuration
export GUM_INPUT_CURSOR_FOREGROUND="$PRIMARY"
export GUM_INPUT_PROMPT_FOREGROUND="$ACCENT"
export GUM_CHOOSE_CURSOR_FOREGROUND="$PRIMARY"
export GUM_FILTER_MATCH_FOREGROUND="$PRIMARY"

# Helper Functions
title() {
  gum style \
    --foreground "$PRIMARY" \
    --bold \
    --border double \
    --border-foreground "$PRIMARY" \
    --padding "1 2" \
    --margin "1 0" \
    --align center \
    --width 60 \
    "$@"
}

section() {
  gum style \
    --foreground "$ACCENT" \
    --bold \
    --margin "1 0" \
    "$@"
}

info() {
  gum style \
    --foreground "$MUTED" \
    --margin "0 2" \
    "$@"
}

# Application
title "My Themed Application"

section "User Information"
NAME=$(gum input --prompt "Name: " --placeholder "Enter your name")

section "Select Option"
OPTION=$(gum choose --header "Choose one:" "Option A" "Option B" "Option C")

section "Additional Details"
DETAILS=$(gum write --placeholder "Enter details..." --height 5)

section "Summary"
info "Name: $NAME"
info "Option: $OPTION"
info "Details: $DETAILS"

gum confirm "Submit?" && echo "Submitted!" || echo "Cancelled"
```

## Debugging Styles

### View All Styles

```bash
# Test different colors
for i in {0..255}; do
  gum style --foreground "$i" "Color $i"
done

# Test borders
for border in none normal rounded thick double; do
  gum style --border "$border" "Border: $border"
done
```

### Check Environment Variables

```bash
# List all GUM_ variables
env | grep GUM_

# Clear all GUM_ variables
unset $(env | grep GUM_ | cut -d= -f1)
```
