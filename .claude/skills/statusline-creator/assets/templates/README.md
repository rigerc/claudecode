# Statusline Templates

Pre-built statusline configurations ready to use. Install any template using the install script:

```bash
./scripts/install_statusline.sh <template-name>
```

## Available Templates

### minimal
**Best for**: Distraction-free work, small terminals

Simple, clean statusline with just directory name and git branch.

Preview: `my-project main`

### git-focused
**Best for**: Git-heavy workflows, version control emphasis

Highlights git information with color-coded status indicators.

Preview: `~/workspace/project │ ⎇ main ✓`

Features:
- Full path with home directory abbreviation
- Git branch with symbol
- Status indicator (✓ clean, ± modified)

### full-featured
**Best for**: Maximum information density, wide terminals

Comprehensive statusline with user, host, directory, git, and time.

Preview: `user@machine │ project │ main ✓ │ 14:23:45`

Features:
- Username and hostname
- Directory name
- Git branch and status
- Current time

### powerline
**Best for**: Modern, stylish appearance with segmented design

Powerline-inspired design with background colors and arrow separators.

Preview: ` project ❯ main ❯` (with dark backgrounds)

Features:
- Segmented backgrounds
- Arrow separators
- True color support

### modern-clean
**Best for**: Balanced information with elegant aesthetics

Clean, modern design with subtle separators and color accents.

Preview: `❯ project · main ●`

Features:
- Colored prompt indicator
- Minimal separators
- Status dots (green = clean, yellow = modified)

### developer
**Best for**: Development work with system metrics

Developer-focused statusline with git changes count and system load.

Preview: `project │ main ✓ │ 14:23 │ 1.2`

Features:
- Changed files count
- System load average
- Compact time display

## Customization

All templates can be customized by:

1. Installing the base template:
   ```bash
   ./scripts/install_statusline.sh minimal
   ```

2. Editing `~/.claude/settings.json` to modify the `statusline.format` field

3. Testing your changes:
   ```bash
   ./scripts/test_statusline.py --config ~/.claude/settings.json --preview
   ```

## Creating Custom Templates

To create your own template:

1. Create a new JSON file in this directory:
   ```json
   {
     "statusline": {
       "format": "your statusline string here"
     }
   }
   ```

2. Test it:
   ```bash
   ./scripts/test_statusline.py "your statusline" --preview
   ```

3. Install it:
   ```bash
   ./scripts/install_statusline.sh my-custom-template
   ```

Refer to `references/statusline_format.md` for formatting details and `references/best_practices.md` for design guidance.
