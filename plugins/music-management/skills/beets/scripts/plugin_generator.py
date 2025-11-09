#!/usr/bin/env python3
"""
Beets Plugin Generator

This script generates beets plugin templates, scaffolds event listeners, and provides
tools for developing custom beets plugins.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

# Plugin templates
PLUGIN_TEMPLATES = {
    'basic': '''"""
Basic Beets Plugin Template

A minimal plugin template that demonstrates the basic structure of a beets plugin.
"""

from beets import config
from beets.plugins import BeetsPlugin


class {PluginName}(BeetsPlugin):
    """
    {PluginDescription}
    """

    def __init__(self):
        super().__init__()
        self.config.add({})

        # Register template functions if needed
        # self.template_funcs["{plugin_name_lower}_func"] = self._template_func

    # def _template_func(self, text):
    #     """Example template function."""
    #     return text.upper()
''',

    'metadata': '''"""
Metadata Beets Plugin Template

A plugin that modifies or processes metadata during import or modification.
"""

from beets import config
from beets.plugins import BeetsPlugin
from beets import importer
from beets.library import Item


class {PluginName}(BeetsPlugin):
    """
    {PluginDescription}
    """

    def __init__(self):
        super().__init__()
        self.config.add({{
            'auto_process': True,
            'field_mappings': {{}}
        }})

        # Register listeners
        self.register_listener('import_task_created', self.task_created)
        self.register_listener('import_task_apply', self.task_apply)

    def task_created(self, task, session):
        """Called when an import task is created."""
        if self.config['auto_process']:
            self.process_metadata(task.items)

    def task_apply(self, task, session):
        """Called when metadata is applied to items."""
        pass

    def process_metadata(self, items):
        """Process metadata for a list of items."""
        for item in items:
            self.process_item(item)

    def process_item(self, item: Item):
        """Process metadata for a single item."""
        # Add custom metadata processing logic here
        # Example: item['custom_field'] = calculate_value(item)
        pass
''',

    'command': '''"""
Command Beets Plugin Template

A plugin that adds custom commands to beets.
"""

from beets import config
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs, print_, input_, configure


class {PluginName}(BeetsPlugin):
    """
    {PluginDescription}
    """

    def __init__(self):
        super().__init__()
        self.config.add({{
            'default_option': 'value'
        }})

        # Register commands
        {PluginName}Command = Subcommand('{plugin_name_lower}',
                                        help='{PluginHelpText}')
        {PluginName}Command.parser.add_option('-d', '--debug',
                                            action='store_true',
                                            help='Enable debug output')
        {PluginName}Command.func = self.{plugin_name_lower}_command
        self._register_command_function({PluginName}Command)

    def {plugin_name_lower}_command(self, lib, opts, args):
        """Custom command implementation."""
        self._log.info('Running {plugin_name_lower} command')

        # Get arguments
        query = decargs(args)

        # Process command
        if opts.debug:
            self._log.debug('Debug mode enabled')

        # Example: list matching items
        items = lib.items(query)
        for item in items:
            print_(f"{{item.artist}} - {{item.title}}")

        print_(f"Processed {{len(items)}} items")
''',

    'template_function': '''"""
Template Function Beets Plugin Template

A plugin that provides custom template functions for path formatting.
"""

from beets import config
from beets.plugins import BeetsPlugin


class {PluginName}(BeetsPlugin):
    """
    {PluginDescription}
    """

    def __init__(self):
        super().__init__()
        self.config.add({{
            'default_format': 'standard'
        }})

        # Register template functions
        self.template_funcs = {{
            '{plugin_name_lower}_format': self.format_text,
            '{plugin_name_lower}_capitalize': self.capitalize_words,
            '{plugin_name_lower}_clean': self.clean_text
        }}

    def format_text(self, text, format_type=None):
        """Format text according to specified type."""
        if not text:
            return ""

        format_type = format_type or self.config['default_format'].get(str)

        if format_type == 'upper':
            return text.upper()
        elif format_type == 'lower':
            return text.lower()
        elif format_type == 'title':
            return text.title()
        else:
            return text

    def capitalize_words(self, text):
        """Capitalize the first letter of each word."""
        if not text:
            return ""
        return ' '.join(word.capitalize() for word in text.split())

    def clean_text(self, text):
        """Clean text by removing extra whitespace and special characters."""
        if not text:
            return ""

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Remove or replace special characters as needed
        # text = text.replace('/', '-')

        return text
''',

    'event_listener': '''"""
Event Listener Beets Plugin Template

A plugin that responds to various beets events.
"""

from beets import config
from beets.plugins import BeetsPlugin
from beets.importer import ImportTask
from beets.library import Item, Album


class {PluginName}(BeetsPlugin):
    """
    {PluginDescription}
    """

    def __init__(self):
        super().__init__()
        self.config.add({{
            'log_events': True,
            'process_items': True
        }})

        # Register event listeners
        self.register_listener('pluginload', self.plugin_loaded)
        self.register_listener('item_imported', self.item_imported)
        self.register_listener('album_imported', self.album_imported)
        self.register_listener('database_change', self.database_changed)
        self.register_listener('cli_exit', self.cli_exit)

    def plugin_loaded(self):
        """Called when the plugin is loaded."""
        self._log.info('{PluginName} plugin loaded')

    def item_imported(self, lib, item: Item):
        """Called when an item is imported."""
        if self.config['log_events'].get(bool):
            self._log.info(f'Item imported: {{item.artist}} - {{item.title}}')

        if self.config['process_items'].get(bool):
            self.process_imported_item(item)

    def album_imported(self, lib, album: Album):
        """Called when an album is imported."""
        if self.config['log_events'].get(bool):
            self._log.info(f'Album imported: {{album.albumartist}} - {{album.album}}')

        self.process_imported_album(album)

    def database_changed(self, lib):
        """Called when the database changes."""
        if self.config['log_events'].get(bool):
            self._log.debug('Database changed')

    def cli_exit(self):
        """Called when the CLI exits."""
        self._log.info('{PluginName} plugin shutting down')

    def process_imported_item(self, item: Item):
        """Process a newly imported item."""
        # Add custom processing logic here
        # Example: add custom tags, update fields, etc.
        pass

    def process_imported_album(self, album: Album):
        """Process a newly imported album."""
        # Add custom album processing logic here
        # Example: calculate album-level metadata
        pass
'''
}

# Event listeners
EVENT_LISTENERS = {
    'import_task_created': '''    def import_task_created(self, task: ImportTask, session):
        """Called when an import task is created."""
        self._log.debug(f'Import task created: {{task.topath()}}')
        # Add custom logic here
''',
    'item_imported': '''    def item_imported(self, lib, item: Item):
        """Called when an item is imported."""
        self._log.debug(f'Item imported: {{item.artist}} - {{item.title}}')
        # Add custom logic here
''',
    'album_imported': '''    def album_imported(self, lib, album: Album):
        """Called when an album is imported."""
        self._log.debug(f'Album imported: {{album.albumartist}} - {{album.album}}')
        # Add custom logic here
''',
    'write': '''    def write(self, item: Item, path: str):
        """Called before writing metadata to a file."""
        self._log.debug(f'Writing metadata for: {{item.title}}')
        # Add custom logic here
''',
    'database_change': '''    def database_change(self, lib):
        """Called when the database changes."""
        self._log.debug('Database changed')
        # Add custom logic here
'''
}

class PluginGenerator:
    def __init__(self):
        self.plugins_dir = Path.home() / '.config' / 'beets' / 'plugins'
        self.templates_dir = Path(__file__).parent.parent / 'assets' / 'plugin_templates'

    def create_plugin(self, name: str, plugin_type: str, description: str = "") -> bool:
        """Create a new plugin from template."""
        if plugin_type not in PLUGIN_TEMPLATES:
            print(f"❌ Unknown plugin type: {plugin_type}")
            print(f"Available types: {', '.join(PLUGIN_TEMPLATES.keys())}")
            return False

        # Prepare template variables
        plugin_name_camel = ''.join(word.capitalize() for word in name.split('_'))
        plugin_name_lower = name.lower()

        if not description:
            description = f"A {plugin_type} beets plugin for {name}"

        # Generate plugin content
        template_content = PLUGIN_TEMPLATES[plugin_type].format(
            PluginName=plugin_name_camel,
            plugin_name_lower=plugin_name_lower,
            PluginDescription=description,
            PluginHelpText=f"Custom {name} functionality"
        )

        # Create plugin directory
        plugin_dir = self.plugins_dir / name
        try:
            plugin_dir.mkdir(parents=True, exist_ok=True)

            # Create main plugin file
            plugin_file = plugin_dir / f"{name}.py"
            with open(plugin_file, 'w') as f:
                f.write(template_content)

            # Create __init__.py for package-style plugins
            init_file = plugin_dir / "__init__.py"
            with open(init_file, 'w') as f:
                f.write(f'from .{name} import {plugin_name_camel}\n')

            print(f"✅ Plugin created: {plugin_dir}")
            print(f"   Main file: {plugin_file}")

            # Show next steps
            self.show_next_steps(name, plugin_type)

            return True

        except Exception as e:
            print(f"❌ Error creating plugin: {e}")
            return False

    def add_event_listener(self, plugin_name: str, event: str) -> bool:
        """Add an event listener to an existing plugin."""
        if event not in EVENT_LISTENERS:
            print(f"❌ Unknown event: {event}")
            print(f"Available events: {', '.join(EVENT_LISTENERS.keys())}")
            return False

        plugin_file = self.plugins_dir / plugin_name / f"{plugin_name}.py"
        if not plugin_file.exists():
            print(f"❌ Plugin not found: {plugin_name}")
            return False

        try:
            # Read existing plugin content
            with open(plugin_file, 'r') as f:
                content = f.read()

            # Check if event listener already exists
            if f"def {event}" in content:
                print(f"⚠️  Event listener '{event}' already exists in plugin")
                return False

            # Add event listener
            event_code = EVENT_LISTENERS[event]

            # Add to __init__ method
            if 'def __init__(self):' in content:
                init_pattern = r'(def __init__\(self\):.*?)(\n\n|\ndef|\Z)'
                import re
                match = re.search(init_pattern, content, re.DOTALL)
                if match:
                    init_content = match.group(1)
                    # Find where to add the register_listener call
                    lines = init_content.split('\n')
                    insert_pos = len(lines) - 1  # Before the last line (super().__init__())

                    # Add register_listener call
                    register_line = f"        self.register_listener('{event}', self.{event})"
                    lines.insert(insert_pos, register_line)

                    # Reconstruct init method
                    new_init = '\n'.join(lines)
                    content = content.replace(init_content, new_init)

            # Add the event method at the end
            content += '\n\n' + event_code

            # Write back to file
            with open(plugin_file, 'w') as f:
                f.write(content)

            print(f"✅ Added event listener '{event}' to plugin '{plugin_name}'")
            return True

        except Exception as e:
            print(f"❌ Error adding event listener: {e}")
            return False

    def create_plugin_config(self, plugin_name: str, config_data: Dict[str, Any]) -> bool:
        """Create or update plugin configuration."""
        config_file = self.plugins_dir / plugin_name / "config.yaml"

        try:
            import yaml
            with open(config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)

            print(f"✅ Plugin configuration created: {config_file}")
            return True

        except ImportError:
            # Fallback to JSON if yaml not available
            json_file = config_file.with_suffix('.json')
            with open(json_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            print(f"✅ Plugin configuration created: {json_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating configuration: {e}")
            return False

    def list_plugins(self) -> None:
        """List existing plugins."""
        if not self.plugins_dir.exists():
            print("No plugins directory found")
            return

        plugins = [d for d in self.plugins_dir.iterdir() if d.is_dir()]

        if not plugins:
            print("No plugins found")
            return

        print("📦 Existing plugins:")
        for plugin_dir in sorted(plugins):
            main_file = plugin_dir / f"{plugin_dir.name}.py"
            if main_file.exists():
                print(f"  ✅ {plugin_dir.name}")
            else:
                print(f"  ❌ {plugin_dir.name} (incomplete)")

    def validate_plugin(self, plugin_name: str) -> bool:
        """Validate a plugin structure and syntax."""
        plugin_dir = self.plugins_dir / plugin_name

        if not plugin_dir.exists():
            print(f"❌ Plugin directory not found: {plugin_name}")
            return False

        # Check main plugin file
        main_file = plugin_dir / f"{plugin_name}.py"
        if not main_file.exists():
            print(f"❌ Main plugin file not found: {main_file}")
            return False

        # Check syntax
        try:
            import ast
            with open(main_file, 'r') as f:
                content = f.read()

            ast.parse(content)
            print(f"✅ Plugin syntax is valid: {plugin_name}")

            # Check for required elements
            if 'class ' in content and 'BeetsPlugin' in content:
                print(f"✅ Plugin class found")
            else:
                print(f"⚠️  Warning: No plugin class found")

            return True

        except SyntaxError as e:
            print(f"❌ Syntax error in plugin: {e}")
            return False
        except Exception as e:
            print(f"❌ Error validating plugin: {e}")
            return False

    def show_next_steps(self, plugin_name: str, plugin_type: str) -> None:
        """Show next steps for plugin development."""
        print(f"\n🚀 Next steps for '{plugin_name}' plugin:")
        print("=" * 40)

        print(f"1. Add plugin to beets configuration:")
        print(f"   plugins: {plugin_name}")

        print(f"\n2. Edit the plugin file:")
        plugin_file = self.plugins_dir / plugin_name / f"{plugin_name}.py"
        print(f"   {plugin_file}")

        print(f"\n3. Test the plugin:")
        print(f"   beet version  # Should load without errors")

        if plugin_type == 'command':
            print(f"\n4. Test the custom command:")
            print(f"   beet {plugin_name} --help")
        elif plugin_type == 'template_function':
            print(f"\n4. Test template functions:")
            print(f"   beet ls -f '%{{{plugin_name}_format{{artist}}}}'")

    def interactive_plugin_creation(self) -> None:
        """Interactive plugin creation wizard."""
        print("🧙‍♂️ Beets Plugin Creation Wizard")
        print("=" * 40)

        # Get plugin name
        while True:
            name = input("Enter plugin name (snake_case): ").strip()
            if not name:
                print("Plugin name is required")
                continue

            # Validate name format
            if not re.match(r'^[a-z][a-z0-9_]*$', name):
                print("Plugin name must be snake_case (lowercase with underscores)")
                continue

            break

        # Get plugin type
        print(f"\nAvailable plugin types:")
        for i, ptype in enumerate(PLUGIN_TEMPLATES.keys(), 1):
            print(f"{i}. {ptype}")

        while True:
            try:
                choice = input(f"Select plugin type (1-{len(PLUGIN_TEMPLATES)}): ").strip()
                type_idx = int(choice) - 1
                plugin_type = list(PLUGIN_TEMPLATES.keys())[type_idx]
                break
            except (ValueError, IndexError):
                print("Invalid choice")

        # Get description
        description = input("Enter plugin description (optional): ").strip()

        # Create plugin
        success = self.create_plugin(name, plugin_type, description)

        if success:
            # Ask about event listeners
            add_events = input("\nAdd event listeners? (y/N): ").strip().lower() == 'y'
            if add_events:
                print(f"\nAvailable events:")
                for i, event in enumerate(EVENT_LISTENERS.keys(), 1):
                    print(f"{i}. {event}")

                while True:
                    try:
                        choice = input(f"Select event (1-{len(EVENT_LISTENERS)}, or enter to finish): ").strip()
                        if not choice:
                            break

                        event_idx = int(choice) - 1
                        event_name = list(EVENT_LISTENERS.keys())[event_idx]
                        self.add_event_listener(name, event_name)
                    except (ValueError, IndexError):
                        print("Invalid choice")

            # Ask about configuration
            add_config = input("\nCreate plugin configuration file? (y/N): ").strip().lower() == 'y'
            if add_config:
                config_data = {
                    'enabled': True,
                    'options': {
                        'example_option': 'example_value'
                    }
                }
                self.create_plugin_config(name, config_data)

def main():
    parser = argparse.ArgumentParser(description='Beets plugin generator')
    parser.add_argument('--name', help='Plugin name (snake_case)')
    parser.add_argument('--type', choices=list(PLUGIN_TEMPLATES.keys()),
                       help='Plugin type')
    parser.add_argument('--description', help='Plugin description')
    parser.add_argument('--list', action='store_true',
                       help='List existing plugins')
    parser.add_argument('--validate', help='Validate a plugin')
    parser.add_argument('--add-event', help='Add event listener to existing plugin')
    parser.add_argument('--event', choices=list(EVENT_LISTENERS.keys()),
                       help='Event type to add')
    parser.add_argument('--create-config', help='Create configuration for plugin')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive plugin creation wizard')

    args = parser.parse_args()

    generator = PluginGenerator()

    if args.list:
        generator.list_plugins()
        return

    if args.validate:
        success = generator.validate_plugin(args.validate)
        sys.exit(0 if success else 1)

    if args.add_event and args.event:
        success = generator.add_event_listener(args.add_event, args.event)
        sys.exit(0 if success else 1)

    if args.interactive:
        generator.interactive_plugin_creation()
        return

    if args.name and args.type:
        success = generator.create_plugin(args.name, args.type, args.description or "")
        sys.exit(0 if success else 1)
    else:
        print("Please specify --name and --type, or use --interactive mode")
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()