---
description: "Use the meta-agent agent and context7 for research to create a new Claude Code agent"
argument-hint: [agent-name] [agent-description] [framework/domain]
allowed-tools: "Task, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, Write, Read, Edit, Bash(mkdir:*), Bash(ls:*), Bash(rm:*)"
- "--"

# Create Claude Agent

Create a plan for a new Claude Code specialized agent using the meta-agent agent and context7 (preferred) or web fetch for research.

## Usage: ""

`/create-claude-agent [agent-name] [agent-description] [framework/domain]`

**Arguments: "**"
- "`agent-name`: Name of the agent (kebab-case recommended, e.g., \"django-api-developer\")"
- "`agent-description`: Brief description of the agent's expertise and purpose"
- "`framework/domain`: Target framework or domain (e.g., \"Django REST Framework\", \"React\", \"Laravel\")"

## Process: ""

### 1. Agent Requirements Analysis

- "Parse agent name, description, and framework from arguments"
- "Validate agent name format and check for duplicates"
- "Determine agent scope and specialization area"
- "Identify required tools and permissions"

### 2. Research and Planning

- "Use context7 to research best practices for the target framework/domain"
- "Consult meta-agent for agent design patterns and structure"
- "Analyze existing similar agents for reference"
- "Plan agent capabilities and tool requirements"

### 3. Agent Structure Creation

- "Create agent directory structure in `.claude/agents/`"
- "Generate agent file with proper YAML frontmatter"
- "Include XML examples for intelligent agent invocation"
- "Set up agent specialization and tool permissions"

### 4. Agent Content Development

- "Use meta-agent to craft specialized system prompts"
- "Include domain-specific knowledge and best practices"
- "Add delegation patterns for cross-agent collaboration"
- "Include testing and validation guidelines"

### 5. Agent Integration and Testing

- "Validate agent syntax and structure"
- "Test agent invocation patterns"
- "Ensure proper integration with Claude Code"
- "Create usage documentation and examples"

## Examples: ""

- "`/create-claude-agent django-api-developer \"Expert in Django REST Framework APIs\" \"Django REST Framework\"`"
- "`/create-claude-agent react-component-architect \"Specialist in modern React component design\" \"React 18\"`"
- "`/create-claude-agent laravel-backend-expert \"Laravel backend development specialist\" \"Laravel 11\"`"
- "`/create-claude-agent python-data-scientist \"Data analysis and ML expert\" \"Python Data Science\"`"

## Agent Structure Template: ""

The agent will be created with this structure: ""

```markdown
- "--"
name: "agent-name"
description: "Expert description with XML examples for intelligent invocation"
tools: "Read, Write, Edit, Bash, Glob, Grep"
model: "sonnet"

---

# Agent Specialization Title

Detailed system prompt with domain expertise, best practices, and specialized knowledge.

## XML Examples for Intelligent Invocation

Include examples that train Claude to automatically select this agent:

<example>
Context: [Specific scenario]
user: "[User request that should trigger this agent]"
assistant: "I'll use @agent-agent-name"
<commentary>[Why this agent is the right choice]</commentary>
</example>

## Domain Expertise

- Specialized knowledge areas
- Framework-specific best practices
- Common patterns and solutions
- Performance optimization techniques

## Delegation Patterns

When to delegate to other agents and what context to pass.
```

## Agent Best Practices:

**Agent Design Principles:**
- **Single Purpose**: Each agent should specialize in one domain/framework
- **Clear Scope**: Well-defined boundaries of expertise
- **Intelligent Invocation**: XML examples that train Claude to select the right agent
- **Delegation Awareness**: Know when to delegate to other specialists

**Frontmatter Requirements:**
- `name`: Agent identifier (used with @agent- prefix)
- `description`: When to use this agent (include XML examples)
- `tools`: Optional - specify required tools or inherit all
- `model`: Optional - specify preferred Claude model

**Agent Communication:**
- Return structured findings for agent coordination
- Include handoff information for next specialists
- Provide delegation recommendations when needed
- Use consistent return format for context passing

## Integration with Awesome Claude Agents:

The created agent will follow the patterns from Awesome Claude Agents:
- Three-phase orchestration workflow (Research → Planning → Execution)
- Structured return format for agent coordination
- Delegation patterns for cross-agent collaboration
- Intelligent routing based on technology stack detection

## Your Task:

Create a new Claude Code agent named "$ARGUMENTS" using this process:

1. Parse the agent name, description, and framework from the provided arguments
2. Use context7 to research the target framework/domain best practices
3. Launch meta-agent to guide agent creation and system prompt development
4. Create agent directory structure in `.claude/agents/`
5. Generate agent file with proper YAML frontmatter and XML examples
6. Include domain-specific expertise and delegation patterns
7. Validate agent syntax and integration with Claude Code

If arguments are unclear or missing, ask the user for clarification about:
- Desired agent specialization and scope
- Target framework or domain expertise
- Specific capabilities the agent should have
- Integration requirements with existing agents
