#!/usr/bin/env python3
"""
Beets Setup and Configuration Generator

This script helps generate optimized beets configurations for different use cases,
validate existing configurations, and set up directory structures for music libraries.
"""

import argparse
import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Configuration templates
CONFIG_TEMPLATES = {
    'basic': {
        'directory': '~/Music',
        'library': '~/.config/beets/library.db',
        'plugins': ['fetchart', 'lyrics', 'lastgenre'],
        'import': {
            'copy': True,
            'write': True,
            'autotag': True,
            'quiet': False
        },
        'paths': {
            'default': '$albumartist/$year - $album%aunique{}/$track - $title',
            'singleton': 'Singletons/$artist - $title',
            'comp': 'Compilations/$year - $album%aunique{}/$track - $title'
        }
    },
    'audiophile': {
        'directory': '~/Music',
        'library': '~/.config/beets/library.db',
        'plugins': ['fetchart', 'lyrics', 'lastgenre', 'embedart', 'badfiles', 'replaygain'],
        'import': {
            'copy': True,
            'write': True,
            'autotag': True,
            'quiet': False,
            'detail': True
        },
        'paths': {
            'default': '$albumartist/$year - $album [$format] [$bitrate]/$track - $title',
            'singleton': 'Singletons/$artist - $title [$format]',
            'comp': 'Compilations/$year - $album [$format]/$track - $title'
        },
        'replaygain': {
            'backend': 'bs1770gain',
            'targetlevel': 89,
            'overwrite': True
        },
        'badfiles': {
            'check_on_import': True
        }
    },
    'dj': {
        'directory': '~/DJ Music',
        'library': '~/.config/beets/dj_library.db',
        'plugins': ['fetchart', 'lyrics', 'lastgenre', 'bpm', 'key', 'beatport'],
        'import': {
            'copy': True,
            'write': True,
            'autotag': True,
            'quiet': False
        },
        'paths': {
            'default': '$genre/$albumartist/$album/$track - $artist - $title',
            'singleton': '$genre/$artist - $title'
        },
        'album_fields': {
            'bpm': 'for item in items: item.get("bpm", 0)',
            'key': 'for item in items: item.get("key", "")'
        }
    },
    'advanced': {
        'directory': '~/Music',
        'library': '~/.config/beets/library.db',
        'plugins': [
            'fetchart', 'lyrics', 'lastgenre', 'embedart', 'badfiles', 'replaygain',
            'scrub', 'mbsync', 'edit', 'ftintitle', 'the', 'chroma', 'convert'
        ],
        'import': {
            'copy': True,
            'write': True,
            'autotag': True,
            'quiet': False,
            'detail': True,
            'log': '~/.config/beets/import.log'
        },
        'paths': {
            'default': '$albumartist/$year - $album%aunique{}/$discnumber - $tracknumber - $title',
            'singleton': 'Singletons/$artist/$album - $title',
            'comp': 'Compilations/$year - $album%aunique{}/$track - $title'
        },
        'fetchart': {
            'auto': True,
            'minwidth': 500,
            'maxwidth': 1200,
            'sources': ['filesystem', 'amazon', 'albumart', 'google', 'fanarttv']
        },
        'lyrics': {
            'auto': True,
            'sources': ['google', 'lyricwikia', 'musixmatch']
        },
        'lastgenre': {
            'auto': True,
            'source': 'album',
            'force': True,
            'count': 1
        }
    }
}

class BeetsSetup:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'beets'
        self.config_file = self.config_dir / 'config.yaml'

    def create_directory_structure(self, music_dir: str) -> bool:
        """Create the necessary directory structure for music library."""
        try:
            music_path = Path(music_dir).expanduser()
            music_path.mkdir(parents=True, exist_ok=True)

            # Create common subdirectories
            subdirs = ['Incoming', 'To Process', 'Various Artists', 'Singletons']
            for subdir in subdirs:
                (music_path / subdir).mkdir(exist_ok=True)

            print(f"✅ Created directory structure at: {music_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating directories: {e}")
            return False

    def generate_config(self, template_name: str, custom_values: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate configuration from template with optional custom values."""
        if template_name not in CONFIG_TEMPLATES:
            raise ValueError(f"Unknown template: {template_name}")

        config = CONFIG_TEMPLATES[template_name].copy()

        if custom_values:
            # Deep merge custom values
            for key, value in custom_values.items():
                if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                    config[key].update(value)
                else:
                    config[key] = value

        return config

    def save_config(self, config: Dict[str, Any], config_path: Optional[str] = None) -> bool:
        """Save configuration to file."""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self.config_file

        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)

            print(f"✅ Configuration saved to: {config_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False

    def validate_config(self, config_path: Optional[str] = None) -> bool:
        """Validate beets configuration."""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self.config_file

        if not config_file.exists():
            print(f"❌ Configuration file not found: {config_file}")
            return False

        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)

            # Basic validation checks
            required_fields = ['directory', 'library']
            for field in required_fields:
                if field not in config:
                    print(f"❌ Missing required field: {field}")
                    return False

            # Validate plugins
            if 'plugins' in config:
                for plugin in config['plugins']:
                    if not isinstance(plugin, str):
                        print(f"❌ Invalid plugin name: {plugin}")
                        return False

            # Validate paths
            if 'paths' in config:
                for path_name, path_format in config['paths'].items():
                    if not isinstance(path_format, str):
                        print(f"❌ Invalid path format for {path_name}")
                        return False

            print("✅ Configuration validation passed")
            return True

        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error validating configuration: {e}")
            return False

    def interactive_setup(self) -> Dict[str, Any]:
        """Interactive configuration setup."""
        print("🎵 Beets Interactive Setup")
        print("=" * 40)

        # Template selection
        print("\nAvailable configuration templates:")
        for i, template in enumerate(CONFIG_TEMPLATES.keys(), 1):
            print(f"{i}. {template}")

        while True:
            try:
                choice = input("\nSelect template (1-{}): ".format(len(CONFIG_TEMPLATES)))
                template_idx = int(choice) - 1
                template_name = list(CONFIG_TEMPLATES.keys())[template_idx]
                break
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")

        print(f"\nSelected template: {template_name}")

        # Generate base config
        config = self.generate_config(template_name)

        # Music directory
        music_dir = input(f"\nMusic directory [{config['directory']}]: ").strip()
        if music_dir:
            config['directory'] = music_dir

        # Library database location
        lib_path = input(f"Library database path [{config['library']}]: ").strip()
        if lib_path:
            config['library'] = lib_path

        # Plugin selection
        print(f"\nCurrent plugins: {', '.join(config['plugins'])}")
        add_plugins = input("Additional plugins (comma-separated): ").strip()
        if add_plugins:
            config['plugins'].extend([p.strip() for p in add_plugins.split(',')])

        return config

    def test_configuration(self, config_path: Optional[str] = None) -> bool:
        """Test beets configuration by running basic commands."""
        print("🧪 Testing beets configuration...")

        try:
            # Test basic beet commands
            import subprocess

            # Test config loading
            result = subprocess.run(['beet', 'config'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Configuration test failed: {result.stderr}")
                return False

            # Test library access
            result = subprocess.run(['beet', 'list', '-f', '$artist'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Library access test failed: {result.stderr}")
                return False

            print("✅ Configuration test passed")
            return True

        except FileNotFoundError:
            print("❌ Beets not found. Please install beets first.")
            return False
        except Exception as e:
            print(f"❌ Configuration test error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Beets setup and configuration generator')
    parser.add_argument('--template', choices=list(CONFIG_TEMPLATES.keys()),
                       help='Configuration template to use')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive configuration setup')
    parser.add_argument('--music-dir', help='Music directory path')
    parser.add_argument('--config-path', help='Custom configuration file path')
    parser.add_argument('--validate-config', action='store_true',
                       help='Validate existing configuration')
    parser.add_argument('--test-config', action='store_true',
                       help='Test configuration by running beets commands')
    parser.add_argument('--create-dirs', action='store_true',
                       help='Create directory structure')

    args = parser.parse_args()

    setup = BeetsSetup()

    if args.validate_config:
        success = setup.validate_config(args.config_path)
        sys.exit(0 if success else 1)

    if args.test_config:
        success = setup.test_configuration(args.config_path)
        sys.exit(0 if success else 1)

    if args.interactive:
        config = setup.interactive_setup()
    elif args.template:
        config = setup.generate_config(args.template)
        if args.music_dir:
            config['directory'] = args.music_dir
    else:
        print("Please specify --template or --interactive mode")
        sys.exit(1)

    # Save configuration
    success = setup.save_config(config, args.config_path)
    if not success:
        sys.exit(1)

    # Create directories if requested
    if args.create_dirs:
        setup.create_directory_structure(config['directory'])

    # Test configuration
    if args.test_config:
        setup.test_configuration(args.config_path)

    print("\n✅ Beets setup completed!")
    print(f"Configuration saved to: {args.config_path or setup.config_file}")
    print(f"Music directory: {config['directory']}")
    print(f"Enabled plugins: {', '.join(config['plugins'])}")

if __name__ == '__main__':
    main()