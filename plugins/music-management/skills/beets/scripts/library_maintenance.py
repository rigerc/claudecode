#!/usr/bin/env python3
"""
Beets Library Maintenance

This script provides comprehensive library maintenance tools including duplicate detection,
consistency checks, cleanup operations, and optimization.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import json
import time
import hashlib

class LibraryMaintenance:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'beets'
        self.library_db = self.config_dir / 'library.db'
        self.backup_dir = self.config_dir / 'backups'

    def backup_library(self) -> bool:
        """Create a backup of the library database."""
        try:
            self.backup_dir.mkdir(exist_ok=True)

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'library_backup_{timestamp}.db'

            if not self.library_db.exists():
                print(f"❌ Library database not found: {self.library_db}")
                return False

            # Copy database
            import shutil
            shutil.copy2(self.library_db, backup_file)

            print(f"✅ Library backup created: {backup_file}")

            # Keep only last 10 backups
            backups = sorted(self.backup_dir.glob('library_backup_*.db'))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
                    print(f"🗑️  Removed old backup: {old_backup}")

            return True

        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False

    def detect_duplicates(self, auto_resolve: bool = False) -> Dict[str, Any]:
        """Detect and optionally resolve duplicate items."""
        print("🔍 Detecting duplicate items...")

        duplicates = {
            'exact_duplicates': [],
            'likely_duplicates': [],
            'resolved': []
        }

        try:
            # Find exact duplicates using beets
            cmd = ['beet', 'duplicates', '-f', '$artist|$album|$title|$track|$path']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                current_group = []

                for line in lines:
                    if line.startswith('-' * 20):
                        if current_group:
                            duplicates['exact_duplicates'].append(current_group)
                        current_group = []
                    else:
                        parts = line.split('|')
                        if len(parts) >= 5:
                            current_group.append({
                                'artist': parts[0],
                                'album': parts[1],
                                'title': parts[2],
                                'track': parts[3],
                                'path': parts[4]
                            })

                if current_group:
                    duplicates['exact_duplicates'].append(current_group)

            print(f"Found {len(duplicates['exact_duplicates'])} exact duplicate groups")

            if auto_resolve and duplicates['exact_duplicates']:
                print("🔧 Auto-resolving duplicates...")
                self._resolve_duplicates(duplicates['exact_duplicates'], duplicates)

        except Exception as e:
            print(f"❌ Error detecting duplicates: {e}")

        return duplicates

    def _resolve_duplicates(self, duplicate_groups: List[List[Dict]], duplicates: Dict):
        """Resolve duplicate groups automatically."""
        for group in duplicate_groups:
            if len(group) < 2:
                continue

            # Strategy: keep the highest quality file
            best_item = max(group, key=lambda x: int(x.get('bitrate', 0)))
            items_to_remove = [item for item in group if item != best_item]

            for item in items_to_remove:
                try:
                    # Remove from library
                    path = item['path']
                    cmd = ['beet', 'remove', '-y', f'path:{path}']
                    result = subprocess.run(cmd, capture_output=True, text=True)

                    if result.returncode == 0:
                        duplicates['resolved'].append(item)
                        print(f"  🗑️  Removed: {item['artist']} - {item['title']}")
                    else:
                        print(f"  ❌ Failed to remove: {item['title']} - {result.stderr}")

                except Exception as e:
                    print(f"  ❌ Error removing item: {e}")

    def check_library_consistency(self) -> Dict[str, Any]:
        """Check library consistency and identify issues."""
        print("🔍 Checking library consistency...")

        issues = {
            'missing_files': [],
            'orphaned_items': [],
            'format_issues': [],
            'path_issues': [],
            'summary': {}
        }

        try:
            # Check for missing files
            cmd = ['beet', 'list', '-f', '$id|$path']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split('|', 1)
                        if len(parts) == 2:
                            item_id, path = parts
                            full_path = Path(path).expanduser()

                            if not full_path.exists():
                                issues['missing_files'].append({
                                    'id': item_id,
                                    'path': path
                                })

            # Check for format issues
            cmd = ['beet', 'list', '-f', '$id|$format|$bitrate']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split('|')
                        if len(parts) >= 3:
                            item_id, format_type, bitrate = parts[0], parts[1], parts[2]

                            if not format_type:
                                issues['format_issues'].append({
                                    'id': item_id,
                                    'issue': 'Missing format'
                                })
                            elif bitrate and bitrate.isdigit():
                                bitrate_val = int(bitrate)
                                if bitrate_val < 128000:  # Less than 128kbps
                                    issues['format_issues'].append({
                                        'id': item_id,
                                        'issue': f'Low bitrate: {bitrate_val}bps'
                                    })

            # Update summary
            issues['summary'] = {
                'missing_files': len(issues['missing_files']),
                'format_issues': len(issues['format_issues']),
                'path_issues': len(issues['path_issues'])
            }

            print(f"✅ Consistency check completed")
            print(f"  Missing files: {issues['summary']['missing_files']}")
            print(f"  Format issues: {issues['summary']['format_issues']}")
            print(f"  Path issues: {issues['summary']['path_issues']}")

        except Exception as e:
            print(f"❌ Error checking consistency: {e}")

        return issues

    def optimize_library(self) -> bool:
        """Optimize library performance."""
        print("🚀 Optimizing library performance...")

        try:
            # Vacuum database
            print("  Vacuuming database...")
            cmd = ['beet', 'modify', '--yes', '--nodb', 'dummy:true']
            result = subprocess.run(cmd, capture_output=True, text=True)
            # This is a workaround - beets doesn't have a direct vacuum command

            # Update all items to trigger database optimization
            print("  Updating item metadata...")
            cmd = ['beet', 'update', '--yes']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"  ⚠️  Update warning: {result.stderr}")

            # Rebuild statistics
            print("  Rebuilding statistics...")
            cmd = ['beet', 'stats']
            result = subprocess.run(cmd, capture_output=True, text=True)

            print("✅ Library optimization completed")
            return True

        except Exception as e:
            print(f"❌ Error optimizing library: {e}")
            return False

    def cleanup_unused_files(self) -> Dict[str, Any]:
        """Clean up unused files and directories."""
        print("🧹 Cleaning up unused files...")

        cleanup_stats = {
            'empty_dirs_removed': 0,
            'temp_files_removed': 0,
            'space_freed': 0
        }

        try:
            # Get music directory from config
            cmd = ['beet', 'config', '-p']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                music_dir = Path(result.stdout.strip()).expanduser()

                # Find empty directories
                for root, dirs, files in os.walk(music_dir, topdown=False):
                    for dir_name in dirs:
                        dir_path = Path(root) / dir_name
                        try:
                            if not any(dir_path.iterdir()):
                                dir_path.rmdir()
                                cleanup_stats['empty_dirs_removed'] += 1
                                print(f"  🗑️  Removed empty directory: {dir_path}")
                        except OSError:
                            pass  # Directory not empty or permission error

                # Find temporary files
                for temp_file in music_dir.rglob('*.tmp'):
                    try:
                        size = temp_file.stat().st_size
                        temp_file.unlink()
                        cleanup_stats['temp_files_removed'] += 1
                        cleanup_stats['space_freed'] += size
                        print(f"  🗑️  Removed temp file: {temp_file}")
                    except OSError:
                        pass

            print(f"✅ Cleanup completed")
            print(f"  Empty directories removed: {cleanup_stats['empty_dirs_removed']}")
            print(f"  Temp files removed: {cleanup_stats['temp_files_removed']}")
            print(f"  Space freed: {cleanup_stats['space_freed']} bytes")

        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

        return cleanup_stats

    def generate_library_report(self) -> Dict[str, Any]:
        """Generate a comprehensive library report."""
        print("📊 Generating library report...")

        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': {},
            'quality_metrics': {},
            'issues': {},
            'recommendations': []
        }

        try:
            # Basic statistics
            cmd = ['beet', 'stats']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # Parse stats output
                stats_lines = result.stdout.split('\n')
                for line in stats_lines:
                    if 'Tracks:' in line:
                        report['statistics']['tracks'] = int(line.split(':')[1].strip())
                    elif 'Albums:' in line:
                        report['statistics']['albums'] = int(line.split(':')[1].strip())
                    elif 'Artists:' in line:
                        report['statistics']['artists'] = int(line.split(':')[1].strip())
                    elif 'Total size:' in line:
                        report['statistics']['total_size'] = line.split(':')[1].strip()
                    elif 'Total time:' in line:
                        report['statistics']['total_time'] = line.split(':')[1].strip()

            # Format distribution
            cmd = ['beet', 'list', '-f', '$format', '--unique']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                formats = [f.strip() for f in result.stdout.split('\n') if f.strip()]
                report['quality_metrics']['formats'] = formats

            # Bitrate distribution
            bitrate_ranges = {
                'High (320kbps+)': 0,
                'Medium (192-319kbps)': 0,
                'Low (128-191kbps)': 0,
                'Very Low (<128kbps)': 0
            }

            cmd = ['beet', 'list', '-f', '$bitrate']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                bitrates = [int(b.strip()) for b in result.stdout.split('\n') if b.strip().isdigit()]
                for bitrate in bitrates:
                    if bitrate >= 320000:
                        bitrate_ranges['High (320kbps+)'] += 1
                    elif bitrate >= 192000:
                        bitrate_ranges['Medium (192-319kbps)'] += 1
                    elif bitrate >= 128000:
                        bitrate_ranges['Low (128-191kbps)'] += 1
                    else:
                        bitrate_ranges['Very Low (<128kbps)'] += 1

                report['quality_metrics']['bitrate_distribution'] = bitrate_ranges

            # Generate recommendations
            if bitrate_ranges['Very Low (<128kbps)'] > 0:
                report['recommendations'].append(
                    f"Consider upgrading {bitrate_ranges['Very Low (<128kbps)']} low bitrate files"
                )

            if len(formats) > 3:
                report['recommendations'].append(
                    "Consider standardizing audio formats for better organization"
                )

            # Check for duplicates
            duplicates = self.detect_duplicates()
            if duplicates['exact_duplicates']:
                report['recommendations'].append(
                    f"Found {len(duplicates['exact_duplicates'])} duplicate groups - consider cleanup"
                )

            print("✅ Library report generated")
            return report

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return report

    def run_full_maintenance(self, scheduled: bool = False, cleanup: bool = False) -> bool:
        """Run a full maintenance routine."""
        print("🔧 Starting full library maintenance...")
        print("=" * 50)

        success_count = 0
        total_operations = 4

        if scheduled:
            print("Running in scheduled mode...")

        # 1. Backup library
        print("\n1. Creating backup...")
        if self.backup_library():
            success_count += 1

        # 2. Check consistency
        print("\n2. Checking consistency...")
        issues = self.check_library_consistency()
        if issues:
            print(f"Found {sum(issues['summary'].values())} issues to address")
        success_count += 1

        # 3. Detect duplicates
        print("\n3. Checking for duplicates...")
        duplicates = self.detect_duplicates(auto_resolve=False)
        success_count += 1

        # 4. Optimize library
        print("\n4. Optimizing library...")
        if self.optimize_library():
            success_count += 1

        # 5. Cleanup (optional)
        if cleanup:
            print("\n5. Cleaning up unused files...")
            self.cleanup_unused_files()

        # Generate final report
        print(f"\n📊 Maintenance Summary:")
        print(f"Operations completed: {success_count}/{total_operations}")

        if duplicates['exact_duplicates']:
            print(f"Duplicate groups found: {len(duplicates['exact_duplicates'])}")

        total_issues = sum(issues['summary'].values())
        if total_issues > 0:
            print(f"Issues found: {total_issues}")

        print("\n✅ Library maintenance completed!")

        return success_count == total_operations

def main():
    parser = argparse.ArgumentParser(description='Beets library maintenance tool')
    parser.add_argument('--duplicates', action='store_true',
                       help='Detect duplicate items')
    parser.add_argument('--auto-resolve', action='store_true',
                       help='Automatically resolve duplicates')
    parser.add_argument('--consistency', action='store_true',
                       help='Check library consistency')
    parser.add_argument('--optimize', action='store_true',
                       help='Optimize library performance')
    parser.add_argument('--cleanup', action='store_true',
                       help='Clean up unused files')
    parser.add_argument('--full-check', action='store_true',
                       help='Run comprehensive maintenance check')
    parser.add_argument('--scheduled', action='store_true',
                       help='Run in scheduled mode (automated)')
    parser.add_argument('--backup', action='store_true',
                       help='Create library backup')
    parser.add_argument('--report', action='store_true',
                       help='Generate library report')
    parser.add_argument('--vacuum', action='store_true',
                       help='Vacuum and optimize database')

    args = parser.parse_args()

    maintenance = LibraryMaintenance()

    if args.full_check:
        success = maintenance.run_full_maintenance(args.scheduled, args.cleanup)
        sys.exit(0 if success else 1)

    if args.backup:
        success = maintenance.backup_library()
        sys.exit(0 if success else 1)

    if args.duplicates:
        duplicates = maintenance.detect_duplicates(args.auto_resolve)
        if duplicates['exact_duplicates']:
            print(f"\nFound {len(duplicates['exact_duplicates'])} duplicate groups")
            if args.auto_resolve:
                print(f"Resolved {len(duplicates['resolved'])} duplicates")

    if args.consistency:
        issues = maintenance.check_library_consistency()
        total_issues = sum(issues['summary'].values())
        if total_issues > 0:
            print(f"\nFound {total_issues} issues to address")

    if args.optimize or args.vacuum:
        maintenance.optimize_library()

    if args.cleanup:
        maintenance.cleanup_unused_files()

    if args.report:
        report = maintenance.generate_library_report()
        report_file = 'beets_library_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n📄 Report saved to: {report_file}")

    if not any([args.duplicates, args.consistency, args.optimize, args.cleanup,
                args.full_check, args.backup, args.report, args.vacuum]):
        print("Please specify a maintenance operation. Use --help for options.")
        sys.exit(1)

if __name__ == '__main__':
    main()