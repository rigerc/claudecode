# Claude Code Extension Marketplace

> A curated collection of Claude Code extensions to enhance your development workflow

## 🚀 Quick Installation

Install this marketplace in Claude Code:

```bash
/plugin marketplace add rigerc/claudecode
```

Then install the extensions:

```bash
/plugin install claudecode-extensions
```

## 📦 Available Extensions

### 🔧 Development Tools
Commands for creating, reviewing, and managing code:

- **`feature-brainstorm`** - /feature-brainstorm [focus-area]
- **`create-command`** - This command helps you create a new Claude Code slash command using the official documentation from the working-with-claude-code skill
- **`create-skill`** - This command helps you create a new Claude Code Skill using the official documentation from the working-with-claude-code skill
- **`create-documentation`** - Use the generate-documentation skill to create comprehensive documentation for the specified target
- **`code-review`** - Perform comprehensive code quality review: $ARGUMENTS
- **`create-hook`** - This command helps you create a new Claude Code hook using the official documentation from the working-with-claude-code skill
- **`create-skill-from-documentation`** - Use the working-with-claude-code skill to create a new Agent Skill based on a documentation file specified by the user
- **`create-agent`** - This command helps you create a new Claude Code agent or sub-agent using the official documentation from the working-with-claude-code skill
- **`refactor-code`** - Intelligently refactor and improve code quality

### 🤖 Specialist Agents
Domain-specific expert agents:

- **`code-reviewer`** - You are a senior code reviewer ensuring high standards of code quality and security
- **`meta-agent`** - Your sole purpose is to act as an expert agent architect. You will take a user's prompt describing a new sub-agent and generate a complete, ready-to-use sub-agent configuration file in Markdown format. You will create and write this new file. Think hard about the user's prompt, and the documentation, and the tools available
- **`mcp-expert`** - You are an MCP (Model Context Protocol) expert specializing in creating, configuring, and optimizing MCP integrations for the claude-code-templates CLI system. You have deep expertise in MCP server architecture, protocol specifications, and integration patterns
- **`claude-optimizer`** - You are an expert optimizer for CLAUDE.md files - configuration documents that guide Claude Code's behavior in software repositories. Your specialized knowledge covers best practices for token optimization, attention patterns, and instruction effectiveness for Sonnet 4 and Opus 4 models
- **`bash-scripting-expert`** - You are an expert Bash scripting developer with years of experience in creating production-ready automation scripts, optimizing performance, and teaching modern Bash best practices. You specialize in transforming complex requirements into clean, efficient, and maintainable Bash solutions following the comprehensive style guide located at bash-style-guide/
- **`context-manager`** - You are a specialized context management agent responsible for maintaining coherent state across multiple agent interactions and sessions. Your role is critical for complex, long-running projects, especially those exceeding 10k tokens
- **`chezmoi`** - You are a Chezmoi dotfile management specialist focusing on secure, efficient configuration file management across multiple machines. Your expertise covers Chezmoi CLI operations, template creation, encryption setup, and workflow optimization
- **`technical-docs-writer`** - You are a senior technical writer and developer advocate specializing in creating clear, complete, user-facing documentation for software projects. Your audience is mid-level engineers who need to understand and successfully use the documented features
- **`readme-writer`** - You are a README documentation specialist who creates compelling, authentic documentation for developer-focused projects. Your expertise lies in crafting READMEs that drive adoption through clear value propositions, honest communication, and developer-centric content
- **`golang-pro`** - You are a Go expert specializing in concurrent, performant, and idiomatic Go code
- **`researcher`** - Context: User needs API documentation

### 📚 Documentation Tools
Generate and manage documentation:

- **`api-docs-generator`** - Automatically generate clean, comprehensive API documentation from multiple source formats and save to `/docs/API.md`. Supports OpenAPI/Swagger specifications, Python/JavaScript/TypeScript docstrings, JSDoc/TSDoc comments, and inline Markdown documentation
- **`generate-documentation`** - This skill researches, analyzes, and generates comprehensive documentation for software projects. It combines code analysis, library documentation research, and best practices to create clear, useful documentation that helps developers understand and use your code effectively

### 🛠️ Testing & Quality
Tools for testing, validation, and quality assurance:

- **`working-with-claude-code`** - This skill provides complete, authoritative documentation for Claude Code directly from docs.claude.com. Instead of guessing about configuration paths, API structures, or feature capabilities, read the official docs stored in this skill's references directory
- **`developing-claude-code-plugins`** - This skill provides efficient workflows for creating Claude Code plugins. Use it to make plugin development fast and correct - it synthesizes official docs into actionable steps and provides working examples
- **`bats-tester`** - This skill enables the creation of comprehensive tests for bash scripts using the bats-core framework. It provides templates, best practices, and workflows for setting up test environments, writing test cases, and organizing test suites effectively

### 🎵 Specialized Tools
Domain-specific utilities:

- **`beets`** - This skill provides comprehensive guidance for working with beets, the powerful music library management system and MusicBrainz tagger. It covers everything from initial library setup to advanced automation workflows, enabling efficient music collection management with precise metadata handling and organizational control

## 📊 Statistics

- **26 Extensions**: 9 commands, 6 skills, 11 agents
- **5 Categories**: Development, Agents, Documentation, Testing, Tools
- **Auto-updated**: Extensions are maintained and updated automatically

## 🔍 Usage Examples

After installation, extensions are immediately available:

```bash
# Create a new specialized agent
/create-agent

# Review your current code changes
/code-review

# Brainstorm new features for your project
/feature-brainstorm

# Generate comprehensive documentation
/generate-documentation api

# Refactor code for better performance
/refactor-code src/main.py
```

## ⚙️ Configuration

Most extensions work out-of-the-box. Some may need additional setup:

- **API Keys**: For external services and integrations
- **Git Access**: For repository-based operations
- **MCP Servers**: For protocol integrations
- **Development Tools**: For building and testing workflows

## 🤝 Contributing

Found an issue or have a suggestion?

- 🐛 [Report Issues](https://github.com/rigerc/claudecode/issues)
- 💡 [Request Features](https://github.com/rigerc/claudecode/discussions)
- 🔧 [Submit Pull Requests](https://github.com/rigerc/claudecode/pulls)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

*Last updated: Automatically generated*
