# Component Implementation Examples

Real-world examples showing complete component implementations.

## Real-World Command: /deploy

**File:** `commands/deploy.md`

```markdown
---
name: deploy
description: Deploy application to specified environment with validation and rollback support
---

# Deploy Command

Deploys the current application to the specified environment.

## Usage

```
/deploy [environment] [--skip-tests] [--force]
```

## Arguments

- `environment` (optional) - Target environment (staging, production). Default: staging
- `--skip-tests` - Skip pre-deployment tests
- `--force` - Force deployment even if validation fails

## Workflow

1. Validate environment configuration exists
2. Run pre-deployment tests (unless --skip-tests)
3. Build application artifacts
4. Upload to environment
5. Run health checks
6. Report deployment status

## Error Handling

If deployment fails:
- Automatically trigger rollback
- Report failure reason
- Suggest corrective actions

## Examples

Deploy to staging (default):
```
/deploy
```

Deploy to production with confirmation:
```
/deploy production
```

Force deploy, skipping tests:
```
/deploy production --skip-tests --force
```

## Implementation

Use the deployment agent for AWS-specific operations. The agent has access to AWS CLI MCP server and handles:
- Credential management
- Resource validation
- Deployment orchestration
- Rollback procedures

Report progress at each stage and ask for confirmation before production deployments.
```

## Real-World Agent: AWS Deployment Specialist

**File:** `agents/aws-specialist.md`

```markdown
---
name: aws-specialist
description: Specialized agent for AWS deployments, infrastructure management, and security best practices. Delegates to this agent when tasks involve AWS services, CloudFormation, ECS, Lambda, or infrastructure as code.
---

# AWS Deployment Specialist

Expert agent for AWS operations with deep knowledge of deployment patterns, security, and troubleshooting.

## Capabilities

- Deploy applications to ECS, Lambda, EC2
- Manage CloudFormation stacks
- Configure security groups and IAM policies
- Monitor CloudWatch metrics and logs
- Implement rollback strategies

## Tool Access

This agent has access to:
- AWS CLI (via MCP server)
- CloudFormation validation tools
- Security scanning utilities
- Deployment scripts in skills/aws-deploy/scripts/

## Delegation Triggers

Delegate to this agent when:
- User invokes /deploy, /rollback, or /status commands
- AWS-related questions about infrastructure
- Debugging deployment failures
- Reviewing security configurations
- Setting up new AWS resources

## Workflow

1. Validate AWS credentials and region configuration
2. Check current state of target resources
3. Plan deployment changes
4. Execute with progress reporting
5. Verify deployment success
6. Configure monitoring and alerts

## Restrictions

- Never deploy to production without explicit user confirmation
- Always validate IAM policies for least-privilege access
- Require MFA for sensitive operations
- Document all infrastructure changes

## Error Recovery

If deployment fails:
1. Capture error details from CloudWatch
2. Analyze failure reason
3. Suggest specific fixes
4. Offer automatic rollback if available
```

## Real-World Skill: Testing Workflow

**File:** `skills/pytest-runner/SKILL.md`

```markdown
---
name: pytest-runner
description: This skill should be used when running Python tests, analyzing test results, debugging test failures, or setting up test environments. Provides bundled test runner scripts and pytest configuration guidance.
---

# Pytest Runner Skill

Comprehensive testing workflow for Python projects using pytest.

## Purpose

Automates test execution, result analysis, and failure debugging with bundled scripts and reference documentation.

## When to Use

Apply this skill when:
- Running unit, integration, or end-to-end tests
- Debugging test failures
- Analyzing test coverage
- Setting up pytest configuration
- Generating test reports

## Workflow

1. **Discover tests** - Use bundled script to find all test files
2. **Run tests** - Execute with appropriate pytest flags
3. **Analyze results** - Parse output for failures, skips, warnings
4. **Debug failures** - Show failure details with context
5. **Report coverage** - Generate and interpret coverage data

## Using Bundled Resources

**scripts/run_tests.py**
Execute to run pytest with standardized configuration:

```bash
python scripts/run_tests.py [--coverage] [--verbose] [--markers <marker>]
```

Options:
- `--coverage` - Generate coverage report
- `--verbose` - Detailed output
- `--markers` - Run only tests with specific marker

**references/pytest-patterns.md**
Load for pytest best practices, fixture patterns, and parameterization examples.

**references/coverage-guide.md**
Load when analyzing coverage reports or setting coverage thresholds.

## Common Patterns

**Run all tests:**
```bash
python scripts/run_tests.py
```

**Run with coverage:**
```bash
python scripts/run_tests.py --coverage
```

**Run specific marker:**
```bash
python scripts/run_tests.py --markers integration
```

## Failure Analysis

When tests fail:
1. Show failure count and categories
2. Display first failure with full traceback
3. Identify common patterns (import errors, assertion failures, etc.)
4. Suggest fixes based on error type
5. Offer to run single failing test for debugging
```

## Real-World Hook: Pre-Commit Validation

**File:** `hooks/hooks.json`

```json
{
  "PostToolUse": {
    "Edit": [
      {
        "description": "Validate Python files after editing",
        "command": "python hooks/scripts/validate_python.py \"${file_path}\"",
        "filter": {
          "filePattern": "**/*.py"
        },
        "continueOnError": false
      }
    ],
    "Write": [
      {
        "description": "Format Python files after creation",
        "command": "black \"${file_path}\" && ruff check --fix \"${file_path}\"",
        "filter": {
          "filePattern": "**/*.py"
        },
        "continueOnError": true
      }
    ]
  },
  "PreToolUse": {
    "Bash": [
      {
        "description": "Warn before destructive git operations",
        "command": "hooks/scripts/git_safety_check.sh \"${command}\"",
        "filter": {
          "patterns": ["git push --force", "git reset --hard", "git clean -fd"]
        },
        "continueOnError": false
      }
    ]
  },
  "AgentStart": [
    {
      "description": "Log agent activation for audit trail",
      "command": "echo \"[$(date)] Agent started: ${agent_name}\" >> .claude/agent-log.txt",
      "continueOnError": true
    }
  ]
}
```

## Real-World MCP Server: GitHub API

**File:** `.mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub API integration for repository operations"
    },
    "aws-cli": {
      "command": "python",
      "args": [
        "-m",
        "mcp_aws_cli"
      ],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_PROFILE": "default"
      },
      "description": "AWS CLI integration for cloud operations"
    },
    "custom-api": {
      "command": "/usr/local/bin/custom-mcp-server",
      "args": ["--port", "3000"],
      "env": {
        "API_KEY": "${CUSTOM_API_KEY}",
        "API_URL": "https://api.example.com"
      },
      "description": "Custom API server for company-specific integrations"
    }
  }
}
```
