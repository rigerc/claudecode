# Agent Creation Best Practices

Proven patterns and recommendations for creating effective Claude Code subagents.

## Design Principles

### Single Responsibility

Each agent should have one clear purpose:

**Good:**
- `code-reviewer` - Reviews code quality and security
- `test-runner` - Runs tests and fixes failures
- `debugger` - Investigates and fixes bugs

**Avoid:**
- `code-helper` - Too vague, tries to do everything
- `dev-assistant` - Unclear when to use it

### Detailed System Prompts

Agents work best with explicit instructions:

**Good:**
```markdown
You are a test automation expert.

When invoked:
1. Identify the relevant test suite (unit/integration/e2e)
2. Run the tests using the appropriate command
3. If tests fail, analyze the failure output
4. Fix the failing tests while preserving test intent
5. Re-run to verify the fix

Testing principles:
- Never skip or disable failing tests
- Maintain test isolation
- Keep tests fast and focused
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
```

**Avoid:**
```markdown
You are a testing expert. Help with tests.
```

### Minimal Tool Access

Grant only necessary permissions:

**Code reviewer** (read-only analysis):
```yaml
tools: Read, Grep, Glob, Bash
```

**Test runner** (needs execution):
```yaml
tools: Read, Edit, Bash
```

**Full development** (comprehensive access):
```yaml
# Omit tools field to inherit all
```

### Proactive Invocation

Use trigger words in descriptions to enable automatic delegation:

**Proactive agents:**
```yaml
description: Expert code reviewer. Use PROACTIVELY after writing or modifying code.
description: Test runner. MUST BE USED when code changes require testing.
description: Security auditor. Use PROACTIVELY for auth, API, or data handling code.
```

**On-demand agents:**
```yaml
description: Performance profiler for identifying bottlenecks.
description: Documentation generator for API endpoints.
```

## Common Patterns

### Code Analysis Agent

**Purpose**: Review code without modifications

```yaml
tools: Read, Grep, Glob, Bash
```

**System prompt structure**:
1. Run `git diff` to see changes
2. Analyze specific aspects (security, performance, style)
3. Provide categorized feedback
4. Include specific examples

### Code Modification Agent

**Purpose**: Make code changes

```yaml
tools: Read, Edit, Write, Bash
```

**System prompt structure**:
1. Understand the requirement
2. Identify files to modify
3. Make minimal, focused changes
4. Verify changes work (run tests/build)
5. Explain what was changed and why

### Testing Agent

**Purpose**: Run tests and fix failures

```yaml
tools: Read, Edit, Bash
```

**System prompt structure**:
1. Determine test type and command
2. Run tests and capture output
3. For failures, identify root cause
4. Fix code or tests as appropriate
5. Verify fix resolves the issue

### Research Agent

**Purpose**: Gather information from codebase

```yaml
tools: Read, Grep, Glob, Bash, WebFetch
```

**System prompt structure**:
1. Understand the research question
2. Search codebase systematically
3. Read relevant files
4. Synthesize findings
5. Present organized summary with file:line references

## Workflow Recommendations

### 1. Start with Claude Generation

**Recommended approach**:
```
> Generate a code reviewer agent that focuses on security and performance
```

Claude will create a complete agent structure. Then customize:
- Adjust tool permissions
- Add domain-specific guidelines
- Include team coding standards
- Add project-specific patterns to check

**Why this works**:
- Gets you a solid foundation quickly
- Ensures proper structure
- You can iterate from working example
- Easier than starting from scratch

### 2. Iterate and Refine

**Process**:
1. Create initial agent
2. Test with real tasks
3. Note what works and what doesn't
4. Refine system prompt based on results
5. Repeat until agent performs reliably

**Common refinements**:
- Add more specific instructions for edge cases
- Clarify output format expectations
- Add constraints for common mistakes
- Include examples of good/bad outputs

### 3. Share and Collaborate

**For teams**:
- Store agents in `.claude/agents/` (project level)
- Commit to version control
- Document agent purpose in README
- Review and improve agents together
- Share effective patterns across projects

**For individuals**:
- Store personal agents in `~/.claude/agents/`
- Override with project-specific versions when needed
- Build a library of reusable agents

## Anti-Patterns

### Avoid These Mistakes

**Too Generic**
```yaml
name: helper
description: Helps with code
```
Problem: Unclear when to use, no specific expertise

**Too Broad**
```markdown
You are an expert in everything. Do whatever the user asks.
```
Problem: No focus, won't perform well at anything specific

**Too Restrictive**
```markdown
Never make any changes without asking first.
Never run any commands without permission.
Always explain in detail before taking action.
```
Problem: Agent becomes passive and slow, defeats purpose of delegation

**Insufficient Instructions**
```markdown
Review the code and provide feedback.
```
Problem: No guidance on what to look for or how to report findings

**Tool Overload**
```yaml
tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite, Skill, SlashCommand
```
Problem: Too many tools makes agent unfocused and slower. Grant minimal necessary access.

## Model Selection

### When to Use Each Model

**Haiku** (fastest, most cost-effective):
```yaml
model: haiku
```
- Simple, repetitive tasks
- Fast iterations (e.g., format checks)
- Well-defined procedures
- Example: Code formatter, linter wrapper

**Sonnet** (balanced, recommended default):
```yaml
model: sonnet
# or omit for default
```
- Most agent tasks
- Code review
- Testing
- Debugging
- Good balance of capability and speed

**Opus** (most capable):
```yaml
model: opus
```
- Complex reasoning required
- Architecture decisions
- Difficult debugging
- Novel problem-solving
- Use sparingly due to cost/latency

**Inherit** (match main conversation):
```yaml
model: inherit
```
- When agent should match user's model choice
- Ensures consistency in reasoning style
- Good for agents that extend main conversation

## Testing Agents

### Initial Testing

**Explicit invocation**:
```
> Use the code-reviewer agent to check my recent changes
```

**Verify behavior**:
- Does it follow the system prompt?
- Are outputs in expected format?
- Does it use tools appropriately?
- Is it too passive or too aggressive?

### Refinement Testing

**Test edge cases**:
- Empty results
- Multiple files
- Large codebases
- Error conditions

**Check tool usage**:
- Uses minimal necessary tools
- Doesn't overuse expensive operations
- Handles tool failures gracefully

## Context Management

### Keep Agents Focused

Agents have separate context windows, which is a feature:

**Good - Focused delegation**:
```
> Use the security-auditor agent to check authentication code
> Use the test-runner agent to verify all tests pass
```

**Avoid - Context dependency**:
```
> Use the code-reviewer agent and remember to also check the database schema we discussed earlier and apply the guidelines from the previous review
```

Problem: Agent doesn't have context from main conversation. Keep each agent invocation self-contained.

### Self-Contained Instructions

Agents should be able to work with minimal context:

**Good system prompt**:
```markdown
When invoked:
1. Run git diff to identify recent changes
2. Focus analysis on modified files
3. Begin immediately with available information
```

**Avoid**:
```markdown
When invoked:
1. Ask user which files to review
2. Wait for confirmation before starting
3. Request clarification on requirements
```

## Documentation

### Document Agent Purpose

Add to project README:

```markdown
## Claude Code Agents

### code-reviewer
Reviews code for security, performance, and best practices.
Runs automatically after code changes.

### test-runner
Runs relevant tests and fixes failures.
Invoke with: "run tests"

### debugger
Investigates errors and unexpected behavior.
Invoke when encountering bugs.
```

### Share Effective Patterns

When you create a particularly effective agent:
1. Document what makes it work well
2. Share the pattern with your team
3. Consider contributing to community examples
4. Adapt pattern for other use cases

## Performance Tips

### Optimize for Speed

**Fast agents**:
- Use `model: haiku` for simple tasks
- Limit tool access to essentials
- Provide clear, focused instructions
- Minimize back-and-forth

**Complex agents**:
- Use `model: sonnet` or `opus` when needed
- Accept longer response times for better results
- Break complex tasks into multiple focused agents

### Reduce Context Pollution

Use agents to keep main conversation focused:

**Instead of**:
```
> Analyze all files in src/ for performance issues
[Main conversation fills with analysis details]
```

**Better**:
```
> Use the performance-analyzer agent to review src/
[Agent returns summary, details stay in agent context]
```

## Maintenance

### Keep Agents Updated

As projects evolve:
- Update agent prompts with new patterns
- Adjust tool permissions as needed
- Archive unused agents
- Document changes in commit messages

### Regular Review

Periodically review agents:
- Are they still being used?
- Do they need refinement?
- Can they be simplified?
- Should they be split or merged?

### Version Control

Treat agents like code:
- Commit with descriptive messages
- Review changes in PRs
- Test before merging
- Document breaking changes
