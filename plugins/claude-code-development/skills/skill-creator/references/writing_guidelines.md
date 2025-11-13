# Writing Guidelines for SKILL.md

## Writing Style

Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

## Structure

SKILL.md should be concise and focused on essential procedural knowledge. Keep it under 50 lines and 1000 words to comply with progressive disclosure principles.

### Required Sections

1. **Title**: Brief skill name
2. **When to Use This Skill**: Clear triggers for skill activation
3. **Quick Start**: Minimal working example or initialization command
4. **Workflow/Process**: High-level steps or key procedures
5. **Available Resources**: References to bundled documentation

### Optional Sections

- **Configuration**: If the skill requires setup
- **Common Patterns**: If there are frequently used approaches
- **Troubleshooting**: For known issues (or link to references/)

## Content Guidelines

### Keep in SKILL.md

- Essential procedural instructions
- High-level workflow steps
- Quick reference examples
- Pointers to bundled resources
- Critical domain knowledge needed for every use

### Move to references/

- Detailed API documentation
- Extended examples and code samples
- Comprehensive schemas or data structures
- Troubleshooting guides
- Historical context or background information
- Alternative approaches and edge cases

## Metadata Best Practices

### Name Field

- Use lowercase with hyphens (kebab-case)
- Be descriptive but concise
- Examples: `pdf-editor`, `frontend-webapp-builder`, `big-query`

### Description Field

- Use third person: "This skill should be used when..." not "Use this skill when..."
- Be specific about triggers and use cases
- Include key technologies or domains
- Keep under 100 words
- Examples:
  - "This skill should be used when working with PDF files, including rotation, merging, splitting, and metadata editing tasks."
  - "This skill should be used when building frontend web applications with React, providing boilerplate templates and component patterns."

## Progressive Disclosure

Remember the three-level loading system:

1. **Metadata (always loaded)**: Name and description must be clear enough for Claude to decide whether to trigger the skill
2. **SKILL.md body (loaded on trigger)**: Essential instructions and workflow guidance
3. **Bundled resources (loaded as needed)**: Detailed documentation, scripts, and assets

Keep SKILL.md lean by moving detailed content to references/. This allows Claude to load comprehensive information only when needed, rather than cluttering the context window.

## Examples of Good SKILL.md Structure

See these skills for reference:

- `go-bubbles-skill`: Clean structure with minimal body and comprehensive references
- `go-bubbletea-skill`: Clear workflow with effective resource organization
- `ha-addon`: Focused procedural guidance with supporting documentation
