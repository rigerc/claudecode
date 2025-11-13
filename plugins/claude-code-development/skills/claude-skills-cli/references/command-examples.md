# Command Examples

## init Command Examples

### Basic Skill Creation
```bash
# Create minimal skill
npx claude-skills-cli init --name my-skill --description "Brief description with trigger keywords"

# Create with examples
npx claude-skills-cli init --name my-skill --description "..." --with-examples
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

### Description Best Practices
```bash
# Good descriptions (specific with triggers)
npx claude-skills-cli init --name pdf-processor \
  --description "Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction."

npx claude-skills-cli init --name excel-analyzer \
  --description "Analyze Excel spreadsheets, create pivot tables, generate charts. Use for data analysis in .xlsx files."

# Bad descriptions (too vague)
npx claude-skills-cli init --name helper \
  --description "Helps with files" # Too generic
```

## validate Command Examples

### Validation Modes
```bash
# Basic validation
npx claude-skills-cli validate .claude/skills/my-skill

# Strict validation (fails on warnings)
npx claude-skills-cli validate .claude/skills/my-skill --strict

# JSON output for automation
npx claude-skills-cli validate .claude/skills/my-skill --format json
```

### Batch Validation
```bash
# Validate all skills in directory
npx claude-skills-cli validate .claude/skills/

# Validate with JSON output for CI/CD
npx claude-skills-cli validate .claude/skills/ --format json > validation-report.json
```

## doctor Command Examples

### Fix Common Issues
```bash
# Fix multi-line descriptions
npx claude-skills-cli doctor .claude/skills/my-skill

# Doctor multiple skills
npx claude-skills-cli doctor .claude/skills/skill1 .claude/skills/skill2

# Doctor all skills in directory
npx claude-skills-cli doctor .claude/skills/
```

## stats Command Examples

### Skill Overview
```bash
# Show statistics for all skills
npx claude-skills-cli stats .claude/skills

# Show statistics for specific skill
npx claude-skills-cli stats .claude/skills/my-skill
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

### Create Distribution Package
```bash
# Package single skill
npx claude-skills-cli package .claude/skills/my-skill

# Package with validation skip
npx claude-skills-cli package .claude/skills/my-skill --skip-validation
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

### Complete Skill Creation Workflow
```bash
# 1. Create skill
npx claude-skills-cli init \
  --name api-client-helper \
  --description "Creating and configuring API client code for REST services. Use when working with HTTP requests, API authentication, or client libraries." \
  --with-examples

# 2. Validate
npx claude-skills-cli validate .claude/skills/api-client-helper --strict

# 3. Fix issues if any
npx claude-skills-cli doctor .claude/skills/api-client-helper

# 4. Ensure activation
npx claude-skills-cli add-hook --project

# 5. Check stats
npx claude-skills-cli stats .claude/skills/
```

### Troubleshooting Workflow
```bash
# 1. Identify issues
npx claude-skills-cli validate .claude/skills/problem-skill

# 2. Get detailed report
npx claude-skills-cli validate .claude/skills/problem-skill --format json

# 3. Auto-fix common issues
npx claude-skills-cli doctor .claude/skills/problem-skill

# 4. Re-validate
npx claude-skills-cli validate .claude/skills/problem-skill --strict

# 5. Check all skills health
npx claude-skills-cli stats .claude/skills/
```

### CI/CD Integration
```bash
# In CI pipeline
#!/bin/bash
set -e

echo "Validating all Claude Skills..."
npx claude-skills-cli validate .claude/skills/ --strict --format json > validation.json

# Check for errors
if jq -e '.[] | select(.status == "error")' validation.json > /dev/null; then
  echo "❌ Skills validation failed"
  exit 1
fi

echo "✅ All skills passed validation"
```