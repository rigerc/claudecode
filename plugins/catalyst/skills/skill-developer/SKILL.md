---
name: skill-developer
description: Use when creating Claude Code skills, managing skill-rules.json, understanding trigger patterns, implementing progressive disclosure, or working with hooks and activation mechanisms.
tags: [claude-code, skills, development, hooks, json, yaml, triggers]
---

# Skill Developer Guide

Create and manage Claude Code skills following best practices with progressive disclosure and proper activation patterns.

## Quick Start

**Create new skill:**
```bash
npx claude-skills-cli init my-skill --description "Brief skill description"
```

**Basic skill structure:**
```
my-skill/
├── SKILL.md
├── references/
└── scripts/
```

## Expert Guidance

- **Progressive Disclosure**: Level 1 metadata, Level 2 core, Level 3+ details
- **Triggers**: Keywords and intent patterns for auto-activation
- **YAML Frontmatter**: Required metadata fields and formatting
- **500-line Rule**: Maximum SKILL.md length for maintainability
- **Hooks**: UserPromptSubmit and activation mechanisms
- **File Paths**: Proper skill locations and paths
- **Validation**: Using claude-skills-cli for compliance

## Progressive Disclosure

Level 2 provides core patterns and examples. Level 3+ contains detailed implementation guides and best practices.