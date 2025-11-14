# Agent File Structure

Complete reference for Claude Code subagent file format and configuration options.

## File Format

Agents are Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When and why to use this agent
tools: Tool1, Tool2, Tool3  # Optional
model: sonnet  # Optional
---

System prompt goes here with detailed instructions.
```

## Configuration Fields

### name (Required)

- **Format**: Lowercase letters and hyphens only
- **Uniqueness**: Must be unique within scope (project/user/plugin)
- **Example**: `code-reviewer`, `test-runner`, `data-scientist`

### description (Required)

- **Purpose**: Tells Claude when to invoke this agent
- **Best practice**: Include trigger keywords and use cases
- **Proactive invocation**: Add "PROACTIVELY" or "MUST BE USED" for automatic delegation
- **Examples**:
  - `"Expert code reviewer. Use PROACTIVELY after writing or modifying code."`
  - `"Debugging specialist. MUST BE USED when encountering errors or test failures."`
  - `"Data analysis expert for SQL queries and BigQuery operations."`

### tools (Optional)

- **Default**: If omitted, inherits all tools from main conversation
- **Format**: Comma-separated list of tool names
- **Available tools**: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, etc.
- **MCP tools**: Available when inherited (omit tools field) or explicitly listed
- **Best practice**: Grant minimal necessary permissions
- **Examples**:
  - `tools: Read, Grep, Glob, Bash` - Read-only analysis
  - `tools: Read, Edit, Bash` - Code modification
  - Omitted - Full tool access including MCP

### model (Optional)

- **Options**:
  - `sonnet` - Claude Sonnet (default for agents)
  - `opus` - Claude Opus (most capable)
  - `haiku` - Claude Haiku (fastest, most cost-effective)
  - `inherit` - Use same model as main conversation
- **Default**: If omitted, uses configured subagent model (sonnet)
- **Use `inherit`**: When you want agents to match main conversation's model choice

## File Locations

### Priority Order

1. **Project agents** (`.claude/agents/`) - Highest priority
2. **CLI-defined agents** (`--agents` flag) - Medium priority
3. **User agents** (`~/.claude/agents/`) - Lower priority
4. **Plugin agents** (plugin directories) - Integrated seamlessly

### Project Agents

```bash
.claude/
└── agents/
    ├── code-reviewer.md
    ├── test-runner.md
    └── debugger.md
```

- Available only in current project
- Check into version control for team sharing
- Override user agents with same name

### User Agents

```bash
~/.claude/
└── agents/
    ├── personal-assistant.md
    └── data-analyst.md
```

- Available across all projects
- Personal agents for individual workflows
- Lower priority than project agents

### Plugin Agents

```bash
~/.claude/plugins/marketplaces/rigerc-claude/plugins/my-plugin/
└── agents/
    └── plugin-agent.md
```

- Provided by installed plugins
- Appear in `/agents` interface
- Can be customized by copying to project/user location

### CLI-Defined Agents

```bash
claude --agents '{
  "quick-reviewer": {
    "description": "Fast code review agent",
    "prompt": "Review code for obvious issues",
    "tools": ["Read", "Grep"],
    "model": "haiku"
  }
}'
```

- Defined at session start
- Useful for testing or automation
- Higher priority than user agents but lower than project agents

## System Prompt Structure

The system prompt (content after frontmatter) should include:

### 1. Role Definition

Clearly state the agent's role and expertise:

```markdown
You are a senior code reviewer specializing in security and performance.
```

### 2. When Invoked

Describe the immediate actions to take:

```markdown
When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately without asking for confirmation
```

### 3. Process and Approach

Detail the methodology:

```markdown
Review process:
- Analyze code for security vulnerabilities
- Check performance implications
- Verify error handling
- Assess test coverage
```

### 4. Output Format

Specify how to present results:

```markdown
Provide feedback organized by severity:
- Critical issues (must fix immediately)
- Warnings (should address)
- Suggestions (consider for improvement)

Include specific code examples for each issue.
```

### 5. Constraints and Guidelines

Add important rules and best practices:

```markdown
Guidelines:
- Never modify code without explaining the issue first
- Prioritize security over convenience
- Suggest idiomatic solutions for the language
- Keep recommendations actionable and specific
```

## Complete Example

```markdown
---
name: security-auditor
description: Security expert for code auditing. Use PROACTIVELY after handling sensitive operations like auth, data access, or API endpoints.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a security auditing specialist focused on identifying vulnerabilities in code.

When invoked:
1. Identify the scope (recent changes or specific files)
2. Use grep to search for common vulnerability patterns
3. Analyze authentication and authorization logic
4. Check for input validation issues
5. Review data handling and storage

Security checklist:
- SQL injection (parameterized queries?)
- XSS (proper output encoding?)
- CSRF (tokens implemented?)
- Authentication (secure password handling?)
- Authorization (proper access controls?)
- Secrets (no hardcoded credentials?)
- Input validation (whitelist approach?)
- Error handling (no information leakage?)

Report format:
For each finding, provide:
- Severity: Critical/High/Medium/Low
- Location: file:line
- Issue: Clear description of the vulnerability
- Impact: What could go wrong
- Fix: Specific code example of the solution
- Reference: Link to OWASP or security best practice

Focus on actionable findings that can be fixed immediately.
Never provide generic security advice without specific code locations.
```

## Validation

After creating an agent, verify the structure:

```bash
# Check file exists and is readable
cat .claude/agents/my-agent.md

# Test invocation
# In Claude Code:
> Use the my-agent agent to [task description]

# Verify in /agents interface
/agents
```

## Tips

- **Start with generation**: Let Claude generate the initial agent, then customize
- **Iterate**: Test the agent and refine the prompt based on results
- **Be specific**: Generic prompts lead to generic results
- **Include examples**: Show the agent what good output looks like
- **Limit scope**: Focused agents work better than generalists
- **Version control**: Commit project agents so team can improve them
