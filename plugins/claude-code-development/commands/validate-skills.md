---
description: Validate skills in plugins using claude-skills-cli with comprehensive analysis
allowed-tools: Read, Write, Bash
---

# Validate skills using claude-skills-cli with comprehensive analysis and automated fixing.

## Overview

This command validates all skills in the `./plugins` directory using the `claude-skills-cli` tool and provides detailed analysis of validation results with recommended fixes.

## Usage Options

### Option 1: Basic Skills Discovery
List all found skills without validation:
```bash
python3 ./scripts/find-skills.py
```

### Option 2: Validation Only
Run validation on all skills and show summary:
```bash
python3 ./scripts/find-skills.py --validate-only
```

### Option 3: Validation with Details
Run validation and show detailed errors/warnings:
```bash
python3 ./scripts/find-skills.py --validate
```

### Option 4: Auto-Fix with Doctor
Run automatic fixes on all skills:
```bash
python3 ./scripts/find-skills.py --doctor
```

### Option 5: Comprehensive Workflow (Recommended)
For complete validation and fixing workflow:
```bash
# Step 1: Run validation to identify issues
python3 ./scripts/find-skills.py --validate

# Step 2: Run doctor to auto-fix common issues
python3 ./scripts/find-skills.py --doctor

# Step 3: Re-validate to check improvements
python3 ./scripts/find-skills.py --validate-only
```

## Validation Analysis

### Common Issues & Automatic Fixes

The tool automatically analyzes validation output and categorizes issues:

#### **Critical Errors (Require Immediate Action)**

**Progressive Disclosure Violations:**
- **Description too long** (>300 chars): Auto-fixed by doctor with reflow
- **Body too large** (>50 lines, >1000 words): Move content to `references/`
- **Excessive code examples** (>2): Move extra examples to `references/examples.md`

**Naming Issues:**
- **Skill name mismatch**: Doctor fixes YAML title alignment
- **Invalid format**: Doctor ensures kebab-case compliance

#### **Warnings (Recommended Improvements)**

**Content Structure:**
- **Missing trigger phrases**: Add "Use when...", "Use for...", "Use to..."
- **Too many sections**: Consolidate into 3-5 focused sections
- **Missing Quick Start**: Add minimal working example
- **Vague terminology**: Replace generic terms with specific descriptions

**Reference Management:**
- **Unused reference files**: Link from SKILL.md or remove
- **Empty directories**: Remove unused `scripts/`, `assets/` folders
- **TODO placeholders**: Complete or remove placeholder content

### Fix Recommendations by Issue Type

#### **Progressive Disclosure Fixes**
```bash
# For skills with too much content:
npx claude-skills-cli doctor ./plugins/[plugin]/skills/[skill-name]

# Manual restructuring:
mkdir -p ./plugins/[plugin]/skills/[skill-name]/references
# Move detailed examples to references/examples.md
# Move comprehensive docs to references/guide.md
# Keep only essential instructions in SKILL.md
```

#### **Description Optimization**
```bash
# Target format: <200 chars with trigger keywords
# Good: "Creating Go CLI applications using urfave/cli v3. Use when building command-line tools, CLI interfaces, or terminal applications."
# Bad: "This skill helps you create command line applications using the urfave/cli library for Go programming..."
```

#### **Content Structure Fixes**
```bash
# Recommended structure:
## Overview (1-2 sentences)
## When to Use (bullet points)
## Quick Start (1 minimal example)
## Key Concepts (3-5 sections max)
## See Also (links to references/)
```

### Validation Exit Codes

- **Exit 0**: All skills passed validation
- **Exit 1**: One or more skills failed validation

### Output Interpretation

**Success Indicators:**
- `✓ PASSED`: Skill meets all validation criteria
- `✓ Doctor completed`: Auto-fixes applied successfully

**Failure Indicators:**
- `✗ FAILED`: Skill has validation errors
- `❌ Doctor operation failed`: Auto-fixes encountered issues

## Manual Validation Commands

For individual skill validation:
```bash
# Strict validation with detailed output
npx claude-skills-cli validate ./plugins/[plugin]/skills/[skill-name] --strict

# Auto-fix common issues
npx claude-skills-cli doctor ./plugins/[plugin]/skills/[skill-name]

# Check skill statistics
npx claude-skills-cli stats ./plugins/[plugin]/skills/[skill-name]
```

## Best Practices

### **Before Validation:**
1. Ensure `npx claude-skills-cli` is installed and accessible
2. Backup skills before running doctor operations
3. Check for any local modifications that might be overwritten

### **After Validation:**
1. Review doctor changes with `git diff`
2. Test skill activation after major changes
3. Commit fixes in logical chunks (per plugin or per issue type)

### **Continuous Integration:**
Add to CI pipeline to enforce skill quality:
```bash
# Fail CI if any skills don't validate
python3 ./scripts/find-skills.py --validate-only
if [ $? -ne 0 ]; then
  echo "Skill validation failed - please fix issues before merging"
  exit 1
fi
```

## Troubleshooting

**Doctor not working:**
```bash
# Check claude-skills-cli installation
npx claude-skills-cli --version

# Install if missing
npm install -g claude-skills-cli
```

**Timeout issues:**
```bash
# Increase timeout in find-skills.py if needed
# Edit line 89 (validation) and line 130 (doctor) timeout values
```

**Permission issues:**
```bash
# Ensure scripts are executable
chmod +x ./scripts/find-skills.py
```

## Example Workflow

```bash
# Complete validation and fixing workflow
echo "=== Step 1: Initial Assessment ==="
python3 ./scripts/find-skills.py --validate

echo "=== Step 2: Auto-fix Common Issues ==="
python3 ./scripts/find-skills.py --doctor

echo "=== Step 3: Verify Improvements ==="
python3 ./scripts/find-skills.py --validate-only

echo "=== Step 4: Review Changes ==="
git status
git diff plugins/

echo "=== Step 5: Test Critical Skills ==="
# Test a few key skills manually
npx claude-skills-cli validate ./plugins/claude-code-development/skills/claude-skills-cli --strict
```

