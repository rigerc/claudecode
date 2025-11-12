---
description: A skill to create a skill using skill-creator skill from a documentation file specified by the user
argument-hint: [documentation-file] [skill-name] [project|personal]
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, Skill
---

# Create Skill from Documentation

Use the skill-creator skill to create a new Agent Skill based on a documentation file specified by the user.

## Parameters
- **documentation-file** (required): Path to the documentation file to analyze
- **skill-name** (optional): Name for the new skill. If not provided, will be derived from the documentation filename
- **scope** (optional): Whether to create a project or personal skill. Defaults to "project"

## Instructions

### 1. Validate Input
- Verify that `$1` exists and is a readable file
- If `$2` is not provided, extract skill name from the documentation filename (removing extensions)
- Determine if `$3` is "project" (default) or "personal"

### 2. Analyze Documentation
- Read the documentation file specified in `$1`
- Analyze the content structure, key topics, and expertise areas covered
- Identify:
  - Main topics and areas of expertise
  - Specific workflows or processes described
  - Tools, libraries, or frameworks mentioned
  - Target audience and use cases

### 3. Use working-with-claude-code Skill
- Use the `Skill` tool with `working-with-claude-code` to understand skill creation best practices
- Reference the skills.md documentation from that skill
- Follow the proper structure and format requirements

### 4. Determine Skill Structure
Based on the documentation analysis, determine:
- **Skill name**: Use `$2` if provided, otherwise derive from filename
- **Description**: Create a clear description of what the skill does and when to use it
- **Allowed tools**: Based on the documentation content, determine appropriate tools to allow
- **Supporting files**: Determine if templates, references, or scripts are needed

### 5. Create Skill Directory Structure
- Create appropriate directory:
  - Project skill: `.claude/skills/[skill-name]/`
  - Personal skill: `~/.claude/skills/[skill-name]/`
- Create `SKILL.md` file with proper YAML frontmatter
- Add supporting files as needed (templates, references, scripts)

### 6. Generate Skill Content

#### SKILL.md Structure:
```yaml
---
name: [Derived Skill Name]
description: [Generated description based on documentation analysis]
allowed-tools: [List of relevant tools]
---

# [Skill Name]

## Overview
[Brief description of what this skill does]

## When to Use
[Clear criteria for when Claude should use this skill]

## Instructions
[Detailed step-by-step guidance]
```

### 7. Create Supporting Materials
Based on the documentation content:
- Add reference documentation if external resources are mentioned
- Create templates for common tasks described in the documentation
- Add scripts if automation or tools are referenced
- Include examples and best practices

### 8. Quality Assurance
- Verify YAML syntax is correct
- Ensure the skill description is specific enough for Claude to discover
- Check that allowed-tools are appropriate for the skill's purpose
- Test that the skill can be discovered properly

## Examples

```bash
# Create skill from API documentation
/create-skill-from-documentation docs/api-reference.js authentication-api

# Create personal skill from tutorial
/create-skill-from-documentation ~/tutorials/data-analysis.md data-processor personal

# Create skill with automatic name detection
/create-skill-from-documentation ./deployment-guide.md
```

## Output

The command will:
1. Create a new skill directory with proper structure
2. Generate a comprehensive SKILL.md file
3. Add supporting files as needed
4. Provide feedback on the created skill location and features
5. Suggest next steps for testing and refinement

## Notes

- The skill will be created based on the expertise domain covered in the documentation
- Complex documentation may result in skills with multiple supporting files
- The skill description will be crafted to help Claude discover when to use it
- All created skills follow Claude Code's skill development best practices