#!/usr/bin/env python3
"""
Beets Import Helper

This script provides guided import workflows, batch processing, and import troubleshooting
for beets music library management.
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

class BeetsImportHelper:
    def __init__(self):
        self.import_log = []
        self.config_dir = Path.home() / '.config' / 'beets'
        self.library_db = self.config_dir / 'library.db'

    def check_beets_installation(self) -> bool:
        """Check if beets is properly installed."""
        try:
            result = subprocess.run(['beet', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Beets version: {result.stdout.strip()}")
                return True
            else:
                print("❌ Beets installation check failed")
                return False
        except FileNotFoundError:
            print("❌ Beets not found. Please install beets first.")
            return False

    def validate_import_source(self, source_path: str) -> bool:
        """Validate the import source directory."""
        source = Path(source_path)

        if not source.exists():
            print(f"❌ Source directory does not exist: {source}")
            return False

        if not source.is_dir():
            print(f"❌ Source is not a directory: {source}")
            return False

        # Check for audio files
        audio_extensions = {'.mp3', '.flac', '.m4a', '.ogg', '.wav', '.wma', '.aac'}
        audio_files = []

        for ext in audio_extensions:
            audio_files.extend(source.rglob(f'*{ext}'))

        if not audio_files:
            print(f"❌ No audio files found in: {source}")
            return False

        print(f"✅ Found {len(audio_files)} audio files in source directory")
        return True

    def guided_import(self, source_path: str, options: Optional[Dict] = None) -> bool:
        """Run a guided import workflow."""
        print(f"🎵 Starting guided import from: {source_path}")
        print("=" * 50)

        # Default import options
        default_options = {
            'copy': True,
            'write': True,
            'autotag': True,
            'quiet': False,
            'delete': False,
            'move': False,
            'threads': 4
        }

        if options:
            default_options.update(options)

        # Build import command
        cmd = ['beet', 'import']

        # Add options
        if default_options['copy']:
            cmd.append('--copy')
        if default_options['write']:
            cmd.append('--write')
        if default_options['autotag']:
            cmd.append('--autotag')
        if default_options['quiet']:
            cmd.append('--quiet')
        if default_options['delete']:
            cmd.append('--delete')
        if default_options['move']:
            cmd.append('--move')

        cmd.extend(['--threads', str(default_options['threads'])])
        cmd.append(source_path)

        # Show the command
        print(f"Running command: {' '.join(cmd)}")
        print()

        try:
            # Run the import
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Monitor progress
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    self.import_log.append(output.strip())

            # Check result
            return_code = process.poll()
            stderr = process.stderr.read()

            if return_code == 0:
                print("✅ Import completed successfully")
                return True
            else:
                print(f"❌ Import failed with return code {return_code}")
                if stderr:
                    print(f"Error: {stderr}")
                return False

        except Exception as e:
            print(f"❌ Import error: {e}")
            return False

    def batch_import(self, source_dirs: List[str], options: Optional[Dict] = None) -> Dict[str, bool]:
        """Import multiple directories in batch."""
        print(f"🎵 Starting batch import of {len(source_dirs)} directories")
        print("=" * 50)

        results = {}

        for i, source_dir in enumerate(source_dirs, 1):
            print(f"\n[{i}/{len(source_dirs)}] Processing: {source_dir}")

            if not self.validate_import_source(source_dir):
                results[source_dir] = False
                continue

            success = self.guided_import(source_dir, options)
            results[source_dir] = success

            # Small delay between imports
            time.sleep(1)

        # Summary
        successful = sum(1 for success in results.values() if success)
        print(f"\n📊 Batch import summary:")
        print(f"✅ Successful: {successful}/{len(source_dirs)}")
        print(f"❌ Failed: {len(source_dirs) - successful}/{len(source_dirs)}")

        return results

    def watch_directory(self, watch_path: str, auto_import: bool = False) -> None:
        """Watch a directory for new files and optionally auto-import."""
        print(f"👀 Watching directory: {watch_path}")
        print("Press Ctrl+C to stop watching")

        try:
            # Simple polling implementation
            processed_files = set()

            while True:
                # Scan for new audio files
                audio_extensions = {'.mp3', '.flac', '.m4a', '.ogg', '.wav', '.wma', '.aac'}
                current_files = set()

                for ext in audio_extensions:
                    current_files.update(Path(watch_path).rglob(f'*{ext}'))

                new_files = current_files - processed_files

                if new_files and auto_import:
                    print(f"🎵 Found {len(new_files)} new files, starting auto-import...")
                    success = self.guided_import(watch_path)
                    if success:
                        processed_files.update(current_files)
                elif new_files:
                    print(f"📁 Found {len(new_files)} new files:")
                    for file_path in sorted(new_files)[:5]:  # Show first 5
                        print(f"  - {file_path}")
                    if len(new_files) > 5:
                        print(f"  ... and {len(new_files) - 5} more files")

                time.sleep(30)  # Check every 30 seconds

        except KeyboardInterrupt:
            print("\n👋 Stopped watching directory")

    def diagnose_import_issues(self) -> bool:
        """Diagnose common import issues."""
        print("🔍 Diagnosing beets import issues...")
        print("=" * 40)

        issues_found = []

        # Check beets installation
        if not self.check_beets_installation():
            issues_found.append("Beets installation problem")

        # Check configuration
        config_file = self.config_dir / 'config.yaml'
        if not config_file.exists():
            issues_found.append("Configuration file not found")
        else:
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)

                if 'directory' not in config:
                    issues_found.append("Music directory not configured")
                elif not Path(config['directory']).expanduser().exists():
                    issues_found.append(f"Music directory does not exist: {config['directory']}")

                if 'library' not in config:
                    issues_found.append("Library database path not configured")

            except Exception as e:
                issues_found.append(f"Configuration file error: {e}")

        # Check library database
        if not self.library_db.exists():
            issues_found.append("Library database does not exist (run initial import)")
        else:
            # Check database integrity
            try:
                result = subprocess.run(['beet', 'list', '-f', '$artist'],
                                       capture_output=True, text=True)
                if result.returncode != 0:
                    issues_found.append("Library database access error")
            except Exception as e:
                issues_found.append(f"Database check error: {e}")

        # Check plugins
        try:
            result = subprocess.run(['beet', 'plugins'], capture_output=True, text=True)
            if result.returncode != 0:
                issues_found.append("Plugin system error")
        except Exception:
            issues_found.append("Unable to check plugins")

        # Report results
        if issues_found:
            print("❌ Issues found:")
            for i, issue in enumerate(issues_found, 1):
                print(f"{i}. {issue}")

            print("\n💡 Suggested fixes:")
            if "Beets installation problem" in issues_found:
                print("- Install beets: pip install beets")
            if "Configuration file not found" in issues_found:
                print("- Create configuration: beet config -e")
            if "Music directory does not exist" in issues_found:
                print("- Create music directory or update config")
            if "Library database does not exist" in issues_found:
                print("- Run initial import to create database")

            return False
        else:
            print("✅ No issues found with beets setup")
            return True

    def get_import_statistics(self) -> Dict[str, Any]:
        """Get statistics about the library."""
        try:
            # Get total items
            result = subprocess.run(['beet', 'list', '-f', '$artist'],
                                   capture_output=True, text=True)
            total_items = len([line for line in result.stdout.split('\n') if line.strip()])

            # Get total albums
            result = subprocess.run(['beet', 'list', '-a', '-f', '$albumartist - $album'],
                                   capture_output=True, text=True)
            total_albums = len([line for line in result.stdout.split('\n') if line.strip()])

            # Get library size (approximate)
            result = subprocess.run(['beet', 'stats'], capture_output=True, text=True)
            stats_output = result.stdout

            return {
                'total_items': total_items,
                'total_albums': total_albums,
                'stats_output': stats_output
            }

        except Exception as e:
            return {'error': str(e)}

    def interactive_import_wizard(self) -> None:
        """Interactive import wizard for new users."""
        print("🧙‍♂️ Beets Import Wizard")
        print("=" * 30)
        print("This wizard will guide you through importing music into your library.\n")

        # Step 1: Check setup
        print("Step 1: Checking beets setup...")
        if not self.diagnose_import_issues():
            print("❌ Please fix the issues above before proceeding.")
            return
        print("✅ Beets setup looks good!\n")

        # Step 2: Get source directory
        while True:
            source_path = input("Enter the path to your music directory: ").strip()
            if self.validate_import_source(source_path):
                break
            print("Please enter a valid directory containing audio files.\n")

        # Step 3: Import options
        print("\nStep 3: Import options")
        print("These options control how your music will be imported:")

        copy = input("Copy files to library directory? (Y/n): ").strip().lower() != 'n'
        write = input("Write metadata to files? (Y/n): ").strip().lower() != 'n'
        autotag = input("Automatically tag music? (Y/n): ").strip().lower() != 'n'
        delete = input("Delete original files after import? (y/N): ").strip().lower() == 'y'

        options = {
            'copy': copy,
            'write': write,
            'autotag': autotag,
            'delete': delete,
            'quiet': False
        }

        # Step 4: Confirmation
        print(f"\nStep 4: Import Summary")
        print(f"Source: {source_path}")
        print(f"Copy files: {'Yes' if copy else 'No'}")
        print(f"Write metadata: {'Yes' if write else 'No'}")
        print(f"Auto-tag: {'Yes' if autotag else 'No'}")
        print(f"Delete originals: {'Yes' if delete else 'No'}")

        confirm = input("\nProceed with import? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("Import cancelled.")
            return

        # Step 5: Execute import
        print("\nStep 5: Starting import...")
        success = self.guided_import(source_path, options)

        if success:
            print("\n✅ Import completed successfully!")
            stats = self.get_import_statistics()
            if 'error' not in stats:
                print(f"Library now contains {stats['total_items']} items and {stats['total_albums']} albums")
        else:
            print("\n❌ Import encountered issues. Check the logs above for details.")

def main():
    parser = argparse.ArgumentParser(description='Beets import helper')
    parser.add_argument('source', nargs='?', help='Source directory to import')
    parser.add_argument('--guided-import', action='store_true',
                       help='Run guided import workflow')
    parser.add_argument('--batch', nargs='+',
                       help='Import multiple directories in batch')
    parser.add_argument('--watch', help='Watch directory for new files')
    parser.add_argument('--auto-import', action='store_true',
                       help='Automatically import when watching directory')
    parser.add_argument('--diagnose', action='store_true',
                       help='Diagnose import issues')
    parser.add_argument('--wizard', action='store_true',
                       help='Run interactive import wizard')
    parser.add_argument('--copy', action='store_true',
                       help='Copy files to library')
    parser.add_argument('--move', action='store_true',
                       help='Move files to library')
    parser.add_argument('--write', action='store_true',
                       help='Write metadata to files')
    parser.add_argument('--no-autotag', action='store_true',
                       help='Disable automatic tagging')
    parser.add_argument('--delete', action='store_true',
                       help='Delete original files')

    args = parser.parse_args()

    helper = BeetsImportHelper()

    if args.diagnose:
        success = helper.diagnose_import_issues()
        sys.exit(0 if success else 1)

    if args.wizard:
        helper.interactive_import_wizard()
        return

    if args.watch:
        helper.watch_directory(args.watch, args.auto_import)
        return

    # Build import options
    options = {}
    if args.copy:
        options['copy'] = True
    if args.move:
        options['move'] = True
    if args.write:
        options['write'] = True
    if args.no_autotag:
        options['autotag'] = False
    if args.delete:
        options['delete'] = True

    if args.batch:
        results = helper.batch_import(args.batch, options)
        failed_count = sum(1 for success in results.values() if not success)
        sys.exit(1 if failed_count > 0 else 0)
    elif args.source:
        if not helper.validate_import_source(args.source):
            sys.exit(1)

        success = helper.guided_import(args.source, options)
        sys.exit(0 if success else 1)
    elif args.guided_import:
        source = input("Enter source directory: ").strip()
        if not helper.validate_import_source(source):
            sys.exit(1)

        success = helper.guided_import(source, options)
        sys.exit(0 if success else 1)
    else:
        print("Please specify a source directory or use --wizard for interactive mode")
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()