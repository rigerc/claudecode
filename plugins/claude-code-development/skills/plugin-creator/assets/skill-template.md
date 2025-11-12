---
name: skill-identifier
description: Specific description of when to use this skill. Include WHAT it does and WHEN to trigger it with keywords and file types.
---

# Skill Name

## Purpose

What this skill provides and when it should be used.

## Usage

### When to Use

- Scenario 1: [Specific trigger]
- Scenario 2: [Specific trigger]
- Scenario 3: [Specific trigger]

### Instructions

1. **Step 1** - First action
2. **Step 2** - Next action
3. **Step 3** - Complete task

## Bundled Resources

**scripts/** - Executable code for deterministic tasks
- `script-name.py` - Description

**references/** - Documentation loaded on demand
- `reference.md` - Detailed specifications

**assets/** - Templates and output files
- `template.ext` - Template for output

## Optional Frontmatter Fields

```yaml
name: skill-identifier  # Max 64 chars, lowercase, numbers, hyphens only (required)
description: When to use this skill (max 1024 chars, required)
allowed-tools: [Read, Bash, Grep]  # Restrict available tools
```

## Best Practices

- Be specific in description for proper discovery
- Use progressive loading - keep SKILL.md concise, details in references/
- Restrict tools with allowed-tools
- Scripts need execute permissions (chmod +x)
