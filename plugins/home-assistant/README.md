# Home Assistant Plugin

A comprehensive Claude Code plugin for Home Assistant development, providing tools and skills for creating add-ons, integrations, and smart home automation workflows.

## 🏠 Overview

This plugin extends Claude Code with specialized capabilities for Home Assistant development, including:

- **Add-on Development**: Complete workflow for creating, building, and publishing Home Assistant add-ons
- **Integration Development**: Tools for building custom Home Assistant integrations
- **Smart Home Automation**: YAML automation and configuration expertise
- **Docker & Containerization**: Container security and optimization for Home Assistant services

## 🚀 Features

### Add-on Development Skill (`ha-addon`)

The core skill for Home Assistant add-on development provides expertise in:

- **Project Structure**: Proper directory layout and file organization
- **Configuration Management**: YAML configuration, build settings, and Docker files
- **Security Best Practices**: AppArmor profiles, API permissions, and security ratings
- **Building & Testing**: Docker builds, local testing, and CI/CD workflows
- **API Integration**: Home Assistant APIs, ingress, and authentication
- **Publishing**: Repository setup, versioning, and distribution

**When to use**: Claude automatically activates this skill when working with Home Assistant add-ons, Docker containers, YAML configuration, or related development tasks.

## 📁 Plugin Structure

```
plugins/home-assistant/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── skills/
│   └── ha-addon/
│       ├── SKILL.md         # Main skill file
│       ├── REFERENCE.md     # Complete reference guide
│       └── templates/       # Production-ready templates
│           ├── config.yaml
│           ├── Dockerfile
│           ├── build.yaml
│           ├── service-example.sh
│           ├── apparmor.txt
│           └── github-actions.yml
└── README.md                # This file
```

## 🛠️ Skills

### ha-addon - Home Assistant Add-on Development

**Description**: Create, build, and publish Home Assistant add-ons. Use when developing Home Assistant add-ons, troubleshooting container issues, configuring Docker-based services, or working with YAML configuration files for Home Assistant extensions.

**Allowed Tools**: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, TodoWrite

**Key Capabilities**:
- Complete add-on development workflow
- Security optimization and AppArmor configuration
- Multi-architecture building and CI/CD setup
- API integration and authentication
- Troubleshooting and debugging

## 🎯 Usage Examples

### Creating a New Add-on

```
I want to create a Home Assistant add-on for a web server
```

Claude will use the ha-addon skill to guide you through:
- Setting up the project structure
- Creating configuration files
- Implementing security best practices
- Setting up build and testing workflows

### Debugging Container Issues

```
My Home Assistant add-on container keeps crashing with permission errors
```

Claude will leverage the skill to:
- Analyze common permission issues
- Check volume mappings and security settings
- Provide debugging commands
- Suggest configuration fixes

### Optimizing Security

```
How can I improve the security rating of my Home Assistant add-on?
```

Claude will provide:
- Security rating system explanation
- AppArmor profile configuration
- Permission minimization strategies
- CodeNotary signing guidance

## 🔧 Installation

This plugin is part of the Claude Code Marketplace. To install:

1. **Via Marketplace**: Use the Claude Code marketplace commands to install the "home-assistant" plugin
2. **Manual Installation**: Clone this repository to your local plugins directory

Once installed, the skills will be automatically available in Claude Code.

## 📚 Documentation

### Skill Documentation

- **[ha-addon Skill Reference](skills/ha-addon/REFERENCE.md)**: Complete reference guide with commands, patterns, and troubleshooting
- **[Skill Templates](skills/ha-addon/templates/)**: Production-ready templates for common add-on patterns

### External Resources

- [Home Assistant Add-on Documentation](https://developers.home-assistant/docs/add-ons/)
- [Community Add-on Repository](https://github.com/hassio-addons/repository)
- [Home Assistant Developer Forums](https://community.home-assistant.io/c/developers/)

## 🤝 Contributing

This plugin welcomes contributions! Areas for enhancement:

- **Additional Skills**: Create skills for integration development, automation workflows, etc.
- **Template Improvements**: Enhance existing templates or add new patterns
- **Documentation**: Improve reference materials and examples
- **Bug Fixes**: Report and fix issues in existing functionality

### Adding New Skills

To add a new skill to this plugin:

1. Create a new directory in `skills/`
2. Follow the [Claude Code skill development guidelines](https://docs.claude.com/en/docs/claude-code/skills)
3. Update `plugin.json` to include the new skill
4. Add documentation and examples

### Development Setup

```bash
# Clone the marketplace repository
git clone https://github.com/rigerc/claude-code-marketplace.git
cd claude-code-marketplace/plugins/home-assistant

# Test skill changes locally
claude  # Skills will be automatically discovered
```

## 📄 License

This plugin is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Home Assistant development team for the excellent add-on framework
- Community contributors who share add-on examples and best practices
- Claude Code team for the extensible skill system

## 📞 Support

For issues, questions, or contributions:

- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Community**: Join the Home Assistant developer community

---

*Enhancing Home Assistant development with intelligent assistance.*