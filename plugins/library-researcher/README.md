# Library Researcher Plugin

**Advanced library research and documentation analysis plugin for Claude Code**

The Library Researcher plugin provides powerful tools for researching, analyzing, and documenting software libraries, frameworks, APIs, and development tools using the Context7 documentation system. It offers comprehensive analysis, comparisons, and practical guidance for any technology stack.

## Features

- **Intelligent Library Research**: Automatically resolves library names and retrieves comprehensive documentation
- **Comparative Analysis**: Compare multiple libraries, frameworks, or tools with detailed feature analysis
- **Integration Guidance**: Get specific integration examples and best practices for combining technologies
- **Up-to-date Documentation**: Access current documentation using Context7's extensive library database
- **Research Templates**: Use standardized templates for library analysis and comparison
- **Quality Assessment**: Evaluate documentation quality and library maintenance status

## Installation

Install the plugin using the Claude Code marketplace:

```bash
/plugin marketplace add library-researcher
```

Or install manually by cloning this repository into your plugins directory.

## Usage

### Basic Library Research

Ask Claude to research any library, framework, or tool:

```bash
# Research a specific library
"How do I use React for building web applications?"

# Compare libraries
"Should I use Express or FastAPI for my web API?"

# Integration research
"How do I integrate PostgreSQL with my Node.js application?"
```

### Advanced Research Patterns

The skill automatically handles complex research scenarios:

- **Single Library Analysis**: Deep dive into one library's capabilities and usage
- **Library Comparison**: Detailed comparison between multiple options
- **Integration Research**: How to combine different technologies
- **Technology Stack Planning**: Research entire development stacks
- **Migration Guidance**: Research alternatives and migration paths

### Supported Research Areas

#### Frontend Development
- UI frameworks: React, Vue, Angular, Svelte
- State management: Redux, MobX, Zustand, Jotai
- Build tools: Webpack, Vite, Rollup
- Testing: Jest, Cypress, Testing Library
- Styling: CSS-in-JS, Tailwind, Styled Components

#### Backend Development
- Web frameworks: Express, FastAPI, Django, Flask
- Databases: PostgreSQL, MongoDB, MySQL, Redis
- Authentication: Passport, Auth0, JWT libraries
- API tools: GraphQL, REST frameworks, OpenAPI
- Containerization: Docker, Kubernetes

#### Development Tools
- Code quality: ESLint, Prettier, TypeScript
- Testing: Jest, Mocha, Chai, Vitest
- Documentation: JSDoc, Swagger, Storybook
- CI/CD: GitHub Actions, GitLab CI, Jenkins

#### Data Science & AI
- Data processing: NumPy, Pandas, Apache Spark
- Machine learning: TensorFlow, PyTorch, Scikit-learn
- Visualization: Matplotlib, Plotly, D3.js
- Notebooks: Jupyter, Google Colab

## How It Works

### Research Workflow

1. **Library Identification**: Extract library names from your request
2. **ID Resolution**: Convert names to Context7-compatible library IDs
3. **Documentation Retrieval**: Fetch comprehensive documentation
4. **Analysis & Synthesis**: Extract key information and create actionable guidance
5. **Quality Assessment**: Evaluate documentation quality and recency

### Context7 Integration

The plugin leverages Context7's extensive documentation database:
- **Official Documentation**: Primary source for accurate information
- **Version-Specific Content**: Target specific library versions
- **Cross-Reference Data**: Links between related libraries
- **Community Insights**: Integration with community resources

### Research Templates

The skill includes standardized templates for:

- **Library Analysis**: Comprehensive single-library evaluation
- **Feature Comparison**: Side-by-side library comparison
- **Integration Guides**: Step-by-step integration instructions
- **Best Practices**: Recommended patterns and common pitfalls

## Examples

### Example 1: Frontend Framework Research

**User Query**: "I need to choose a frontend framework for my new project"

**Response Includes**:
- React vs Vue vs Angular comparison
- Performance benchmarks
- Learning curve analysis
- Ecosystem and community support
- Recommendation based on project requirements

### Example 2: Database Selection

**User Query**: "Which database should I use for my e-commerce platform?"

**Response Includes**:
- PostgreSQL vs MongoDB vs MySQL comparison
- Scalability analysis
- Performance characteristics
- Cost considerations
- Team expertise requirements
- Final recommendation with justification

### Example 3: API Integration

**User Query**: "How do I integrate Stripe payments in my Node.js application?"

**Response Includes**:
- Stripe Node.js SDK setup
- Code examples for common payment flows
- Security best practices
- Error handling patterns
- Testing recommendations

## Configuration

### Environment Setup

The plugin requires the Context7 MCP server to be properly configured in your Claude Code environment. Ensure that the following MCP tools are available:

- `mcp__context7__resolve-library-id`
- `mcp__context7__get-library-docs`

### Customization

You can customize the research behavior by:

- **Research Focus**: Specify particular areas of interest (API, setup, examples)
- **Version Targeting**: Request documentation for specific library versions
- **Depth Level**: Choose between overview or detailed research
- **Comparison Criteria**: Define custom criteria for library comparisons

## Best Practices

### For Effective Research

1. **Be Specific**: Provide context about your use case and requirements
2. **Mention Constraints**: Include information about your existing stack, team skills, or performance requirements
3. **Ask for Comparisons**: When evaluating options, request side-by-side comparisons
4. **Request Examples**: Ask for working code examples when possible
5. **Follow Up**: Ask follow-up questions for clarification or additional details

### Research Quality Tips

1. **Verify Versions**: Always check if the documentation matches your target version
2. **Cross-Reference**: Use multiple sources for critical decisions
3. **Test Examples**: Verify code examples work in your environment
4. **Consider Ecosystem**: Research related tools and compatibility
5. **Check Maintenance**: Verify library is actively maintained

## Troubleshooting

### Common Issues

**Library Not Found**
- Try alternative names or abbreviations
- Check if the library is in Context7's database
- Fall back to web search for official documentation

**Conflicting Information**
- Prioritize official documentation over community sources
- Check documentation dates and version compatibility
- Test different approaches when possible

**Outdated Documentation**
- Verify version numbers match your target
- Look for migration guides or changelogs
- Search for recent community tutorials

### Getting Help

1. **Check Examples**: Review the `examples/` directory for common use cases
2. **Use Templates**: Leverage research templates in `templates/`
3. **Community**: Join discussions in the repository issues
4. **Documentation**: Refer to Context7 documentation for advanced usage

## Contributing

We welcome contributions to improve the Library Researcher plugin:

- **New Research Patterns**: Add templates for new research scenarios
- **Library Support**: Help expand Context7 library coverage
- **Examples**: Contribute real-world research examples
- **Documentation**: Improve plugin documentation and guides

### Development Setup

```bash
# Clone the repository
git clone https://github.com/rigerc/claudecode.git
cd claudecode/plugins/library-researcher

# Run validation
make validate

# Test the plugin
make test
```

## Plugin Structure

```
library-researcher/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── skills/
│   └── library-researcher/
│       ├── SKILL.md             # Main skill definition
│       ├── references/          # Additional documentation
│       ├── assets/              # Images and media
│       ├── templates/           # Research templates
│       └── scripts/             # Utility scripts
└── README.md                    # This file
```

## License

This plugin is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for details.

## Version History

### v1.0.0
- Initial release
- Context7 integration
- Research templates
- Comprehensive library analysis
- Comparison framework
- Integration guidance

## Support

For support, questions, or feature requests:
- **Issues**: Create an issue in the repository
- **Discussions**: Join community discussions
- **Documentation**: Check the plugin wiki and examples

---

**The Library Researcher plugin ensures comprehensive, accurate, and practical library research for informed development decisions.**