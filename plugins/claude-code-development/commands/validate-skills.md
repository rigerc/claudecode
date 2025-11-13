---
description: Validate skills in plugins using claude-skills-cli with comprehensive analysis
allowed-tools: Read, Write, Bash
---

# Validate claude skills using claude-skills-cli with comprehensive analysis and automated fixing.

This command validates all skills in the `./plugins` directory using the `claude-skills-cli` tool and provides detailed analysis of validation results with recommended fixes.

## Step 1: Run doctor to auto-fix common issues
python3 ./scripts/find-skills.py --doctor

## Step 2: Validate to check improvements
python3 ./scripts/find-skills.py --validate
```

Analyze the output and suggest improvements and fixes for each skill that failed validation.
