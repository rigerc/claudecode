---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, and tools.

## When to Use This Skill

Use this skill when you need to:

- Create a new skill from scratch
- Update or refactor an existing skill
- Understand skill structure and best practices
- Package and distribute skills
- Debug skill validation errors

## Quick Start

Initialize a new skill using the provided script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates a template skill directory with proper structure and placeholder files.

## Skill Creation Workflow

Follow these steps in order (skip only if clearly not applicable):

1. **Understand with Examples**: Gather concrete examples of how the skill will be used
2. **Plan Resources**: Identify scripts, references, and assets needed
3. **Initialize**: Run `init_skill.py` to create the skill structure
4. **Implement**: Add resources and write SKILL.md instructions
5. **Package**: Run `scripts/package_skill.py <path/to/skill>` to validate and create distributable zip
6. **Iterate**: Test and refine based on real usage

## Available Resources

See `references/` for comprehensive documentation:

- **skill_structure.md**: Anatomy of skills, progressive disclosure, and resource types
- **creation_process.md**: Detailed step-by-step creation workflow
- **writing_guidelines.md**: Best practices for writing effective SKILL.md content
- **skills.md**: Complete skills documentation and advanced topics
