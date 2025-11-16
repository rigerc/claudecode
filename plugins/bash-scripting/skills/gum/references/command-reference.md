# Gum Command Reference

Complete reference for all gum commands with examples and usage patterns.

## Input Commands

### `gum input` - Single-line Text Input

Prompts for single-line text input with support for placeholders, default values, and password masking.

**Basic Usage:**

```bash
# Simple input
gum input --placeholder "Enter your name"

# Capture to variable
NAME=$(gum input --placeholder "Enter your name")

# Save to file
gum input --placeholder "Enter your name" > name.txt
```

**Password Input:**

```bash
# Masked password input
gum input --password --placeholder "Enter password" > password.txt

# Use in sudo replacement
alias please="gum input --password | sudo -nS"
```

**With Default Value:**

```bash
# Pre-fill input with value
gum input --value "default text" --placeholder "Edit this"
```

**Custom Styling:**

```bash
# Customize colors and appearance
gum input --cursor.foreground "#FF0" \
          --prompt.foreground "#0FF" \
          --placeholder "What's up?" \
          --prompt "* " \
          --width 80
```

**Environment Variables:**

```bash
export GUM_INPUT_CURSOR_FOREGROUND="#FF0"
export GUM_INPUT_PROMPT_FOREGROUND="#0FF"
export GUM_INPUT_PLACEHOLDER="What's up?"
export GUM_INPUT_PROMPT="* "
export GUM_INPUT_WIDTH=80

# Flags can override environment variables
gum input
```

### `gum write` - Multi-line Text Input

Provides a text area for multi-line input. Complete with `Ctrl+D`, abort with `Ctrl+C` or `Escape`.

**Basic Usage:**

```bash
# Multi-line input to file
gum write > story.txt

# With placeholder
gum write --placeholder "Enter your story here..." > output.txt
```

**Custom Dimensions:**

```bash
# Set width and height
gum write --width 80 --height 20 > article.txt
```

**Git Commit Example:**

```bash
# Combine with gum input for commit messages
git commit -m "$(gum input --placeholder "Summary")" \
           -m "$(gum write --placeholder "Details")"
```

**Advanced Options:**

```bash
# Show cursor line and set character limit
gum write --show-cursor-line \
          --char-limit 500 \
          --base-style "foreground:212" > description.txt
```

## Selection Commands

### `gum choose` - Select from List

Presents options for single or multiple selections without fuzzy matching.

**Single Choice:**

```bash
# Basic selection
TYPE=$(gum choose "fix" "feat" "docs" "style" "refactor" "test")

# Expanded example
CARD=$(gum choose --height 15 {{A,K,Q,J},{10..2}}" "{♠,♥,♣,♦})
echo "Was your card the $CARD?"
```

**Multiple Selections:**

```bash
# With selection limit
gum choose --limit 5 "Strawberry" "Banana" "Cherry" "Grape" "Apple"

# Unlimited selections
cat foods.txt | gum choose --no-limit --header "Grocery Shopping"
```

**Pre-selected Options:**

```bash
# Pre-select specific items
gum choose --selected "Apple" --selected "Banana" \
  "Apple" "Banana" "Cherry" "Date" "Elderberry"
```

**Custom Styling:**

```bash
# Customize cursor and selection colors
gum choose --cursor "> " \
           --cursor.foreground 212 \
           --selected.foreground 212 \
           "Option 1" "Option 2" "Option 3"
```

**Real-World Examples:**

```bash
# Delete git branches
git branch | cut -c 3- | gum choose --no-limit | xargs git branch -D

# Uninstall packages
brew list | gum choose --no-limit | xargs brew uninstall

# Checkout GitHub PR
gh pr list | cut -f1,2 | gum choose | cut -f1 | xargs gh pr checkout
```

### `gum filter` - Fuzzy Search and Filter

Enables fuzzy searching to filter items, supporting multiple selections and exact/fuzzy matching.

**Basic Usage:**

```bash
# Filter from file
echo "Strawberry" >> flavors.txt
echo "Banana" >> flavors.txt
echo "Cherry" >> flavors.txt
gum filter < flavors.txt > selection.txt
```

**Multiple Selections:**

```bash
# With limit
cat flavors.txt | gum filter --limit 2

# Unlimited
cat flavors.txt | gum filter --no-limit
```

**File Selection:**

```bash
# Open selected file in editor
$EDITOR $(gum filter)
```

**Custom Styling:**

```bash
# With header and custom appearance
gum filter --header "Select files:" \
           --placeholder "Search..." \
           --indicator "→ " \
           --match.foreground 212 \
           < file_list.txt
```

**Real-World Examples:**

```bash
# Filter shell history
gum filter < $HISTFILE --height 20

# Filter git commits
git log --oneline | gum filter | cut -d' ' -f1

# Filter and checkout git branches
git branch | cut -c 3- | gum filter | xargs git checkout

# Connect to tmux session
SESSION=$(tmux list-sessions -F \#S | gum filter --placeholder "Pick session...")
tmux switch-client -t "$SESSION" || tmux attach -t "$SESSION"
```

### `gum file` - Navigate and Select Files

Interactive file manager for navigating directories and selecting files.

**Basic Usage:**

```bash
# Pick file from current directory
gum file

# Pick from specific directory
gum file $HOME

# Open in editor
$EDITOR $(gum file)
```

**Advanced Options:**

```bash
# Select from specific path
gum file /etc/

# With custom height
gum file --height 20 ~/projects/

# Show all files including hidden
gum file --all ~/Documents/
```

### `gum confirm` - Yes/No Confirmation

Asks for user confirmation, returns exit code 0 for yes, 1 for no.

**Basic Usage:**

```bash
# Simple confirmation
gum confirm && rm file.txt || echo "File not removed"

# Custom text
gum confirm "Delete all files?" \
  --affirmative="Yes, delete!" \
  --negative="No, keep them"
```

**Conditional Execution:**

```bash
# Use in if statement
if gum confirm "Deploy to production?"; then
  ./deploy.sh
else
  echo "Deployment cancelled"
fi

# Git commit example
gum confirm "Commit changes?" && git commit -m "$SUMMARY" -m "$DESCRIPTION"
```

**Custom Styling:**

```bash
# Style selected and unselected options
gum confirm "Continue?" \
  --selected.foreground=212 \
  --unselected.foreground=240
```

## Display Commands

### `gum style` - Apply Colors and Formatting

Applies colors, borders, alignment, padding, and margins to text using Lip Gloss.

**Basic Styling:**

```bash
# Simple colored text
gum style --foreground 212 "Bubble Gum"

# Bold and colored
gum style --bold --foreground 99 "Important Message"

# Multiple formatting
gum style --italic --underline --foreground 212 "Styled Text"
```

**Borders and Layout:**

```bash
# With border and layout options
gum style \
  --foreground 212 --border-foreground 212 --border double \
  --align center --width 50 --margin "1 2" --padding "2 4" \
  'Bubble Gum (1¢)' 'So sweet and so fresh!'

# Create bordered box
BOX=$(gum style --border rounded --border-foreground 57 \
               --padding "1 2" --width 30 "Box Content")
echo "$BOX"
```

### `gum format` - Process and Style Text

Processes markdown, code, templates, and emojis with syntax highlighting.

**Markdown Formatting:**

```bash
# Format markdown from arguments
gum format -- "# Gum Formats" "- Markdown" "- Code" "- Template" "- Emoji"

# From stdin
echo "# Title
## Subtitle
- List item" | gum format

# From file with theme
gum format --theme dark < document.md
gum format --theme light < README.md
```

**Code Syntax Highlighting:**

```bash
# Highlight code with language detection
cat main.go | gum format -t code

# Specify language
gum format --language go < code.go
```

**Template Processing:**

```bash
# Process template with styling functions
echo '{{ Bold "Tasty" }} {{ Italic "Bubble" }} {{ Color "99" "0" " Gum " }}' \
  | gum format -t template
```

**Emoji Rendering:**

```bash
# Render emojis from :name: format
echo 'I :heart: Bubble Gum :candy:' | gum format -t emoji
```

### `gum join` - Combine Text Horizontally or Vertically

Combines multiple text elements for complex layouts.

**Horizontal Join:**

```bash
I=$(gum style --padding "1 5" --border double --border-foreground 212 "I")
LOVE=$(gum style --padding "1 4" --border double --border-foreground 57 "LOVE")
gum join --horizontal "$I" "$LOVE"
```

**Vertical Join:**

```bash
HEADER=$(gum style --bold --foreground 212 "Header")
CONTENT=$(gum style --foreground 240 "Content here")
gum join --vertical "$HEADER" "$CONTENT"
```

**Complex Layouts:**

```bash
I=$(gum style --padding "1 5" --border double --border-foreground 212 "I")
LOVE=$(gum style --padding "1 4" --border double --border-foreground 57 "LOVE")
BUBBLE=$(gum style --padding "1 8" --border double --border-foreground 255 "Bubble")
GUM=$(gum style --padding "1 5" --border double --border-foreground 240 "Gum")

I_LOVE=$(gum join "$I" "$LOVE")
BUBBLE_GUM=$(gum join "$BUBBLE" "$GUM")
gum join --align center --vertical "$I_LOVE" "$BUBBLE_GUM"
```

### `gum pager` - Scroll Through Content

Displays content in a scrollable viewport with line numbers and search.

**Basic Usage:**

```bash
# Basic paging
gum pager < README.md

# Custom dimensions
gum pager --height 20 --width 80 < large_file.txt
```

**Advanced Features:**

```bash
# With line numbers
gum pager --show-line-numbers < code.go

# Soft wrap long lines
gum pager --soft-wrap < log_file.txt

# Custom styling for search matches
gum pager --match-style "foreground:212" \
          --match-highlight-style "foreground:212,bold" \
          < document.md
```

### `gum table` - Render Tabular Data

Renders and allows selection from CSV or tabular data.

**Basic Usage:**

```bash
# Basic table from CSV
gum table <<< "Flavor,Price\nStrawberry,$0.50\nBanana,$0.99\nCherry,$0.75"

# Select row and extract field
gum table < data.csv | cut -d ',' -f 1
```

**From File:**

```bash
# With custom separator
gum table --separator="|" --file data.txt
```

**Custom Styling:**

```bash
# Configure columns and appearance
gum table --columns "Name,Age,City" \
          --widths 20,10,15 \
          --border rounded \
          --border.foreground 212 < users.csv
```

**Print Mode:**

```bash
# Display without selection
gum table --print < report.csv
```

## Utility Commands

### `gum spin` - Display Spinner

Shows spinner animation while running commands.

**Basic Usage:**

```bash
# Basic spinner with command
gum spin --spinner dot --title "Buying Bubble Gum..." -- sleep 5

# Show command output
gum spin --spinner line --title "Installing packages..." \
         --show-output -- npm install
```

**Spinner Styles:**

Available spinner types: `line`, `dot`, `minidot`, `jump`, `pulse`, `points`, `globe`, `moon`, `monkey`, `meter`, `hamburger`

```bash
# Different spinner styles
gum spin --spinner globe --title "Processing..." -- ./long_task.sh
gum spin --spinner moon --title "Loading..." -- curl https://api.example.com
```

**With Alignment:**

```bash
# Align spinner
gum spin --spinner dot --title "Working..." --align right -- make build
```

### `gum log` - Structured Logging

Logs messages with severity levels and structured data using charmbracelet/log.

**Basic Logging:**

```bash
# Simple log messages
gum log --level info "Application started"
gum log --level error "Failed to connect to database"
```

**Structured Logging:**

```bash
# With structured fields
gum log --structured --level debug "Creating file..." name file.txt
gum log --structured --level error "Unable to create file." name file.txt
```

**Timestamps:**

```bash
# Include timestamps (see Go time package for formats)
gum log --time rfc822 --level info "Processing request"
gum log --time "2006-01-02 15:04:05" --level warn "High memory usage"
```

**Custom Styling:**

```bash
# Custom log styling
gum log --level.foreground 212 --message.bold true \
        --level info "Styled log message"
```

**Different Formatters:**

```bash
# JSON output
gum log --formatter json --structured --level info "Event occurred" user "john"

# logfmt output
gum log --formatter logfmt --structured --level debug "Query executed" duration 45
```

**Log to File:**

```bash
# Redirect to file
gum log --file app.log --level error "Critical error occurred"
```

## Complete Examples

### Interactive Git Commit

```bash
TYPE=$(gum choose "fix" "feat" "docs" "style" "refactor" "test")
SCOPE=$(gum input --placeholder "scope")
SUMMARY=$(gum input --placeholder "Summary of changes")
DESCRIPTION=$(gum write --placeholder "Detailed description (Ctrl+D to finish)")
gum confirm "Commit changes?" && git commit -m "$TYPE($SCOPE): $SUMMARY" -m "$DESCRIPTION"
```

### Git Commit with Width Constraints

```bash
git commit -m "$(gum input --width 50 --placeholder "Summary of changes")" \
           -m "$(gum write --width 80 --placeholder "Details of changes")"
```

### Complex Layout

```bash
I=$(gum style --padding "1 5" --border double --border-foreground 212 "I")
LOVE=$(gum style --padding "1 4" --border double --border-foreground 57 "LOVE")
BUBBLE=$(gum style --padding "1 8" --border double --border-foreground 255 "Bubble")
GUM=$(gum style --padding "1 5" --border double --border-foreground 240 "Gum")

I_LOVE=$(gum join "$I" "$LOVE")
BUBBLE_GUM=$(gum join "$BUBBLE" "$GUM")
gum join --align center --vertical "$I_LOVE" "$BUBBLE_GUM"
```
