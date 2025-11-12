#!/usr/bin/env python3
"""
Migrate urfave/cli v2 code to v3.
This script helps identify and apply the necessary changes for v2 to v3 migration.
"""

import re
import sys
from pathlib import Path

def migrate_imports(content: str) -> tuple[str, list[str]]:
    """Migrate import statements from v2 to v3."""
    changes = []

    # Replace v2 imports with v3
    if 'github.com/urfave/cli/v2' in content:
        content = content.replace('github.com/urfave/cli/v2', 'github.com/urfave/cli/v3')
        changes.append("Updated import from v2 to v3")

    if 'github.com/urfave/cli' in content and 'v3' not in content:
        content = content.replace('github.com/urfave/cli', 'github.com/urfave/cli/v3')
        changes.append("Updated import to v3")

    return content, changes

def migrate_app_creation(content: str) -> tuple[str, list[str]]:
    """Migrate from cli.App to cli.Command."""
    changes = []

    # Replace &cli.App{} with &cli.Command{}
    content = re.sub(r'&cli\.App\{', '&cli.Command{', content)

    # Replace cli.NewApp() with &cli.Command{}
    content = re.sub(r'cli\.NewApp\(\)', '&cli.Command{}', content)

    # Replace app.Run with cmd.Run and add context
    if 'app.Run(os.Args)' in content:
        content = content.replace('app.Run(os.Args)', 'cmd.Run(context.Background(), os.Args)')
        changes.append("Changed app.Run to cmd.Run with context")
    elif 'c.App.Run' in content:
        content = re.sub(r'c\.App\.Run\(([^)]+)\)', r'cmd.Run(context.Background(), \1)', content)
        changes.append("Changed App.Run to cmd.Run with context")

    return content, changes

def migrate_action_functions(content: str) -> tuple[str, list[str]]:
    """Migrate action functions to use context.Context."""
    changes = []

    # Find action function signatures and update them
    # Pattern: func(*cli.Context) -> func(context.Context, *cli.Command)
    action_pattern = r'func\s+\w+\(\s*\*cli\.Context\s*\)\s*error\s*\{'

    def replace_action(match):
        return 'func(context.Context, *cli.Command) error {'

    new_content = re.sub(action_pattern, replace_action, content)
    if new_content != content:
        changes.append("Updated action function signature to include context")
        content = new_content

    # Update action calls in commands
    content = re.sub(r'Action:\s+func\(\s*c\s*\*cli\.Context\s*\)',
                     'Action: func(ctx context.Context, cmd *cli.Command)', content)

    # Update function body references from c.Context to cmd
    content = re.sub(r'\bc\.(String|Bool|Int|StringSlice|Args|NArg|Set|IsSet)', r'cmd.\1', content)
    content = re.sub(r'\bc\.(FlagNames|GlobalFlagNames|Parent|App)', r'cmd.\1', content)

    return content, changes

def migrate_flag_actions(content: str) -> tuple[str, list[str]]:
    """Migrate flag action function signatures."""
    changes = []

    # Update flag action signature
    flag_action_pattern = r'Action:\s+func\(\s*c\s*\*cli\.Context\s*,\s*(\w+)\s+(\w+)\)\s*error\s*\{'

    def replace_flag_action(match):
        param_type = match.group(1)
        param_name = match.group(2)
        return f'Action: func(ctx context.Context, cmd *cli.Command, {param_name} {param_type}) error {{'

    new_content = re.sub(flag_action_pattern, replace_flag_action, content)
    if new_content != content:
        changes.append("Updated flag action function signature")
        content = new_content

    return content, changes

def migrate_before_after_hooks(content: str) -> tuple[str, list[str]]:
    """Migrate Before and After function signatures."""
    changes = []

    # Update Before function signature
    before_pattern = r'Before:\s+func\(\s*c\s*\*cli\.Context\s*\)\s*error\s*\{'
    new_content = re.sub(before_pattern, 'Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {', content)
    if new_content != content:
        changes.append("Updated Before function signature")
        content = new_content

    # Update After function signature (should be the same in v2 and v3)
    # No changes needed for After function

    # Update function calls in Before/After
    content = re.sub(r'c\.App\.Writer', 'cmd.Root().Writer', content)

    return content, changes

def add_context_import(content: str) -> tuple[str, list[str]]:
    """Add context import if not present."""
    changes = []

    if 'import (' in content and '"context"' not in content:
        # Add context import
        import_start = content.find('import (')
        import_end = content.find(')', import_start)

        if import_start != -1 and import_end != -1:
            import_section = content[import_start:import_end + 1]
            if '"context"' not in import_section:
                new_import_section = import_section.replace('import (', 'import (\n\t"context"')
                content = content[:import_start] + new_import_section + content[import_end + 1:]
                changes.append("Added context import")

    return content, changes

def migrate_file(file_path: str, backup: bool = True) -> bool:
    """Migrate a single Go file from v2 to v3."""
    try:
        with open(file_path, 'r') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

    content = original_content
    all_changes = []

    # Apply migration steps
    content, changes = migrate_imports(content)
    all_changes.extend(changes)

    content, changes = add_context_import(content)
    all_changes.extend(changes)

    content, changes = migrate_app_creation(content)
    all_changes.extend(changes)

    content, changes = migrate_action_functions(content)
    all_changes.extend(changes)

    content, changes = migrate_flag_actions(content)
    all_changes.extend(changes)

    content, changes = migrate_before_after_hooks(content)
    all_changes.extend(changes)

    # Check if any changes were made
    if content == original_content:
        print(f"No changes needed for {file_path}")
        return True

    # Create backup if requested
    if backup:
        backup_path = f"{file_path}.backup"
        try:
            with open(backup_path, 'w') as f:
                f.write(original_content)
            print(f"Created backup: {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")

    # Write migrated content
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Migrated {file_path}")
        for change in all_changes:
            print(f"  - {change}")
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrate urfave/cli v2 code to v3")
    parser.add_argument("files", nargs="+", help="Go files to migrate")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backup files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying files")

    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN - No files will be modified")
        print("=" * 50)

    success_count = 0
    for file_path in args.files:
        if not file_path.endswith('.go'):
            print(f"Skipping non-Go file: {file_path}")
            continue

        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            continue

        if args.dry_run:
            print(f"Would migrate: {file_path}")
            success_count += 1
        else:
            if migrate_file(file_path, backup=not args.no_backup):
                success_count += 1

    print("=" * 50)
    if args.dry_run:
        print(f"Would process {success_count} files")
    else:
        print(f"Successfully migrated {success_count}/{len(args.files)} files")

    if not args.dry_run and success_count > 0:
        print("\nNext steps:")
        print("1. Run: go get github.com/urfave/cli/v3")
        print("2. Test your application: go run .")
        print("3. Check for any remaining compilation errors")

if __name__ == "__main__":
    main()