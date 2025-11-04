---
description: "Create a complete expert system by generating an agent, a skill, and a helper command for the specified subject"
argument-hint: [subject-name] [subject-description] [framework/domain]
allowed-tools: "Write, Read, Edit, Bash(mkdir:*), Bash(ls:*), Bash(rm:*), Task, Skill, mcp__context7__resolve-library-id, mcp__context7__get-library-docs"

---

# Create Claude Expert System

Create a complete expert system for any subject by generating three integrated components: a specialized agent, a comprehensive skill, and a helper command. This meta-command orchestrates the creation of a full expertise package that provides domain-specific knowledge, specialized workflows, and automation capabilities.

## Usage:

`/create-claude-expert [subject-name] [subject-description] [framework/domain]`

**Arguments:**
- `subject-name`: Name of the subject/domain (kebab-case recommended, e.g., "docker-management", "kubernetes-orchestration")
- `subject-description`: Brief description of the subject area and expertise needed
- `framework/domain`: Target framework or domain (e.g., "Docker & Kubernetes", "AWS Cloud", "Machine Learning")

## Process:

### 1. Expert System Planning

- Parse subject name, description, and domain from arguments
- Validate subject format and check for existing expertise systems
- Analyze the subject to determine agent, skill, and command requirements
- Plan the integration strategy between all three components

### 2. Research Phase

- Use context7 to research the subject domain and best practices
- Identify key concepts, workflows, and common tasks
- Research existing tools, frameworks, and methodologies
- Gather information for specialized knowledge base

### 3. Agent Creation

- Execute `/create-claude-agent` with specialized parameters for the subject
- Create domain-specific agent with XML examples for intelligent invocation
- Include delegation patterns and cross-agent collaboration
- Configure agent tools and permissions for the domain

### 4. Skill Development

- Execute `/create-claude-skill` with comprehensive subject knowledge
- Create structured skill with domain expertise and workflows
- Include references, scripts, and assets specific to the subject
- Package skill for distribution and reuse

### 5. Helper Command Creation

- Execute `/create-claude-command` for common domain tasks
- Create utility command that leverages both the agent and skill
- Include automation patterns for repetitive domain tasks
- Integrate with existing Claude Code workflows

### 6. System Integration

- Create integration documentation for all components
- Set up cross-references between agent, skill, and command
- Validate that all components work together seamlessly
- Generate usage examples and best practices

## Examples:

- `/create-claude-expert docker-management "Complete Docker and container orchestration expertise" "Docker & Kubernetes"`
- `/create-claude-expert aws-cloud-architecture "AWS cloud architecture and DevOps expertise" "Amazon Web Services"`
- `/create-claude-expert machine-learning "ML model development and deployment expertise" "Machine Learning & AI"`
- `/create-claude-expert react-development "Modern React development expertise" "React & Next.js"`

## Generated Components:

### 1. Specialized Agent (`@agent-{subject}-expert`)
- Domain-specific knowledge and best practices
- Intelligent invocation patterns with XML examples
- Delegation awareness and collaboration patterns
- Framework-specific expertise and tool recommendations

### 2. Comprehensive Skill (`{subject}-expert`)
- Structured knowledge base with core capabilities
- Domain-specific workflows and processes
- Resource organization (scripts/, references/, assets/)
- Packaged for distribution and team sharing

### 3. Helper Command (`/{subject}-helper`)
- Common domain task automation
- Integration with agent and skill
- Workflow shortcuts and utilities
- Error handling and best practices

## Integration Architecture:

The three components work together in a coordinated system:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Helper Cmd    │───▶│   Agent Expert   │───▶│   Skill Expert  │
│                 │    │                  │    │                 │
│ Task Automation │    │ Domain Knowledge │    │ Deep Expertise  │
│ Quick Actions   │    │ Specialization   │    │ Structured Info │
│ Workflow Entry  │    │ Intelligent Use  │    │ Resource Access │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Usage Flow:**
1. **Helper Command**: Entry point for common tasks and quick actions
2. **Agent Expert**: Handles complex domain-specific problems and analysis
3. **Skill Expert**: Provides deep knowledge, references, and structured workflows

## Quality Assurance:

### Component Validation:
- **Agent**: Test intelligent invocation and domain expertise
- **Skill**: Validate knowledge structure and resource organization
- **Command**: Test workflow automation and integration

### Integration Testing:
- Verify cross-component communication
- Test delegation patterns and context passing
- Validate end-to-end workflow scenarios
- Ensure consistent naming and conventions

### Documentation Generation:
- Create comprehensive usage guide
- Generate integration examples
- Document best practices and patterns
- Provide troubleshooting guidance

## Advanced Features:

### Smart Component Orchestration:
The command intelligently coordinates between components based on task complexity:
- Simple tasks → Helper command
- Domain-specific problems → Agent expert
- Deep knowledge needs → Skill expert
- Complex workflows → Combined usage

### Cross-Component Context:
Maintains context awareness between all three components:
- Shared terminology and conventions
- Consistent data structures and formats
- Unified error handling and logging
- Coordinated tool permissions

### Extensibility:
The generated expert system is designed for future enhancement:
- Plugin architecture for additional tools
- Modular skill components for specialization
- Configurable agent capabilities
- Extensible command interfaces

## Your Task:

Create a complete expert system for "$ARGUMENTS" using this orchestrated approach:

1. Parse the subject name, description, and domain from provided arguments
2. Research the subject domain using context7 for comprehensive understanding
3. Execute `/create-claude-agent` to create a specialized domain agent
4. Execute `/create-claude-skill` to develop a comprehensive knowledge skill
5. Execute `/create-claude-command` to build a domain helper utility
6. Integrate all components with proper cross-references and documentation
7. Validate the complete system and generate usage examples

If arguments are unclear or missing, ask the user for clarification about:
- Specific domain expertise needed
- Target frameworks or technologies
- Common tasks or workflows to automate
- Integration requirements with existing systems

## Notes:

- This command creates a comprehensive expertise package that may take several minutes to complete
- All three components will be cross-referenced and designed to work together
- The generated system follows established patterns for agents, skills, and commands
- Components can be used independently or as an integrated expert system
- Documentation and examples will be generated for each component and the complete system
