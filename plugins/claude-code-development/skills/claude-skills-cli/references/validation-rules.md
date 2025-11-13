# Validation Rules Reference

## Structure & Format Validation

### Directory Structure
```
skill-name/
├── SKILL.md (required)
├── references/ (optional)
├── scripts/ (optional)
├── templates/ (optional)
└── assets/ (optional)
```

### Naming Requirements
- **Skill name**: kebab-case only (lowercase letters, numbers, hyphens)
- **Max length**: 64 characters
- **Directory match**: Skill directory name must equal skill name in YAML

### YAML Frontmatter
```yaml
---
name: skill-name
description: Brief description (max 1024 chars)
allowed-tools: Tool1, Tool2, Tool3 (optional)
---
```

#### Required Fields
- `name`: Must match directory name, kebab-case format
- `description**: Brief description of skill purpose and usage

#### Optional Fields
- `allowed-tools`: Comma-separated list of permitted tools

## Content Validation

### Level 1: Metadata Rules
- **Description length**: <200 characters optimal
- **Trigger specificity**: Must include clear usage indicators
- **User phrasing**: Third-person, action-oriented, gerunds
- **Keyword richness**: Align description with actual content

### Level 2: Body Rules
- **Line count**: ~50 target, 150 maximum
- **Word count**: <1000 recommended, <5000 maximum
- **Token estimate**: <6500 token budget
- **Code blocks**: 1-2 optimal, avoid excessive code
- **Sections**: 3-5 recommended for organization

### Level 3: References Rules
- **File existence**: All referenced files must exist
- **Orphan detection**: Files not referenced from Level 2
- **Nesting depth**: Analyze directory structure depth
- **Link validation**: Internal links must be valid

## Common Validation Failures

### Multi-line Descriptions
**Problem**: YAML description spans multiple lines
**Solution**: Use single-line description or run doctor command
```bash
npx claude-skills-cli doctor .claude/skills/my-skill
```

### Missing Required Fields
**Problem**: YAML missing name or description
**Solution**: Add required fields to frontmatter

### Invalid YAML Syntax
**Problem**: Tabs instead of spaces, unquoted special characters
**Solution**: Fix indentation and quote special characters

### Excessive Content
**Problem**: Body exceeds line/word/token limits
**Solution**: Move content to Level 3 files, condense instructions

### Broken References
**Problem**: Referenced files don't exist
**Solution**: Create missing files or remove broken links

## Validation Modes

### Basic Validation
```bash
npx claude-skills-cli validate .claude/skills/my-skill
```
Reports errors and warnings

### Strict Validation
```bash
npx claude-skills-cli validate .claude/skills/my-skill --strict
```
Fails on warnings, enforces all rules strictly

### JSON Output
```bash
npx claude-skills-cli validate .claude/skills/my-skill --format json
```
Machine-readable output for automation