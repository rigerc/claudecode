---
description: Validate all agent skills using claude-skills-cli
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
---

# Validate All Skills

You are tasked with validating all Claude Code agent skills in this project using the validation script and claude-skills-cli.

## Process

1. Execute the validation script located at:
   `plugins/claude-code-development/skills/claude-skills-cli/scripts/validate-all-skills.sh`

2. For each skill that fails validation:
   - Read the skill's SKILL.md file to understand its structure
   - Identify the specific validation errors from claude-skills-cli output
   - Analyze what needs to be fixed based on the error messages
   - Create a todo list with specific fixes needed for that skill
   - Provide a concise plan for fixes and improvements

## Validation Script

The script:
- Finds all directories containing SKILL.md files
- Validates each skill using `npx claude-skill-cli validate`
- Reports pass/fail status for each skill
- Provides a summary of total skills, passed, and failed

## Expected Output

For each failed skill, provide:

1. **Skill Name and Location**: Full path to the skill directory
2. **Validation Errors**: Exact error messages from claude-skills-cli
3. **Root Cause Analysis**: What's causing the validation to fail
4. **Fix Plan**: Specific steps to resolve each error, including:
   - Missing required fields or sections
   - Incorrect frontmatter format
   - Invalid file structure
   - Content quality issues
   - Reference file problems

## Success Criteria

- All skills pass validation
- Each skill has proper structure according to claude-skills-cli requirements
- SKILL.md files follow the expected format
- No validation errors remain

## Tools Available

You have access to:
- **Bash**: Run the validation script
- **Read**: Examine skill files and error messages
- **Grep**: Search for patterns in skill files
- **Glob**: Find skill directories
- **TodoWrite**: Track fixes needed for each skill

Execute the validation script now and provide a comprehensive report.
