#!/usr/bin/env python3
"""
Boilr Template Validation Script
Validates boilr templates for correct structure, syntax, and common issues.
"""

import os
import json
import sys
import argparse
from pathlib import Path
import re

class TemplateValidator:
    def __init__(self, template_dir):
        self.template_dir = Path(template_dir)
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self):
        """Run all validation checks."""
        print(f"🔍 Validating template: {self.template_dir}")
        print("=" * 50)

        self.validate_directory_structure()
        self.validate_project_json()
        self.validate_template_files()
        self.validate_template_syntax()
        self.validate_boilerplate_files()
        self.validate_best_practices()

        self.print_results()
        return len(self.errors) == 0

    def validate_directory_structure(self):
        """Validate required directory structure."""
        print("\n📁 Checking directory structure...")

        # Check if template directory exists
        template_path = self.template_dir / "template"
        if not template_path.exists():
            self.errors.append("Missing 'template' directory")
        else:
            self.info.append("✅ Template directory exists")

        # Check boilerplate directory (optional)
        boilerplate_path = self.template_dir / "boilerplate"
        if boilerplate_path.exists():
            self.info.append("✅ Boilerplate directory exists")

    def validate_project_json(self):
        """Validate project.json file."""
        print("\n📄 Checking project.json...")

        project_json_path = self.template_dir / "project.json"
        if not project_json_path.exists():
            self.warnings.append("No project.json found - template will work but without prompts")
            return

        try:
            with open(project_json_path, 'r') as f:
                data = json.load(f)

            # Validate structure
            if "prompts" not in data:
                self.errors.append("project.json must contain 'prompts' array")
                return

            if not isinstance(data["prompts"], list):
                self.errors.append("'prompts' must be an array")
                return

            # Validate each prompt
            for i, prompt in enumerate(data["prompts"]):
                if not isinstance(prompt, dict):
                    self.errors.append(f"Prompt {i} must be an object")
                    continue

                # Required fields
                if "name" not in prompt:
                    self.errors.append(f"Prompt {i} missing required 'name' field")
                elif not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', prompt["name"]):
                    self.errors.append(f"Prompt {i} name '{prompt['name']}' is not a valid Go identifier")

                if "message" not in prompt:
                    self.errors.append(f"Prompt {i} missing required 'message' field")

                # Optional field validation
                if "default" in prompt and not isinstance(prompt["default"], str):
                    self.warnings.append(f"Prompt {i} default value should be a string")

            self.info.append(f"✅ project.json valid with {len(data['prompts'])} prompt(s)")

        except json.JSONDecodeError as e:
            self.errors.append(f"project.json contains invalid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Error reading project.json: {e}")

    def validate_template_files(self):
        """Validate files in template directory."""
        print("\n📝 Checking template files...")

        template_path = self.template_dir / "template"
        if not template_path.exists():
            return

        template_files = list(template_path.rglob("*"))
        template_files = [f for f in template_files if f.is_file()]

        if not template_files:
            self.warnings.append("No files found in template directory")
            return

        for file_path in template_files:
            relative_path = file_path.relative_to(template_path)

            # Check for template variables in filename
            if self.has_template_variables(str(relative_path)):
                self.info.append(f"📄 Template variables found in filename: {relative_path}")

            # Check file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for template variables
                if self.has_template_variables(content):
                    self.info.append(f"📄 Template variables found in: {relative_path}")

                # Check for common Go files
                if file_path.name.endswith('.go'):
                    self.validate_go_file(file_path, content)

                if file_path.name == 'go.mod':
                    self.validate_go_mod(file_path, content)

            except UnicodeDecodeError:
                self.warnings.append(f"Binary file detected: {relative_path}")
            except Exception as e:
                self.errors.append(f"Error reading {relative_path}: {e}")

        self.info.append(f"✅ Found {len(template_files)} template file(s)")

    def validate_template_syntax(self):
        """Validate Go template syntax."""
        print("\n🔧 Checking template syntax...")

        template_path = self.template_dir / "template"
        if not template_path.exists():
            return

        # Basic template syntax validation
        for file_path in template_path.rglob("*"):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for unclosed template actions
                open_count = content.count('{{')
                close_count = content.count('}}')

                if open_count != close_count:
                    self.errors.append(f"Unclosed template actions in {file_path.relative_to(template_path)}: {open_count} opens, {close_count} closes")

                # Check for common template syntax issues
                if '{{.' in content and not re.search(r'\{\{\.\w+\}}', content):
                    self.warnings.append(f"Possible invalid template variable syntax in {file_path.relative_to(template_path)}")

            except UnicodeDecodeError:
                continue  # Skip binary files

        self.info.append("✅ Template syntax validation completed")

    def validate_go_file(self, file_path, content):
        """Validate Go file template."""
        # Check for common Go template patterns
        if 'package main' in content and '{{.ModuleName}}' not in content:
            self.warnings.append(f"Go file {file_path.name} has 'package main' but no module template variable")

        # Check for import statements that might need template variables
        if 'import (' in content and '{{.ModuleName}}' not in content:
            self.info.append(f"Go file {file_path.name} has imports but no module template variable")

    def validate_go_mod(self, file_path, content):
        """Validate go.mod template."""
        if 'module ' in content and '{{.ModuleName}}' not in content:
            self.warnings.append("go.mod file has module declaration but no {{.ModuleName}} template variable")

    def validate_boilerplate_files(self):
        """Validate files in boilerplate directory."""
        print("\n📦 Checking boilerplate files...")

        boilerplate_path = self.template_dir / "boilerplate"
        if not boilerplate_path.exists():
            return

        boilerplate_files = list(boilerplate_path.rglob("*"))
        boilerplate_files = [f for f in boilerplate_files if f.is_file()]

        for file_path in boilerplate_files:
            relative_path = file_path.relative_to(boilerplate_path)

            # Boilerplate files should not contain template variables
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if self.has_template_variables(content):
                    self.warnings.append(f"Boilerplate file contains template variables: {relative_path}")

            except UnicodeDecodeError:
                self.info.append(f"📦 Binary boilerplate file: {relative_path}")

        self.info.append(f"✅ Found {len(boilerplate_files)} boilerplate file(s)")

    def validate_best_practices(self):
        """Check for best practices."""
        print("\n⭐ Checking best practices...")

        # Check for README
        template_path = self.template_dir / "template"
        if template_path.exists():
            readme_files = list(template_path.rglob("README*"))
            if not readme_files:
                self.warnings.append("No README.md template found")
            else:
                self.info.append("✅ README template found")

        # Check for .gitignore
        gitignore_files = list(self.template_dir.rglob(".gitignore"))
        if not gitignore_files:
            self.warnings.append("No .gitignore file found")
        else:
            self.info.append("✅ .gitignore file found")

        # Check for go.mod in Go templates
        go_mod_files = list(template_path.rglob("go.mod")) if template_path.exists() else []
        if go_mod_files:
            self.info.append("✅ go.mod template found")
        else:
            go_files = list(template_path.rglob("*.go")) if template_path.exists() else []
            if go_files:
                self.warnings.append("Go files found but no go.mod template")

    def has_template_variables(self, text):
        """Check if text contains Go template variables."""
        return '{{' in text and '}}' in text

    def print_results(self):
        """Print validation results."""
        print("\n" + "=" * 50)
        print("📊 VALIDATION RESULTS")
        print("=" * 50)

        if self.info:
            print(f"\nℹ️  INFORMATION ({len(self.info)}):")
            for item in self.info:
                print(f"   {item}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
        else:
            print("\n✅ No errors found!")

        print(f"\n📈 Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")

def main():
    parser = argparse.ArgumentParser(description="Validate boilr templates")
    parser.add_argument("template_dir", help="Path to the template directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    if not os.path.exists(args.template_dir):
        print(f"❌ Template directory does not exist: {args.template_dir}")
        sys.exit(1)

    validator = TemplateValidator(args.template_dir)
    is_valid = validator.validate()

    if args.strict and validator.warnings:
        print(f"\n❌ Validation failed due to warnings in strict mode")
        sys.exit(1)

    if not is_valid:
        print(f"\n❌ Template validation failed")
        sys.exit(1)
    else:
        print(f"\n✅ Template validation passed!")

if __name__ == "__main__":
    main()