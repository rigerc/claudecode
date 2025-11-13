---
name: bats-tester
description: Use when creating tests for bash scripts using bats-core. Provides expertise in test writing, setup, and best practices.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
---

# Bats Testing Framework Expert

Expert assistance for testing bash scripts with bats-core, providing test patterns, setup guidance, and best practices.

## When to Use This Skill

Use this skill when you need help with:

- Writing .bats test files and test cases
- Setting up bats-core test environments
- Using bats-assert and bats-support libraries
- Test organization and project structure
- Mocking, fixtures, and test helpers
- Debugging test failures

## Quick Start

```bash
#!/usr/bin/env bats

@test "script runs successfully" {
  run ./script.sh
  [ "$status" -eq 0 ]
}

@test "script produces expected output" {
  run ./script.sh arg1
  [ "$status" -eq 0 ]
  [[ "$output" == *"expected"* ]]
}
```

## Available Resources

See `references/` for comprehensive documentation:

- **detailed-guide.md**: Complete testing guide and workflows
- **setup-guide.md**: Project structure and initialization
- **testing-patterns.md**: Assertions, setup/teardown, and common patterns
- **assertion_patterns.md**: Detailed assertion library reference
- **bats_functions.md**: Core bats function reference
- **test_organization.md**: Organizing tests and project structure
- **advanced-techniques.md**: Mocking, fixtures, and complex scenarios
- **troubleshooting.md**: Common issues and debugging techniques