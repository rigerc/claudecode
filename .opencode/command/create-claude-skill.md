---
description: "Required! Use the skill-creator skill to create a new Claude Code skill"
argument-hint: [skill-name] [skill-description]
allowed-tools: "Skill, Write, Read, Bash(python3:*), Bash(mkdir:*), Bash(ls:*), Bash(rm:*), Edit"

---

# Create Claude Skill

Create a plan for a new Claude Code skill using the skill-creator skill, which provides comprehensive guidance for developing effective skills with proper structure, resources, and best practices. Identify and research the skill's subject first (using provided documentation (preferred), context7 or web fetch).

## Usage:

`/create-claude-skill [skill-name] [skill-description]`

**Arguments:**
- `skill-name`: Name of the skill to create (kebab-case recommended)
- `skill-description`: Brief description of what the skill does

## Process:

### 1. Skill Requirements Analysis

- Parse skill name and description from arguments
- Validate skill name format and uniqueness
- Determine skill purpose and target use cases
- Identify potential resource requirements (scripts, references, assets)

### 2. Skill Structure Planning

- Load skill-creator to access guidance and templates
- Determine appropriate skill structure based on purpose
- Plan resource organization (scripts/, references/, assets/)
- Define skill metadata and scope

### 3. Skill Initialization

- Execute skill-creator's init_skill.py script
- Create skill directory with proper structure
- Generate initial SKILL.md template
- Set up example resource directories

### 4. Skill Content Development

- Customize SKILL.md with skill-specific content
- Remove unnecessary example files and directories
- Add skill-specific resources if needed
- Follow skill-creator best practices

### 5. Skill Validation and Packaging

- Validate skill structure and syntax
- Test skill functionality if applicable
- Package skill into distributable format
- Provide usage instructions and examples

## Examples:

- `/create-claude-skill pdf-editor "Edit PDF files including rotation, merging, and form filling"`
- `/create-claude-skill github-automation "Automate GitHub workflows, PR management, and issue tracking"`
- `/create-claude-skill data-analyst "Analyze data files, generate reports, and create visualizations"`
- `/create-claude-skill docker-manager "Manage Docker containers, images, and deployments"`

## Skill Development Guidelines:

**Skill Types:**
- **Workflow Skills**: Multi-step procedures for specific domains
- **Tool Integration Skills**: Interface with external APIs and services
- **Domain Expertise Skills**: Specialized knowledge and business logic
- **Template Skills**: Boilerplate generators and scaffolding tools

**Resource Planning:**
- `scripts/`: Executable code for automation and repeated operations
- `references/`: Documentation loaded into context as needed
- `assets/`: Files used in output (templates, images, boilerplate)

**Best Practices:**
- Use imperative/infinitive form in instructions
- Focus on procedural knowledge not obvious to Claude
- Include concrete examples and decision trees
- Reference bundled resources appropriately
- Keep SKILL.md lean (<5k words), use references for detailed info

## Your Task:

Create a new skill named "$ARGUMENTS" using the skill-creator:

1. Parse the skill name and description from the provided arguments
2. Launch skill-creator to access comprehensive guidance
3. Initialize the skill using the init_skill.py script
4. Customize the skill content based on the description
5. Validate and package the final skill
6. Provide clear usage instructions and examples

If arguments are unclear or missing, ask the user for clarification about:
- Desired skill name and format
- Specific functionality the skill should provide
- Target use cases and workflows
- Any existing resources or templates to include
