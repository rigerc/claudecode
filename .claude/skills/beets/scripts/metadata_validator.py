#!/usr/bin/env python3
"""
Beets Metadata Validator

This script validates metadata consistency, performs batch operations, and ensures
data quality in beets music libraries.
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import json

class MetadataValidator:
    def __init__(self):
        self.validation_rules = {
            'required_fields': ['artist', 'album', 'title', 'track'],
            'numeric_fields': ['year', 'track', 'tracktotal', 'disc', 'disctotal', 'bitrate'],
            'date_fields': ['added', 'mtime'],
            'list_fields': ['genre', 'style', 'mood']
        }

        self.quality_checks = {
            'min_bitrate': 128000,  # 128 kbps
            'min_year': 1900,
            'max_year': 2030,
            'max_title_length': 200,
            'max_artist_length': 100,
            'max_album_length': 200
        }

    def get_library_items(self, query: str = "") -> List[Dict[str, Any]]:
        """Get all items from the library."""
        try:
            # Use beet list with JSON format if available, otherwise parse text
            cmd = ['beet', 'list', '-f', '$artist|$album|$title|$year|$track|$genre|$bitrate|$format']
            if query:
                cmd.append(query)

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error fetching library items: {result.stderr}")
                return []

            items = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('|')
                    if len(parts) >= 8:
                        items.append({
                            'artist': parts[0] or 'Unknown',
                            'album': parts[1] or 'Unknown',
                            'title': parts[2] or 'Unknown',
                            'year': parts[3] or '',
                            'track': parts[4] or '',
                            'genre': parts[5] or '',
                            'bitrate': parts[6] or '',
                            'format': parts[7] or ''
                        })

            return items

        except Exception as e:
            print(f"Error getting library items: {e}")
            return []

    def validate_field_completeness(self, items: List[Dict]) -> Dict[str, Any]:
        """Check for missing or empty required fields."""
        issues = {
            'missing_fields': [],
            'field_stats': {},
            'summary': {}
        }

        total_items = len(items)
        if total_items == 0:
            return issues

        for field in self.validation_rules['required_fields']:
            missing_count = 0
            empty_count = 0

            for item in items:
                if field not in item:
                    missing_count += 1
                elif not item[field] or item[field] in ['Unknown', '']:
                    empty_count += 1

            missing_percent = (missing_count / total_items) * 100
            empty_percent = (empty_count / total_items) * 100

            issues['field_stats'][field] = {
                'missing': missing_count,
                'empty': empty_count,
                'missing_percent': missing_percent,
                'empty_percent': empty_percent
            }

            if missing_count > 0 or empty_count > 0:
                issues['missing_fields'].append({
                    'field': field,
                    'missing_count': missing_count,
                    'empty_count': empty_count,
                    'total_affected': missing_count + empty_count
                })

        issues['summary'] = {
            'total_items': total_items,
            'fields_with_issues': len(issues['missing_fields']),
            'items_with_missing_data': len(set(
                item['_id'] for item in items
                for field in self.validation_rules['required_fields']
                if field not in item or not item[field] or item[field] in ['Unknown', '']
            ))
        }

        return issues

    def validate_numeric_fields(self, items: List[Dict]) -> Dict[str, Any]:
        """Validate numeric field formats and ranges."""
        issues = {
            'invalid_numbers': [],
            'out_of_range': [],
            'summary': {}
        }

        for item in items:
            item_issues = []

            for field in self.validation_rules['numeric_fields']:
                if field not in item or not item[field]:
                    continue

                value = item[field]

                # Check if it's a valid number
                try:
                    num_value = int(value)

                    # Range checks
                    if field == 'year':
                        if num_value < self.quality_checks['min_year'] or num_value > self.quality_checks['max_year']:
                            item_issues.append(f"{field}: {num_value} (out of range)")
                    elif field == 'bitrate':
                        if num_value < self.quality_checks['min_bitrate']:
                            item_issues.append(f"{field}: {num_value} (low quality)")

                except ValueError:
                    item_issues.append(f"{field}: {value} (not a number)")

            if item_issues:
                issues['invalid_numbers'].append({
                    'item': item,
                    'issues': item_issues
                })

        issues['summary'] = {
            'total_items': len(items),
            'items_with_issues': len(issues['invalid_numbers'])
        }

        return issues

    def validate_text_quality(self, items: List[Dict]) -> Dict[str, Any]:
        """Validate text field quality and formatting."""
        issues = {
            'length_issues': [],
            'formatting_issues': [],
            'encoding_issues': [],
            'summary': {}
        }

        for item in items:
            item_issues = []

            # Check length limits
            for field in ['title', 'artist', 'album']:
                if field in item and item[field]:
                    length = len(item[field])
                    max_length = self.quality_checks[f'max_{field}_length']

                    if length > max_length:
                        item_issues.append(f"{field}: {length} chars (too long)")

            # Check for common formatting issues
            for field in ['title', 'artist', 'album']:
                if field in item and item[field]:
                    text = item[field]

                    # Check for extra whitespace
                    if text != text.strip():
                        item_issues.append(f"{field}: has leading/trailing whitespace")

                    # Check for multiple spaces
                    if '  ' in text:
                        item_issues.append(f"{field}: has multiple consecutive spaces")

                    # Check for all caps
                    if text.isupper() and len(text) > 3:
                        item_issues.append(f"{field}: all uppercase")

                    # Check for all lowercase
                    if text.islower() and len(text) > 3:
                        item_issues.append(f"{field}: all lowercase")

            if item_issues:
                issues['formatting_issues'].append({
                    'item': item,
                    'issues': item_issues
                })

        issues['summary'] = {
            'total_items': len(items),
            'items_with_issues': len(issues['formatting_issues'])
        }

        return issues

    def check_duplicates(self, items: List[Dict]) -> Dict[str, Any]:
        """Check for duplicate items based on various criteria."""
        issues = {
            'exact_duplicates': [],
            'likely_duplicates': [],
            'summary': {}
        }

        # Create signatures for exact duplicates
        signatures = {}
        for item in items:
            signature = f"{item['artist']}|{item['album']}|{item['title']}|{item['track']}"
            if signature not in signatures:
                signatures[signature] = []
            signatures[signature].append(item)

        # Find exact duplicates
        for signature, dup_items in signatures.items():
            if len(dup_items) > 1:
                issues['exact_duplicates'].append({
                    'signature': signature,
                    'count': len(dup_items),
                    'items': dup_items
                })

        # Find likely duplicates (same artist and title, different album/track)
        title_signatures = {}
        for item in items:
            title_sig = f"{item['artist']}|{item['title']}"
            if title_sig not in title_signatures:
                title_signatures[title_sig] = []
            title_signatures[title_sig].append(item)

        for title_sig, dup_items in title_signatures.items():
            if len(dup_items) > 1:
                # Check if they're not exact duplicates
                albums = set(item['album'] for item in dup_items)
                if len(albums) > 1:
                    issues['likely_duplicates'].append({
                        'signature': title_sig,
                        'count': len(dup_items),
                        'items': dup_items,
                        'albums': list(albums)
                    })

        issues['summary'] = {
            'total_items': len(items),
            'exact_duplicate_groups': len(issues['exact_duplicates']),
            'likely_duplicate_groups': len(issues['likely_duplicates']),
            'total_duplicate_items': sum(
                group['count'] for group in issues['exact_duplicates']
            ) + sum(
                group['count'] for group in issues['likely_duplicates']
            )
        }

        return issues

    def generate_quality_report(self, items: List[Dict]) -> Dict[str, Any]:
        """Generate a comprehensive quality report."""
        print("🔍 Analyzing library metadata quality...")
        print("=" * 50)

        report = {
            'summary': {
                'total_items': len(items),
                'analysis_timestamp': str(Path(__file__).stat().st_mtime)
            },
            'checks': {}
        }

        # Run all validation checks
        print("Checking field completeness...")
        report['checks']['field_completeness'] = self.validate_field_completeness(items)

        print("Validating numeric fields...")
        report['checks']['numeric_validation'] = self.validate_numeric_fields(items)

        print("Analyzing text quality...")
        report['checks']['text_quality'] = self.validate_text_quality(items)

        print("Checking for duplicates...")
        report['checks']['duplicates'] = self.check_duplicates(items)

        # Calculate overall quality score
        total_issues = 0
        max_possible_issues = 0

        for check_name, check_result in report['checks'].items():
            if 'items_with_issues' in check_result.get('summary', {}):
                total_issues += check_result['summary']['items_with_issues']
                max_possible_issues += check_result['summary']['total_items']

        if max_possible_issues > 0:
            quality_score = max(0, 100 - (total_issues / max_possible_issues * 100))
        else:
            quality_score = 100

        report['quality_score'] = round(quality_score, 2)

        return report

    def display_report(self, report: Dict[str, Any]) -> None:
        """Display the quality report in a readable format."""
        print(f"\n📊 Library Quality Report")
        print("=" * 40)
        print(f"Total Items: {report['summary']['total_items']}")
        print(f"Overall Quality Score: {report['quality_score']}/100")
        print()

        # Field completeness
        field_check = report['checks']['field_completeness']
        print(f"📋 Field Completeness:")
        print(f"  Items with missing data: {field_check['summary']['items_with_missing_data']}")
        if field_check['missing_fields']:
            print("  Issues by field:")
            for field_info in field_check['missing_fields']:
                print(f"    - {field_info['field']}: {field_info['total_affected']} items affected")

        # Numeric validation
        numeric_check = report['checks']['numeric_validation']
        print(f"\n🔢 Numeric Validation:")
        print(f"  Items with numeric issues: {numeric_check['summary']['items_with_issues']}")

        # Text quality
        text_check = report['checks']['text_quality']
        print(f"\n✍️ Text Quality:")
        print(f"  Items with formatting issues: {text_check['summary']['items_with_issues']}")

        # Duplicates
        dup_check = report['checks']['duplicates']
        print(f"\n🔄 Duplicates:")
        print(f"  Exact duplicate groups: {dup_check['summary']['exact_duplicate_groups']}")
        print(f"  Likely duplicate groups: {dup_check['summary']['likely_duplicate_groups']}")

    def batch_modify(self, query: str, modifications: List[str]) -> bool:
        """Perform batch modifications using beet modify."""
        try:
            cmd = ['beet', 'modify', '-y', query] + modifications
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Batch modification completed")
                print(f"Output: {result.stdout}")
                return True
            else:
                print(f"❌ Batch modification failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error during batch modification: {e}")
            return False

    def fix_common_issues(self, items: List[Dict]) -> None:
        """Automatically fix common metadata issues."""
        print("🔧 Fixing common metadata issues...")

        fix_count = 0

        for item in items:
            modifications = []

            # Fix whitespace issues
            for field in ['artist', 'album', 'title']:
                if field in item and item[field]:
                    original = item[field]
                    fixed = original.strip()

                    # Remove extra spaces
                    while '  ' in fixed:
                        fixed = fixed.replace('  ', ' ')

                    if fixed != original:
                        modifications.append(f"{field}={fixed}")

            # Capitalize titles (simple title case)
            if 'title' in item and item['title']:
                title = item['title']
                if title.islower() and len(title) > 3:
                    fixed = title.title()
                    modifications.append(f"title={fixed}")

            # Apply modifications if any
            if modifications:
                query = f"artist:{item['artist']} album:{item['album']} title:{item['title']}"
                if self.batch_modify(query, modifications):
                    fix_count += 1

        print(f"✅ Fixed issues in {fix_count} items")

def main():
    parser = argparse.ArgumentParser(description='Beets metadata validator')
    parser.add_argument('--check-all', action='store_true',
                       help='Run all validation checks')
    parser.add_argument('--query', help='Query to filter items to validate')
    parser.add_argument('--batch-modify', nargs='+',
                       help='Batch modify items (format: field=value)')
    parser.add_argument('--fix-issues', action='store_true',
                       help='Automatically fix common issues')
    parser.add_argument('--quality-report', action='store_true',
                       help='Generate detailed quality report')
    parser.add_argument('--check-duplicates', action='store_true',
                       help='Check for duplicate items')
    parser.add_argument('--check-completeness', action='store_true',
                       help='Check for missing required fields')

    args = parser.parse_args()

    validator = MetadataValidator()

    # Get library items
    print("📚 Loading library...")
    items = validator.get_library_items(args.query or "")
    print(f"✅ Loaded {len(items)} items")

    if not items:
        print("No items found in library")
        sys.exit(1)

    if args.check_all or args.quality_report:
        report = validator.generate_quality_report(items)
        validator.display_report(report)

        if args.quality_report:
            # Save detailed report to file
            with open('beets_quality_report.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n📄 Detailed report saved to: beets_quality_report.json")

    if args.check_completeness:
        issues = validator.validate_field_completeness(items)
        print(f"\n📋 Field Completeness Issues:")
        print(f"Items with missing data: {issues['summary']['items_with_missing_data']}")
        for field_info in issues['missing_fields']:
            print(f"  - {field_info['field']}: {field_info['total_affected']} items")

    if args.check_duplicates:
        duplicates = validator.check_duplicates(items)
        print(f"\n🔄 Duplicate Analysis:")
        print(f"Exact duplicate groups: {duplicates['summary']['exact_duplicate_groups']}")
        print(f"Likely duplicate groups: {duplicates['summary']['likely_duplicate_groups']}")

        if duplicates['exact_duplicates']:
            print("\nExact duplicates found:")
            for group in duplicates['exact_duplicates'][:5]:  # Show first 5
                print(f"  - {group['signature']} ({group['count']} copies)")

    if args.batch_modify:
        if not args.query:
            print("❌ --query is required for batch modification")
            sys.exit(1)

        success = validator.batch_modify(args.query, args.batch_modify)
        sys.exit(0 if success else 1)

    if args.fix_issues:
        validator.fix_common_issues(items)

    if not any([args.check_all, args.quality_report, args.check_duplicates,
                args.check_completeness, args.batch_modify, args.fix_issues]):
        print("Please specify an action. Use --help for options.")
        sys.exit(1)

if __name__ == '__main__':
    main()