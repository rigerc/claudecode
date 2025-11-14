# Command Examples

## init Command Examples

### Basic Skill Creation
```bash
# Create minimal skill
npx claude-skills-cli init --name my-skill --description "Brief description with trigger keywords"

# Create at specific path (always use full/absolute paths)
npx claude-skills-cli init --path /full/path/to/.claude/skills/my-skill --description "Brief description with trigger keywords"

# Create with examples
npx claude-skills-cli init --name my-skill --description "..." --with-examples

# Create with examples at specific path (use full path)
npx claude-skills-cli init --path /full/path/to/plugins/my-plugin/skills/my-skill --description "..." --with-examples
```

### Naming Conventions
```bash
# Good names (kebab-case)
npx claude-skills-cli init --name api-client --description "..."
npx claude-skills-cli init --name data-processor --description "..."
npx claude-skills-cli init --name git-helper --description "..."

# Bad names (avoid)
npx claude-skills-cli init --name MySkill --description "..." # Capital letters
npx claude-skills-cli init --name api_client --description "..." # Underscores
npx claude-skills-cli init --name "api client" --description "..." # Spaces
```

### Path-based Creation (always use full/absolute paths)
```bash
# Create in project skills (use full path)
npx claude-skills-cli init --path /full/path/to/.claude/skills/my-skill --description "Project-specific skill"

# Create in user skills (~ expands to full home path)
npx claude-skills-cli init --path ~/.claude/skills/my-skill --description "Personal skill"

# Create in plugin skills (use full path)
npx claude-skills-cli init --path /full/path/to/plugins/my-plugin/skills/my-skill --description "Plugin skill"

# Create with nested path (use full path)
npx claude-skills-cli init --path /full/path/to/plugins/claude-code-development/skills/agent-creator --description "Agent creation skill"
```

### Description Best Practices
```bash
# Good descriptions (specific with triggers)
npx claude-skills-cli init --name pdf-processor \
  --description "Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction."

# Use full paths with --path option
npx claude-skills-cli init --path /full/path/to/.claude/skills/excel-analyzer \
  --description "Analyze Excel spreadsheets, create pivot tables, generate charts. Use for data analysis in .xlsx files."

# Bad descriptions (too vague)
npx claude-skills-cli init --name helper \
  --description "Helps with files" # Too generic
```

## validate Command Examples

### Validation Modes (use full paths)
```bash
# Basic validation (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill

# Strict validation (fails on warnings, use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill --strict

# JSON output for automation (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/my-skill --format json
```

### Batch Validation
```bash
# Validate all skills in directory (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/

# Validate with JSON output for CI/CD (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/ --format json > validation-report.json
```

## doctor Command Examples

### Fix Common Issues (use full paths)
```bash
# Fix multi-line descriptions (use full path)
npx claude-skills-cli doctor /full/path/to/.claude/skills/my-skill

# Doctor multiple skills (use full paths)
npx claude-skills-cli doctor /full/path/to/.claude/skills/skill1 /full/path/to/.claude/skills/skill2

# Doctor all skills in directory (use full path)
npx claude-skills-cli doctor /full/path/to/.claude/skills/
```

## stats Command Examples

### Skill Overview (use full paths)
```bash
# Show statistics for all skills (use full path)
npx claude-skills-cli stats /full/path/to/.claude/skills

# Show statistics for specific skill (use full path)
npx claude-skills-cli stats /full/path/to/.claude/skills/my-skill
```

### Sample Output
```
Skills Overview (5 skills)
├── api-client: ✅ Valid (42 lines, 1.2k tokens)
├── data-processor: ⚠️  Warnings (67 lines, 2.1k tokens)
├── git-helper: ✅ Valid (38 lines, 0.9k tokens)
├── pdf-processor: ❌ Errors (missing references)
└── excel-analyzer: ✅ Valid (45 lines, 1.4k tokens)

Quality Rating: 4/5
```

## package Command Examples

### Create Distribution Package (use full paths)
```bash
# Package single skill (use full path)
npx claude-skills-cli package /full/path/to/.claude/skills/my-skill

# Package with validation skip (use full path)
npx claude-skills-cli package /full/path/to/.claude/skills/my-skill --skip-validation
```

### Output
```bash
Creating package: my-skill-v1.0.0.zip
✅ Validation passed
📦 Package created: ./dist/my-skill-v1.0.0.zip
```

## add-hook Command Examples

### Hook Scopes
```bash
# Global hook (applies to all projects)
npx claude-skills-cli add-hook

# Project hook (committed to git)
npx claude-skills-cli add-hook --project

# Local hook (gitignored, personal)
npx claude-skills-cli add-hook --local
```

### Hook Configuration
The hook adds this instruction to settings:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "echo 'INSTRUCTION: Check available skills, match keywords to skill names/descriptions, and activate matching skills using Skill(skill-name).'"
      }
    ]
  }
}
```

## Workflow Examples

### Complete Skill Creation Workflow (use full paths)
```bash
# 1. Create skill (use full path with --path)
npx claude-skills-cli init \
  --path /full/path/to/.claude/skills/api-client-helper \
  --description "Creating and configuring API client code for REST services. Use when working with HTTP requests, API authentication, or client libraries." \
  --with-examples

# 2. Validate (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/api-client-helper --strict

# 3. Fix issues if any (use full path)
npx claude-skills-cli doctor /full/path/to/.claude/skills/api-client-helper

# 4. Ensure activation
npx claude-skills-cli add-hook --project

# 5. Check stats (use full path)
npx claude-skills-cli stats /full/path/to/.claude/skills/
```

### Troubleshooting Workflow (use full paths)
```bash
# 1. Identify issues (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/problem-skill

# 2. Get detailed report (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/problem-skill --format json

# 3. Auto-fix common issues (use full path)
npx claude-skills-cli doctor /full/path/to/.claude/skills/problem-skill

# 4. Re-validate (use full path)
npx claude-skills-cli validate /full/path/to/.claude/skills/problem-skill --strict

# 5. Check all skills health (use full path)
npx claude-skills-cli stats /full/path/to/.claude/skills/
```

### CI/CD Integration (use full paths)
```bash
# In CI pipeline
#!/bin/bash
set -e

echo "Validating all Claude Skills..."
# Use full path or $PWD for current working directory
npx claude-skills-cli validate $PWD/.claude/skills/ --strict --format json > validation.json

# Check for errors
if jq -e '.[] | select(.status == "error")' validation.json > /dev/null; then
  echo "❌ Skills validation failed"
  exit 1
fi

echo "✅ All skills passed validation"
```