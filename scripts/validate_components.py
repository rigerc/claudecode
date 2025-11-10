#!/usr/bin/env python3
"""
Claude Code Component Validator

Comprehensive validation script for Claude Code components (hooks, skills, commands, agents).
Validates structure, schema, and format according to official reference documentation.

Usage:
    python validate_components.py --plugin /path/to/plugin
    python validate_components.py --hooks /path/to/hooks.json
    python validate_components.py --skill /path/to/skill
    python validate_components.py --command /path/to/command.md
    python validate_components.py --agent /path/to/agent.md
    python validate_components.py --all /path/to/plugins/dir
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# ANSI color codes for better UX
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class ValidationResult:
    """Container for validation results"""

    def __init__(
        self,
        is_valid: bool,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        severity: str = "error",
    ):
        self.is_valid = is_valid
        self.message = message
        self.line = line
        self.column = column
        self.severity = severity  # error, warning, info

    def __str__(self):
        location = ""
        if self.line is not None:
            location = f":{self.line}"
            if self.column is not None:
                location += f":{self.column}"

        color = (
            Colors.RED
            if self.severity == "error"
            else Colors.YELLOW
            if self.severity == "warning"
            else Colors.CYAN
        )
        return f"{color}{self.severity.upper()}{Colors.END}{location}: {self.message}"


class ComponentValidator:
    """Base class for component validators"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.results: List[ValidationResult] = []

    def add_result(
        self,
        is_valid: bool,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        severity: str = "error",
    ):
        """Add a validation result"""
        self.results.append(ValidationResult(is_valid, message, line, column, severity))

    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return any(not r.is_valid and r.severity == "error" for r in self.results)

    def print_results(self):
        """Print validation results with colors"""
        if not self.results:
            print(f"{Colors.GREEN}✓{Colors.END} {self.file_path}: No issues found")
            return

        print(f"\n{Colors.BOLD}Validation results for {self.file_path}:{Colors.END}")

        for result in self.results:
            print(f"  {result}")

        errors = sum(
            1 for r in self.results if not r.is_valid and r.severity == "error"
        )
        warnings = sum(
            1 for r in self.results if not r.is_valid and r.severity == "warning"
        )

        if errors > 0:
            print(f"\n{Colors.RED}✗{Colors.END} {errors} error(s) found")
        if warnings > 0:
            print(f"{Colors.YELLOW}⚠{Colors.END} {warnings} warning(s) found")
        if errors == 0 and warnings == 0:
            print(f"\n{Colors.GREEN}✓{Colors.END} All checks passed")


class HooksValidator(ComponentValidator):
    """Validator for hooks.json files"""

    VALID_EVENTS = {
        "PreToolUse",
        "PostToolUse",
        "Notification",
        "UserPromptSubmit",
        "Stop",
        "SubagentStop",
        "PreCompact",
        "SessionStart",
        "SessionEnd",
    }

    VALID_SESSION_START_MATCHERS = {"startup", "resume", "clear", "compact"}
    VALID_PRECOMPACT_MATCHERS = {"manual", "auto"}
    VALID_SESSION_END_REASONS = {"clear", "logout", "prompt_input_exit", "other"}

    def validate(self):
        """Validate hooks.json structure and content"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.add_result(False, f"Invalid JSON: {e.msg}", e.lineno, e.colno)
            return
        except Exception as e:
            self.add_result(False, f"Failed to read file: {e}")
            return

        # Validate top-level structure
        if not isinstance(data, dict):
            self.add_result(False, "Root must be a JSON object")
            return

        # Validate optional description field
        if "description" in data:
            if not isinstance(data["description"], str):
                self.add_result(False, "Description must be a string")

        # Validate hooks field
        if "hooks" not in data:
            self.add_result(False, "Missing required 'hooks' field")
            return

        hooks = data["hooks"]
        if not isinstance(hooks, dict):
            self.add_result(False, "Hooks must be a JSON object")
            return

        # Validate each event
        for event_name, event_hooks in hooks.items():
            self._validate_event(event_name, event_hooks)

    def _validate_event(self, event_name: str, event_hooks: Any):
        """Validate a single event configuration"""
        if event_name not in self.VALID_EVENTS:
            self.add_result(
                False,
                f"Invalid event name '{event_name}'. Valid events: {', '.join(sorted(self.VALID_EVENTS))}",
            )
            return

        if not isinstance(event_hooks, list):
            self.add_result(False, f"Event '{event_name}' must be a list")
            return

        for i, hook_config in enumerate(event_hooks):
            self._validate_hook_config(event_name, hook_config, i)

    def _validate_hook_config(self, event_name: str, hook_config: Any, index: int):
        """Validate a single hook configuration"""
        if not isinstance(hook_config, dict):
            self.add_result(
                False, f"Hook configuration at index {index} must be a JSON object"
            )
            return

        # Validate matcher field (optional for some events)
        if "matcher" in hook_config:
            matcher = hook_config["matcher"]
            if not isinstance(matcher, str):
                self.add_result(
                    False, f"Matcher must be a string", None, None, "warning"
                )
            else:
                self._validate_matcher(event_name, matcher)

        # Validate hooks field
        if "hooks" not in hook_config:
            self.add_result(
                False, f"Missing 'hooks' field in hook configuration at index {index}"
            )
            return

        hooks_list = hook_config["hooks"]
        if not isinstance(hooks_list, list):
            self.add_result(
                False,
                f"Hooks field must be a list in hook configuration at index {index}",
            )
            return

        for j, hook in enumerate(hooks_list):
            self._validate_single_hook(event_name, hook, index, j)

    def _validate_matcher(self, event_name: str, matcher: str):
        """Validate matcher value for specific events"""
        if (
            event_name == "SessionStart"
            and matcher not in self.VALID_SESSION_START_MATCHERS
        ):
            self.add_result(
                False,
                f"Invalid matcher '{matcher}' for SessionStart. Valid: {', '.join(sorted(self.VALID_SESSION_START_MATCHERS))}",
                None,
                None,
                "warning",
            )
        elif (
            event_name == "PreCompact" and matcher not in self.VALID_PRECOMPACT_MATCHERS
        ):
            self.add_result(
                False,
                f"Invalid matcher '{matcher}' for PreCompact. Valid: {', '.join(sorted(self.VALID_PRECOMPACT_MATCHERS))}",
                None,
                None,
                "warning",
            )

    def _validate_single_hook(
        self, event_name: str, hook: Any, config_index: int, hook_index: int
    ):
        """Validate a single hook definition"""
        if not isinstance(hook, dict):
            self.add_result(False, f"Hook at index {hook_index} must be a JSON object")
            return

        # Validate type field
        if "type" not in hook:
            self.add_result(
                False, f"Missing 'type' field in hook at index {hook_index}"
            )
            return

        hook_type = hook["type"]
        if hook_type != "command":
            self.add_result(
                False, f"Invalid hook type '{hook_type}'. Only 'command' is supported"
            )
            return

        # Validate command field
        if "command" not in hook:
            self.add_result(
                False, f"Missing 'command' field in hook at index {hook_index}"
            )
            return

        command = hook["command"]
        if not isinstance(command, str):
            self.add_result(
                False, f"Command must be a string in hook at index {hook_index}"
            )
            return

        if not command.strip():
            self.add_result(
                False, f"Command cannot be empty in hook at index {hook_index}"
            )
            return

        # Validate optional timeout field
        if "timeout" in hook:
            timeout = hook["timeout"]
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                self.add_result(
                    False,
                    f"Timeout must be a positive number in hook at index {hook_index}",
                )

        # Check for common issues
        if "${CLAUDE_PLUGIN_ROOT}" in command and event_name not in [
            "SessionStart",
            "PreToolUse",
            "PostToolUse",
        ]:
            self.add_result(
                True, f"Using CLAUDE_PLUGIN_ROOT variable", None, None, "info"
            )

        if "$CLAUDE_PROJECT_DIR" in command:
            self.add_result(
                True, f"Using CLAUDE_PROJECT_DIR variable", None, None, "info"
            )


class SkillValidator(ComponentValidator):
    """Validator for SKILL.md files"""

    REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}
    OPTIONAL_FRONTMATTER_FIELDS = {"allowed-tools", "model"}
    ALL_FRONTMATTER_FIELDS = REQUIRED_FRONTMATTER_FIELDS | OPTIONAL_FRONTMATTER_FIELDS

    def validate(self):
        """Validate SKILL.md structure and content"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.add_result(False, f"Failed to read file: {e}")
            return

        # Check for YAML frontmatter
        if not content.startswith("---\n"):
            self.add_result(False, "SKILL.md must start with YAML frontmatter (---)")
            return

        # Extract frontmatter
        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                self.add_result(False, "Missing closing frontmatter delimiter (---)")
                return

            frontmatter_str = parts[1].strip()
            markdown_content = parts[2].strip()

            # Parse YAML frontmatter (basic parsing)
            try:
                frontmatter = self._parse_basic_yaml(frontmatter_str)
                if not isinstance(frontmatter, dict):
                    self.add_result(False, "Frontmatter must be a YAML object")
                    return
            except Exception as e:
                self.add_result(
                    False,
                    f"Invalid frontmatter: {e}. Install PyYAML for better validation",
                )
                return

            # Validate frontmatter fields
            self._validate_frontmatter(frontmatter)

            # Validate markdown content
            self._validate_markdown_content(markdown_content)

        except Exception as e:
            self.add_result(False, f"Error parsing SKILL.md: {e}")

    def _parse_basic_yaml(self, yaml_str: str) -> Dict[str, Any]:
        """Very basic YAML parser for simple key: value pairs"""
        result = {}
        for line in yaml_str.split("\n"):
            line = line.strip()
            if line and ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                result[key] = value
        return result

    def _validate_frontmatter(self, frontmatter: Dict[str, Any]):
        """Validate YAML frontmatter"""
        # Check required fields
        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if field not in frontmatter:
                self.add_result(False, f"Missing required frontmatter field: {field}")
            elif not isinstance(frontmatter[field], str):
                self.add_result(False, f"Frontmatter field '{field}' must be a string")

        # Check for unknown fields
        for field in frontmatter:
            if field not in self.ALL_FRONTMATTER_FIELDS:
                self.add_result(
                    False, f"Unknown frontmatter field: {field}", None, None, "warning"
                )

        # Validate allowed-tools if present
        if "allowed-tools" in frontmatter:
            allowed_tools = frontmatter["allowed-tools"]
            if isinstance(allowed_tools, str):
                # Comma-separated list
                tools = [tool.strip() for tool in allowed_tools.split(",")]
                self._validate_tool_names(tools)
            elif isinstance(allowed_tools, list):
                self._validate_tool_names(allowed_tools)
            else:
                self.add_result(False, "allowed-tools must be a string or list")

        # Validate description quality
        if "description" in frontmatter:
            desc = frontmatter["description"]
            if len(desc) < 10:
                self.add_result(
                    False,
                    "Description should be more descriptive (at least 10 characters)",
                    None,
                    None,
                    "warning",
                )
            elif "use when" not in desc.lower():
                self.add_result(
                    False,
                    "Description should include when to use the skill",
                    None,
                    None,
                    "warning",
                )

    def _validate_tool_names(self, tools: List[str]):
        """Validate tool names in allowed-tools"""
        valid_tools = {
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Bash",
            "LS",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "Task",
            "SlashCommand",
        }

        for tool in tools:
            tool = tool.strip()
            if tool not in valid_tools:
                self.add_result(
                    False,
                    f"Unknown tool in allowed-tools: {tool}",
                    None,
                    None,
                    "warning",
                )

    def _validate_markdown_content(self, content: str):
        """Validate markdown content structure"""
        if not content.strip():
            self.add_result(False, "SKILL.md cannot be empty after frontmatter")
            return

        lines = content.split("\n")

        # Check for main heading
        has_heading = any(line.strip().startswith("# ") for line in lines)
        if not has_heading:
            self.add_result(
                False,
                "SKILL.md should have a main heading (# Skill Name)",
                None,
                None,
                "warning",
            )

        # Check for sections
        has_instructions = any("instruction" in line.lower() for line in lines)
        has_examples = any("example" in line.lower() for line in lines)

        if not has_instructions:
            self.add_result(
                False, "Consider adding an Instructions section", None, None, "info"
            )

        if not has_examples:
            self.add_result(
                False, "Consider adding an Examples section", None, None, "info"
            )

        # Check for common file references
        file_refs = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for ref_text, ref_path in file_refs:
            if ref_path.startswith("./") or ref_path.startswith("../"):
                self.add_result(
                    True,
                    f"Found relative file reference: {ref_path}",
                    None,
                    None,
                    "info",
                )


class CommandValidator(ComponentValidator):
    """Validator for command markdown files"""

    VALID_FRONTMATTER_FIELDS = {
        "description",
        "allowed-tools",
        "argument-hint",
        "model",
        "disable-model-invocation",
    }

    def validate(self):
        """Validate command markdown file"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.add_result(False, f"Failed to read file: {e}")
            return

        # Check for optional frontmatter
        if content.startswith("---\n"):
            self._validate_frontmatter(content)
            # Extract content after frontmatter
            parts = content.split("---", 2)
            if len(parts) >= 3:
                markdown_content = parts[2].strip()
            else:
                markdown_content = ""
        else:
            markdown_content = content.strip()

        # Validate markdown content
        self._validate_markdown_content(markdown_content)

    def _validate_frontmatter(self, content: str):
        """Validate YAML frontmatter"""
        try:
            parts = content.split("---", 2)
            if len(parts) < 2:
                self.add_result(False, "Invalid frontmatter format")
                return

            frontmatter_str = parts[1].strip()
            frontmatter = self._parse_basic_yaml(frontmatter_str)

            if not isinstance(frontmatter, dict):
                self.add_result(False, "Frontmatter must be a YAML object")
                return

            # Validate fields
            for field in frontmatter:
                if field not in self.VALID_FRONTMATTER_FIELDS:
                    self.add_result(
                        False,
                        f"Unknown frontmatter field: {field}",
                        None,
                        None,
                        "warning",
                    )

            # Validate description
            if "description" in frontmatter:
                desc = frontmatter["description"]
                if not isinstance(desc, str):
                    self.add_result(False, "Description must be a string")
                elif len(desc) < 5:
                    self.add_result(
                        False,
                        "Description should be more descriptive",
                        None,
                        None,
                        "warning",
                    )

            # Validate allowed-tools
            if "allowed-tools" in frontmatter:
                allowed_tools = frontmatter["allowed-tools"]
                if isinstance(allowed_tools, str):
                    tools = [tool.strip() for tool in allowed_tools.split(",")]
                    self._validate_tool_names(tools)
                elif isinstance(allowed_tools, list):
                    self._validate_tool_names(allowed_tools)
                else:
                    self.add_result(False, "allowed-tools must be a string or list")

            # Validate argument-hint
            if "argument-hint" in frontmatter:
                hint = frontmatter["argument-hint"]
                if not isinstance(hint, str):
                    self.add_result(False, "argument-hint must be a string")

            # Validate disable-model-invocation
            if "disable-model-invocation" in frontmatter:
                disable = frontmatter["disable-model-invocation"]
                if not isinstance(disable, bool):
                    self.add_result(False, "disable-model-invocation must be a boolean")

        except Exception as e:
            self.add_result(
                False, f"Invalid frontmatter: {e}. Install PyYAML for better validation"
            )

    def _parse_basic_yaml(self, yaml_str: str) -> Dict[str, Any]:
        """Very basic YAML parser for simple key: value pairs"""
        result = {}
        for line in yaml_str.split("\n"):
            line = line.strip()
            if line and ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # Handle boolean values
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                result[key] = value
        return result

    def _validate_tool_names(self, tools: List[str]):
        """Validate tool names in allowed-tools"""
        valid_tools = {
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Bash",
            "LS",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "Task",
            "SlashCommand",
        }

        for tool in tools:
            tool = tool.strip()
            # Handle tool-specific syntax like "Bash(git add:*)"
            if "(" in tool:
                base_tool = tool.split("(")[0]
                if base_tool not in valid_tools:
                    self.add_result(
                        False,
                        f"Unknown tool in allowed-tools: {base_tool}",
                        None,
                        None,
                        "warning",
                    )
            else:
                if tool not in valid_tools:
                    self.add_result(
                        False,
                        f"Unknown tool in allowed-tools: {tool}",
                        None,
                        None,
                        "warning",
                    )

    def _validate_markdown_content(self, content: str):
        """Validate markdown content"""
        if not content:
            self.add_result(False, "Command file cannot be empty")
            return

        lines = content.split("\n")

        # Check for argument placeholders
        has_arguments = any("$" in line for line in lines)
        if has_arguments:
            # Check for valid argument patterns
            for i, line in enumerate(lines):
                if "$ARGUMENTS" in line or re.search(r"\$\d+", line):
                    self.add_result(
                        True,
                        f"Found argument placeholder on line {i + 1}",
                        None,
                        None,
                        "info",
                    )

        # Check for bash command execution
        has_bash = any("!`" in line for line in lines)
        if has_bash:
            self.add_result(True, "Found bash command execution", None, None, "info")

        # Check for file references
        has_file_refs = any("@" in line for line in lines)
        if has_file_refs:
            self.add_result(True, "Found file references", None, None, "info")


class AgentValidator(ComponentValidator):
    """Validator for agent markdown files"""

    REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}
    OPTIONAL_FRONTMATTER_FIELDS = {"tools", "model"}
    ALL_FRONTMATTER_FIELDS = REQUIRED_FRONTMATTER_FIELDS | OPTIONAL_FRONTMATTER_FIELDS

    def validate(self):
        """Validate agent markdown file"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.add_result(False, f"Failed to read file: {e}")
            return

        # Check for YAML frontmatter
        if not content.startswith("---\n"):
            self.add_result(False, "Agent file must start with YAML frontmatter (---)")
            return

        # Extract frontmatter
        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                self.add_result(False, "Missing closing frontmatter delimiter (---)")
                return

            frontmatter_str = parts[1].strip()
            markdown_content = parts[2].strip()

            # Parse YAML frontmatter
            try:
                frontmatter = self._parse_basic_yaml(frontmatter_str)
                if not isinstance(frontmatter, dict):
                    self.add_result(False, "Frontmatter must be a YAML object")
                    return
            except Exception as e:
                self.add_result(
                    False,
                    f"Invalid frontmatter: {e}. Install PyYAML for better validation",
                )
                return

            # Validate frontmatter fields
            self._validate_frontmatter(frontmatter)

            # Validate markdown content
            self._validate_markdown_content(markdown_content)

        except Exception as e:
            self.add_result(False, f"Error parsing agent file: {e}")

    def _parse_basic_yaml(self, yaml_str: str) -> Dict[str, Any]:
        """Very basic YAML parser for simple key: value pairs"""
        result = {}
        for line in yaml_str.split("\n"):
            line = line.strip()
            if line and ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # Handle boolean values
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                result[key] = value
        return result

    def _validate_frontmatter(self, frontmatter: Dict[str, Any]):
        """Validate YAML frontmatter"""
        # Check required fields
        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if field not in frontmatter:
                self.add_result(False, f"Missing required frontmatter field: {field}")
            elif not isinstance(frontmatter[field], str):
                self.add_result(False, f"Frontmatter field '{field}' must be a string")

        # Check for unknown fields
        for field in frontmatter:
            if field not in self.ALL_FRONTMATTER_FIELDS:
                self.add_result(
                    False, f"Unknown frontmatter field: {field}", None, None, "warning"
                )

        # Validate tools if present
        if "tools" in frontmatter:
            tools = frontmatter["tools"]
            if isinstance(tools, str):
                tool_list = [tool.strip() for tool in tools.split(",")]
                self._validate_tool_names(tool_list)
            elif isinstance(tools, list):
                self._validate_tool_names(tools)
            else:
                self.add_result(False, "tools must be a string or list")

        # Validate model if present
        if "model" in frontmatter:
            model = frontmatter["model"]
            if not isinstance(model, str):
                self.add_result(False, "model must be a string")
            else:
                valid_models = {"sonnet", "opus", "haiku"}
                if model.lower() not in valid_models:
                    self.add_result(
                        False,
                        f"Unknown model: {model}. Valid: {', '.join(valid_models)}",
                        None,
                        None,
                        "warning",
                    )

        # Validate description quality
        if "description" in frontmatter:
            desc = frontmatter["description"]
            if len(desc) < 10:
                self.add_result(
                    False,
                    "Description should be more descriptive (at least 10 characters)",
                    None,
                    None,
                    "warning",
                )

    def _validate_tool_names(self, tools: List[str]):
        """Validate tool names"""
        valid_tools = {
            "Read",
            "Write",
            "Edit",
            "MultiEdit",
            "Bash",
            "LS",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "Task",
            "SlashCommand",
        }

        for tool in tools:
            tool = tool.strip()
            if tool not in valid_tools:
                self.add_result(False, f"Unknown tool: {tool}", None, None, "warning")

    def _validate_markdown_content(self, content: str):
        """Validate markdown content"""
        if not content.strip():
            self.add_result(False, "Agent file cannot be empty after frontmatter")
            return

        lines = content.split("\n")

        # Check for main heading
        has_heading = any(line.strip().startswith("# ") for line in lines)
        if not has_heading:
            self.add_result(
                False, "Agent file should have a main heading", None, None, "warning"
            )

        # Check for expertise definition
        has_expertise = any("expert" in line.lower() for line in lines)
        if not has_expertise:
            self.add_result(
                False,
                "Consider defining the agent's expertise clearly",
                None,
                None,
                "info",
            )

        # Check for usage instructions
        has_usage = any(
            "when" in line.lower()
            and ("use" in line.lower() or "invoke" in line.lower())
            for line in lines
        )
        if not has_usage:
            self.add_result(
                False, "Consider specifying when to use this agent", None, None, "info"
            )


class PluginValidator:
    """Validator for entire plugin directories"""

    def __init__(self, plugin_path: str):
        self.plugin_path = Path(plugin_path)
        self.results: List[ValidationResult] = []

    def validate(self):
        """Validate entire plugin structure"""
        if not self.plugin_path.exists():
            self.results.append(
                ValidationResult(
                    False, f"Plugin directory does not exist: {self.plugin_path}"
                )
            )
            return

        if not self.plugin_path.is_dir():
            self.results.append(
                ValidationResult(
                    False, f"Plugin path is not a directory: {self.plugin_path}"
                )
            )
            return

        # Check for required plugin.json
        plugin_json = self.plugin_path / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            self.results.append(
                ValidationResult(False, "Missing .claude-plugin/plugin.json")
            )
        else:
            self._validate_plugin_json(plugin_json)

        # Validate components
        self._validate_component_directory("commands", CommandValidator)
        self._validate_component_directory("agents", AgentValidator)
        self._validate_component_directory("skills", self._validate_skill_directory)
        self._validate_component_directory("hooks", self._validate_hooks_directory)

    def _validate_plugin_json(self, plugin_json_path: Path):
        """Validate plugin.json file"""
        try:
            with open(plugin_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.results.append(
                ValidationResult(
                    False, f"Invalid JSON in plugin.json: {e.msg}", e.lineno, e.colno
                )
            )
            return
        except Exception as e:
            self.results.append(
                ValidationResult(False, f"Failed to read plugin.json: {e}")
            )
            return

        # Validate required fields
        required_fields = {"name", "version", "description", "author", "license"}
        for field in required_fields:
            if field not in data:
                self.results.append(
                    ValidationResult(
                        False, f"Missing required field in plugin.json: {field}"
                    )
                )
            elif field == "author":
                if not isinstance(data[field], dict):
                    self.results.append(
                        ValidationResult(
                            False, "Field 'author' in plugin.json must be an object"
                        )
                    )
                elif "name" not in data[field]:
                    self.results.append(
                        ValidationResult(
                            False, "Author object must have a 'name' field"
                        )
                    )
                elif not isinstance(data[field]["name"], str):
                    self.results.append(
                        ValidationResult(False, "Author 'name' field must be a string")
                    )
            elif not isinstance(data[field], str):
                self.results.append(
                    ValidationResult(
                        False, f"Field '{field}' in plugin.json must be a string"
                    )
                )

        # Validate version format
        if "version" in data:
            version = data["version"]
            if not re.match(r"^\d+\.\d+\.\d+", version):
                self.results.append(
                    ValidationResult(
                        False,
                        "Version should follow semantic versioning (x.y.z)",
                        None,
                        None,
                        "warning",
                    )
                )

    def _validate_component_directory(self, dir_name: str, validator_class):
        """Validate a component directory"""
        component_dir = self.plugin_path / dir_name
        if not component_dir.exists():
            return  # Optional directory

        if not component_dir.is_dir():
            self.results.append(
                ValidationResult(False, f"{dir_name} should be a directory")
            )
            return

        if dir_name == "skills":
            # Special handling for skills (subdirectories)
            for skill_dir in component_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        validator = SkillValidator(str(skill_md))
                        validator.validate()
                        self.results.extend(validator.results)
                    else:
                        self.results.append(
                            ValidationResult(
                                False,
                                f"Skill directory {skill_dir.name} missing SKILL.md",
                                None,
                                None,
                                "warning",
                            )
                        )
        elif dir_name == "hooks":
            # Special handling for hooks (JSON files)
            for hook_file in component_dir.glob("*.json"):
                validator = HooksValidator(str(hook_file))
                validator.validate()
                self.results.extend(validator.results)
        else:
            # Commands and agents (markdown files)
            for md_file in component_dir.glob("*.md"):
                validator = validator_class(str(md_file))
                validator.validate()
                self.results.extend(validator.results)

    def _validate_skill_directory(self, skill_dir: Path):
        """Validate a single skill directory"""
        if not skill_dir.is_dir():
            return

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            self.results.append(
                ValidationResult(False, f"Missing SKILL.md in {skill_dir.name}")
            )
            return

        validator = SkillValidator(str(skill_md))
        validator.validate()
        self.results.extend(validator.results)

    def _validate_hooks_directory(self, hooks_dir: Path):
        """Validate hooks directory"""
        if not hooks_dir.is_dir():
            return

        # Look for hooks.json or individual hook files
        hooks_json = hooks_dir / "hooks.json"
        if hooks_json.exists():
            validator = HooksValidator(str(hooks_json))
            validator.validate()
            self.results.extend(validator.results)

        # Also validate any other JSON files
        for json_file in hooks_dir.glob("*.json"):
            if json_file.name != "hooks.json":
                validator = HooksValidator(str(json_file))
                validator.validate()
                self.results.extend(validator.results)

    def print_results(self):
        """Print validation results"""
        if not self.results:
            print(
                f"{Colors.GREEN}✓{Colors.END} Plugin {self.plugin_path}: No issues found"
            )
            return

        print(
            f"\n{Colors.BOLD}Validation results for plugin {self.plugin_path}:{Colors.END}"
        )

        for result in self.results:
            print(f"  {result}")

        errors = sum(
            1 for r in self.results if not r.is_valid and r.severity == "error"
        )
        warnings = sum(
            1 for r in self.results if not r.is_valid and r.severity == "warning"
        )

        if errors > 0:
            print(f"\n{Colors.RED}✗{Colors.END} {errors} error(s) found")
        if warnings > 0:
            print(f"{Colors.YELLOW}⚠{Colors.END} {warnings} warning(s) found")
        if errors == 0 and warnings == 0:
            print(f"\n{Colors.GREEN}✓{Colors.END} All checks passed")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Claude Code components (hooks, skills, commands, agents)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a specific hooks.json file
  python validate_components.py --hooks /path/to/hooks.json
  
  # Validate a specific skill
  python validate_components.py --skill /path/to/skill
  
  # Validate a specific command
  python validate_components.py --command /path/to/command.md
  
  # Validate a specific agent
  python validate_components.py --agent /path/to/agent.md
  
  # Validate an entire plugin
  python validate_components.py --plugin /path/to/plugin
  
  # Validate all plugins in a directory
  python validate_components.py --all /path/to/plugins/dir
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hooks", help="Validate hooks.json file")
    group.add_argument("--skill", help="Validate skill directory (containing SKILL.md)")
    group.add_argument("--command", help="Validate command markdown file")
    group.add_argument("--agent", help="Validate agent markdown file")
    group.add_argument("--plugin", help="Validate entire plugin directory")
    group.add_argument("--all", help="Validate all plugins in directory")

    parser.add_argument(
        "--quiet", action="store_true", help="Only show errors and warnings"
    )
    parser.add_argument(
        "--version", action="version", version="Claude Code Component Validator 1.0.0"
    )

    args = parser.parse_args()

    success = True

    try:
        if args.hooks:
            validator = HooksValidator(args.hooks)
            validator.validate()
            validator.print_results()
            success = not validator.has_errors()

        elif args.skill:
            skill_path = Path(args.skill)
            if skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
            else:
                skill_md = skill_path

            validator = SkillValidator(str(skill_md))
            validator.validate()
            validator.print_results()
            success = not validator.has_errors()

        elif args.command:
            validator = CommandValidator(args.command)
            validator.validate()
            validator.print_results()
            success = not validator.has_errors()

        elif args.agent:
            validator = AgentValidator(args.agent)
            validator.validate()
            validator.print_results()
            success = not validator.has_errors()

        elif args.plugin:
            validator = PluginValidator(args.plugin)
            validator.validate()
            validator.print_results()
            success = not any(
                not r.is_valid and r.severity == "error" for r in validator.results
            )

        elif args.all:
            all_path = Path(args.all)
            if not all_path.is_dir():
                print(f"{Colors.RED}Error: {args.all} is not a directory{Colors.END}")
                sys.exit(1)

            plugin_dirs = [
                d
                for d in all_path.iterdir()
                if d.is_dir() and (d / ".claude-plugin").exists()
            ]

            if not plugin_dirs:
                print(f"{Colors.YELLOW}No plugins found in {args.all}{Colors.END}")
                sys.exit(0)

            all_success = True
            for plugin_dir in plugin_dirs:
                validator = PluginValidator(str(plugin_dir))
                validator.validate()
                validator.print_results()
                if any(
                    not r.is_valid and r.severity == "error" for r in validator.results
                ):
                    all_success = False
                print()  # Add spacing between plugins

            success = all_success

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation interrupted{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
