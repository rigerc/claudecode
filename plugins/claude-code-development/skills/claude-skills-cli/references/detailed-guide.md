---
name: claude-skills-cli
description: Creating and managing Claude Agent Skills using claude-skills-cli CLI tool with progressive disclosure validation. Use when users ask to create skills, validate skill structure, or need reliable skill activation methods.
allowed-tools: Bash, Write, Read, Edit, Glob
---

# Claude Skills CLI

## Overview
Using claude-skills-cli to create, validate, and manage Claude Agent Skills with progressive disclosure validation. This CLI tool enforces proper skill structure, validates content constraints, and provides reliable skill activation solutions.

## When to Use
Use this skill when users:
- Ask to create new Claude Agent Skills
- Need help with skill validation or structure
- Want to ensure skills activate reliably in Claude Code
- Need to package or share skills
- Are having trouble with skill discovery/activation

## Key Concepts

### Progressive Disclosure System
Skills load in 3 levels to optimize tokens:
- **Level 1**: SKILL.md metadata (always in context, <200 chars)
- **Level 2**: SKILL.md body (when skill triggers, ~50 lines)
- **Level 3**: references/, scripts/, assets/ (as needed)

### Activation Reliability
Skills often don't auto-activate reliably. Use explicit hooks for guaranteed activation.

## Core Workflows

### 1. Creating New Skills

#### Step 1: Choose Save Location
Before creating a skill, determine where to save it:

**Save Location Options:**
- **Project Skills** (`.claude/skills/`): Team-shared, committed to git
- **Personal Skills** (`~/.claude/skills/`): Individual, across all projects
- **Project Plugin Skills** (`plugins/[plugin]/skills/`): Bundled with plugins (if `plugins/` directory exists)

**Choosing the Right Location:**
- Use **Project** for team workflows and shared utilities
- Use **Personal** for individual preferences and experimental skills
- Use **Project Plugin** when developing skills to distribute with a plugin

#### Step 2: Create Skill Scaffolding
You have two options for creating skill scaffolding:

**Option 1: Create with name (creates in current directory)**
```bash
# Create minimal skill scaffolding
npx claude-skills-cli init --name my-skill --description "Brief description with trigger keywords"

# Create with example files
npx claude-skills-cli init --name my-skill --description "..." --with-examples
```

**Option 2: Create with path (creates directly at target location - use full/absolute paths)**
```bash
# Create at specific location (no move needed) - always use full paths
npx claude-skills-cli init --path /full/path/to/.claude/skills/my-skill --description "Brief description with trigger keywords"

# Create with examples at target location
npx claude-skills-cli init --path /full/path/to/.claude/skills/my-skill --description "..." --with-examples
```

#### Step 3: Move to Desired Location (if using --name option)
The CLI creates skills in the current directory when using `--name`. Move them to the chosen location:

```bash
# For project skills
mv my-skill .claude/skills/

# For personal skills
mv my-skill ~/.claude/skills/

# For plugin skills (identify plugin directory first)
ls plugins/  # See available plugins
mv my-skill plugins/[plugin-name]/skills/
```

**Note**: When using `--path`, skills are created directly at the target location, eliminating the need to move them.

#### Skill Structure Validation
The CLI enforces:
- Name format (kebab-case, matches directory)
- YAML frontmatter validity
- Required fields presence
- Description length optimization (<200 chars)
- Progressive disclosure structure

### 2. Validation Workflow

#### Comprehensive Validation
```bash
# Basic validation (use full paths)
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill

# Strict validation (fail on warnings)
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill --strict

# JSON output for automation
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill --format json
```

#### Validation Checks
- **Structure & Format**: Name matching, YAML validity, required fields
- **Level 1 (Metadata)**: Description length, trigger phrases, keyword richness
- **Level 2 (Body)**: Line count (~50 target), word count, code blocks, sections
- **Level 3 (References)**: File existence, orphaned files, nesting depth

### 3. Issue Resolution

#### Auto-fix Common Issues
```bash
# Use full paths
npx claude-skills-cli doctor /full/path/to/.claude/skills/my-skill
```

The doctor fixes:
- Multi-line descriptions (adds prettier-ignore, reflows to single line)
- Ensures Claude Code recognition
- Common structural issues

### 4. Skill Activation

#### Reliable Activation Setup
```bash
# Add global hook (recommended - applies to all projects)
npx claude-skills-cli add-hook

# Project-specific hook (committed to git)
npx claude-skills-cli add-hook --project

# Local hook (gitignored, personal)
npx claude-skills-cli add-hook --local
```

#### Why Explicit Hooks Matter
- Skills often don't auto-activate despite documentation claims
- Explicit "INSTRUCTION:" prefix is critical for reliability
- Hooks tell Claude to check AND activate skills using Skill() syntax
- Scales automatically with new skills (no keyword management needed)

### 5. Management Operations

#### View Skill Statistics
```bash
# Use full paths
npx claude-skills-cli stats /full/path/to/.claude/skills
```

#### Package for Distribution
```bash
# Use full paths
npx claude-skills-cli package /full/path/to/.claude/skills/my-skill
```

## Best Practices

### Location Selection Guidelines
1. **Always Ask First**: Before creating skills, ask users where they want to save them
2. **Explain Options**: Clearly describe the differences between project, personal, and plugin locations
3. **Consider Use Case**:
   - Team workflows → Project skills
   - Individual preferences → Personal skills
   - Distribution needs → Plugin skills
4. **Detect Plugin Directory**: Check for `plugins/` directory before suggesting plugin option

### Skill Creation Guidelines
1. **Start Simple**: Use init command, validate frequently
2. **Focus Description**: Include what skill does AND when to use it
3. **Progressive Disclosure**: Keep core instructions minimal, move details to references
4. **Test Activation**: Always add hooks for reliability

### Validation Strategy
1. **Validate Early**: Run validation after each major change
2. **Use Strict Mode**: For production-ready skills
3. **Check Dependencies**: Ensure referenced files exist
4. **Monitor Stats**: Use stats command to track skill quality

### Content Optimization
1. **Description Length**: Target <200 characters for optimal discovery
2. **Body Length**: Aim for ~50 lines, maximum 150 lines
3. **Code Blocks**: 1-2 optimal, avoid excessive code
4. **Sections**: 3-5 recommended sections for organization

## Common Issues & Solutions

### Skills Not Activating
**Problem**: Claude doesn't use the skill
**Solution**:
```bash
npx claude-skills-cli add-hook  # Add explicit activation hook
```

### Multi-line Descriptions
**Problem**: Validation warns about multi-line descriptions
**Solution**:
```bash
# Use full paths
npx claude-skills-cli doctor /full/path/to/.claude/skills/my-skill
```

### Validation Failures
**Problem**: Skills don't pass validation
**Solution**:
1. Run validation with detailed output
2. Check file structure matches requirements
3. Verify YAML syntax in frontmatter
4. Ensure description specificity

## Examples

### Example 1: Project Skill for Team Workflow
```bash
# Step 1: Create skill scaffolding directly at target location (use full path)
npx claude-skills-cli init \
  --path /full/path/to/.claude/skills/api-client-helper \
  --description "Creating and configuring API client code for REST services. Use when working with HTTP requests, API authentication, or client libraries."

# Step 2: Validate with strict mode (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/api-client-helper --strict

# Step 3: Ensure reliable activation for team
npx claude-skills-cli add-hook --project
```

**Alternative (using --name option):**
```bash
# Step 1: Create skill scaffolding with name
npx claude-skills-cli init \
  --name api-client-helper \
  --description "Creating and configuring API client code for REST services. Use when working with HTTP requests, API authentication, or client libraries."

# Step 2: Move to project location (team-shared)
mv api-client-helper /full/path/to/.claude/skills/

# Step 3: Validate with strict mode (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/api-client-helper --strict

# Step 4: Ensure reliable activation for team
npx claude-skills-cli add-hook --project
```

### Example 2: Personal Skill for Individual Use
```bash
# Step 1: Create skill scaffolding with examples at target location (~ expands to full home path)
npx claude-skills-cli init \
  --path ~/.claude/skills/data-processor \
  --description "Processing and analyzing data files in CSV, JSON, and Excel formats. Use for data cleaning, transformation, and analysis tasks." \
  --with-examples

# Step 2: Fix any formatting issues (~ expands to full path)
npx claude-skills-cli doctor ~/.claude/skills/data-processor

# Step 3: Check overall quality
npx claude-skills-cli stats ~/.claude/skills/

# Step 4: Add global hook for personal activation
npx claude-skills-cli add-hook
```

**Alternative (using --name option):**
```bash
# Step 1: Create skill scaffolding with examples
npx claude-skills-cli init \
  --name data-processor \
  --description "Processing and analyzing data files in CSV, JSON, and Excel formats. Use for data cleaning, transformation, and analysis tasks." \
  --with-examples

# Step 2: Move to personal location (~ expands to full path)
mv data-processor ~/.claude/skills/

# Step 3: Fix any formatting issues
npx claude-skills-cli doctor ~/.claude/skills/data-processor

# Step 4: Check overall quality
npx claude-skills-cli stats ~/.claude/skills/

# Step 5: Add global hook for personal activation
npx claude-skills-cli add-hook
```

### Example 3: Plugin Skill Development
```bash
# Step 1: Check available plugins
ls /full/path/to/plugins/
# Output: claude-code-development/ my-custom-plugin/

# Step 2: Create skill scaffolding directly at plugin location (use full path)
npx claude-skills-cli init \
  --path /full/path/to/plugins/claude-code-development/skills/plugin-helper \
  --description "Helping users develop and test Claude Code plugins. Use when creating plugin structure, debugging plugin issues, or packaging plugins."

# Step 3: Validate and test (use full path)
npx claude-skills-cli validate /full/path/to/plugins/claude-code-development/skills/plugin-helper --strict

# Step 4: Package for distribution (use full path)
npx claude-skills-cli package /full/path/to/plugins/claude-code-development/skills/plugin-helper
```

**Alternative (using --name option):**
```bash
# Step 1: Check available plugins
ls /full/path/to/plugins/
# Output: claude-code-development/ my-custom-plugin/

# Step 2: Create skill scaffolding
npx claude-skills-cli init \
  --name plugin-helper \
  --description "Helping users develop and test Claude Code plugins. Use when creating plugin structure, debugging plugin issues, or packaging plugins."

# Step 3: Move to plugin location (use full path)
mv plugin-helper /full/path/to/plugins/claude-code-development/skills/

# Step 4: Validate and test (use full path)
npx claude-skills-cli validate /full/path/to/plugins/claude-code-development/skills/plugin-helper --strict

# Step 5: Package for distribution (use full path)
npx claude-skills-cli package /full/path/to/plugins/claude-code-development/skills/plugin-helper
```

### Example 4: Interactive Location Selection Workflow
When a user asks to create a skill, guide them through location selection:

**User**: "I want to create a skill for managing git repositories"

**Workflow**:
1. **Ask about location**: "Where would you like to save this skill?"
   - **Project** (.claude/skills/) - shared with your team
   - **Personal** (~/.claude/skills/) - just for you
   - **Plugin** (plugins/[name]/skills/) - bundle with a plugin

2. **Create based on choice**:
   ```bash
   # For project skill (using --path for direct creation - use full path)
   npx claude-skills-cli init --path /full/path/to/.claude/skills/git-manager --description "Managing git repositories, branches, and workflows. Use for git operations, branch management, and repository maintenance."

   # Alternative (using --name, requires moving with full path)
   npx claude-skills-cli init --name git-manager --description "Managing git repositories, branches, and workflows. Use for git operations, branch management, and repository maintenance."
   mv git-manager /full/path/to/.claude/skills/
   ```

3. **Complete setup**:
   ```bash
   # Validate and ensure activation (use full path)
   npx claude-skills-cli validate /full/path/to/.claude/skills/git-manager --strict
   npx claude-skills-cli add-hook --project  # or --global or --local
   ```

## References
- [Progressive Disclosure Architecture](./references/progressive-disclosure.md)
- [Validation Rules Reference](./references/validation-rules.md)
- [Command Examples](./references/command-examples.md)
- [Skill Templates](./templates/)