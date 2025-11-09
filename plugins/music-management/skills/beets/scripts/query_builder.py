#!/usr/bin/env python3
"""
Beets Query Builder

This script provides an interactive query builder, query validation, and optimization
for beets music library searches.
"""

import argparse
import subprocess
import sys
import re
from typing import List, Dict, Any, Optional, Tuple
import json

class BeetsQueryBuilder:
    def __init__(self):
        self.query_history = []
        self.query_examples = {
            'Basic Artist Search': "artist:Beatles",
            'Year Range': "year:1960..1969",
            'Genre Search': "genre:Rock",
            'Bitrate Filter': "bitrate:320000",
            'Combined Query': "artist:Led Zeppelin genre:Rock year:1970..1979",
            'Custom Field': "mood:party",
            'Album Search': "album:\"Dark Side of the Moon\"",
            'Missing Metadata': "missing:genre",
            'Duplicate Detection': "dup:true",
            'Singleton Tracks': "singleton:true"
        }

        self.query_fields = {
            'Standard Fields': [
                'artist', 'album', 'albumartist', 'title', 'genre', 'year',
                'track', 'tracktotal', 'disc', 'disctotal', 'bitrate',
                'format', 'length', 'size', 'mtime', 'added'
            ],
            'Flexible Fields': [
                'mood', 'rating', 'context', 'tempo', 'key', 'bpm',
                'language', 'country', 'label', 'composer', 'lyricist'
            ],
            'Special Queries': [
                'missing:', 'singleton:', 'comp:', 'duplicate:',
                'path:', 'comments:', 'lyrics:'
            ]
        }

        self.operators = {
            'Equals': ':',
            'Not Equals': '!:',
            'Contains': ':',
            'Matches Regex': ':',
            'Greater Than': '>',
            'Less Than': '<',
            'Greater or Equal': '>=',
            'Less or Equal': '<=',
            'Range': '..'
        }

    def validate_query_syntax(self, query: str) -> Tuple[bool, Optional[str]]:
        """Validate basic query syntax."""
        if not query.strip():
            return False, "Empty query"

        # Check for balanced quotes
        quote_count = query.count('"')
        if quote_count % 2 != 0:
            return False, "Unmatched quotes"

        # Check for invalid characters in field names
        field_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)([:!<>]=?|:)([^ ]+)'
        matches = re.findall(field_pattern, query)

        if not matches and ' ' not in query:
            # This might be a simple text search
            return True, None

        for field, operator, value in matches:
            if field not in self.get_all_fields():
                return False, f"Unknown field: {field}"

        return True, None

    def get_all_fields(self) -> List[str]:
        """Get all available query fields."""
        all_fields = []
        for category, fields in self.query_fields.items():
            all_fields.extend(fields)
        return all_fields

    def test_query(self, query: str) -> Tuple[bool, Optional[str], Optional[List[Dict]]]:
        """Test a query against the beets library."""
        try:
            # Run the query with beet list
            cmd = ['beet', 'list', '-f', '$artist - $album - $title', query]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if "no such query field" in error_msg.lower():
                    return False, "Invalid field in query", None
                elif "syntax error" in error_msg.lower():
                    return False, "Query syntax error", None
                else:
                    return False, f"Query error: {error_msg}", None

            # Parse results
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            results = []
            for line in lines:
                parts = line.split(' - ', 2)
                if len(parts) >= 3:
                    results.append({
                        'artist': parts[0],
                        'album': parts[1],
                        'title': parts[2]
                    })
                elif len(parts) == 2:
                    results.append({
                        'artist': parts[0],
                        'album': parts[1],
                        'title': ''
                    })
                elif len(parts) == 1:
                    results.append({
                        'artist': parts[0],
                        'album': '',
                        'title': ''
                    })

            return True, None, results

        except Exception as e:
            return False, f"Error executing query: {e}", None

    def optimize_query(self, query: str) -> Tuple[str, List[str]]:
        """Optimize query for better performance."""
        suggestions = []
        optimized = query

        # Suggest using specific fields instead of general text search
        if ' ' in query and ':' not in query:
            suggestions.append("Consider using specific fields (e.g., 'artist:name' instead of just 'name')")

        # Suggest using year ranges for better performance
        year_match = re.search(r'year:(\d{4})', optimized)
        if year_match and '..' not in optimized:
            year = year_match.group(1)
            suggestions.append(f"Consider using year range (e.g., 'year:{year}..{int(year)+4}')")

        # Suggest using more specific operators
        if ':320000' in optimized:
            suggestions.append("Consider using 'bitrate:>=320000' for high-quality audio")

        # Remove redundant terms
        terms = optimized.split()
        unique_terms = list(dict.fromkeys(terms))  # Preserve order, remove duplicates
        if len(unique_terms) != len(terms):
            optimized = ' '.join(unique_terms)
            suggestions.append("Removed duplicate terms")

        return optimized, suggestions

    def build_interactive_query(self) -> str:
        """Interactive query building."""
        print("🔍 Beets Interactive Query Builder")
        print("=" * 40)
        print("Build your query step by step. Press Enter to finish.\n")

        query_parts = []

        while True:
            print(f"Current query: {' '.join(query_parts) or '(empty)'}")
            print("\nOptions:")
            print("1. Add field filter")
            print("2. Add text search")
            print("3. Add logical operator (AND, OR)")
            print("4. Show example queries")
            print("5. Finish query")
            print("6. Clear query")

            choice = input("\nSelect option (1-6): ").strip()

            if choice == '1':
                field, value = self.get_field_filter()
                if field and value:
                    query_parts.append(f"{field}:{value}")
            elif choice == '2':
                text = input("Enter search text: ").strip()
                if text:
                    if ' ' in text:
                        query_parts.append(f'"{text}"')
                    else:
                        query_parts.append(text)
            elif choice == '3':
                operator = input("Enter operator (AND/OR): ").strip().upper()
                if operator in ['AND', 'OR']:
                    query_parts.append(operator)
            elif choice == '4':
                self.show_examples()
            elif choice == '5':
                break
            elif choice == '6':
                query_parts = []
            else:
                print("Invalid choice. Please try again.")

        final_query = ' '.join(query_parts)
        return final_query.strip()

    def get_field_filter(self) -> Tuple[Optional[str], Optional[str]]:
        """Get field and value for query filter."""
        print("\nAvailable fields:")
        categories = list(self.query_fields.keys())

        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        cat_choice = input(f"Select category (1-{len(categories)}): ").strip()
        try:
            cat_idx = int(cat_choice) - 1
            if 0 <= cat_idx < len(categories):
                category = categories[cat_idx]
                fields = self.query_fields[category]

                print(f"\n{category} fields:")
                for i, field in enumerate(fields, 1):
                    print(f"{i}. {field}")

                field_choice = input(f"Select field (1-{len(fields)}): ").strip()
                try:
                    field_idx = int(field_choice) - 1
                    if 0 <= field_idx < len(fields):
                        field = fields[field_idx]

                        print(f"\nOperators for {field}:")
                        ops = list(self.operators.keys())
                        for i, op in enumerate(ops, 1):
                            print(f"{i}. {op} ({self.operators[op]})")

                        op_choice = input(f"Select operator (1-{len(ops)}, default ':'): ").strip()
                        if op_choice and op_choice.isdigit():
                            op_idx = int(op_choice) - 1
                            if 0 <= op_idx < len(ops):
                                operator = self.operators[ops[op_idx]]
                            else:
                                operator = ':'
                        else:
                            operator = ':'

                        value = input(f"Enter value for {field}{operator}: ").strip()
                        return field, value

                except ValueError:
                    print("Invalid field selection")
                    return None, None
            else:
                print("Invalid category selection")
                return None, None

        except ValueError:
            print("Invalid choice")
            return None, None

    def show_examples(self) -> None:
        """Show example queries."""
        print("\n📋 Example Queries:")
        print("=" * 30)
        for i, (description, query) in enumerate(self.query_examples.items(), 1):
            print(f"{i}. {description}")
            print(f"   Query: {query}")
            print()

    def analyze_query_performance(self, query: str) -> Dict[str, Any]:
        """Analyze query performance characteristics."""
        analysis = {
            'complexity': 'low',
            'estimated_results': 'unknown',
            'optimization_suggestions': []
        }

        # Analyze complexity
        if ' OR ' in query or '..' in query:
            analysis['complexity'] = 'medium'
        if query.count(':') > 3 or ' AND ' in query:
            analysis['complexity'] = 'high'

        # Test query to get result count
        success, error, results = self.test_query(query)
        if success and results:
            analysis['estimated_results'] = len(results)

            # Provide suggestions based on results
            if len(results) > 1000:
                analysis['optimization_suggestions'].append("Large result set - consider adding more filters")
            elif len(results) == 0:
                analysis['optimization_suggestions'].append("No results - check spelling and field names")
            elif len(results) < 10:
                analysis['optimization_suggestions'].append("Very specific query - good for precision")

        # Check for optimization opportunities
        if 'artist:' in query and 'album:' not in query:
            analysis['optimization_suggestions'].append("Consider adding album filter for more specific results")

        return analysis

    def generate_query_report(self, query: str) -> None:
        """Generate a comprehensive query analysis report."""
        print(f"\n📊 Query Analysis Report")
        print("=" * 30)
        print(f"Query: {query}\n")

        # Validation
        is_valid, error = self.validate_query_syntax(query)
        if not is_valid:
            print(f"❌ Invalid Query: {error}")
            return

        print("✅ Query syntax is valid")

        # Test query
        success, error, results = self.test_query(query)
        if not success:
            print(f"❌ Query failed: {error}")
            return

        print(f"✅ Query executed successfully")
        print(f"📈 Results found: {len(results)}")

        # Show sample results
        if results:
            print(f"\n📄 Sample Results (showing first 5):")
            for i, result in enumerate(results[:5], 1):
                print(f"{i}. {result['artist']} - {result['album']} - {result['title']}")

        # Performance analysis
        analysis = self.analyze_query_performance(query)
        print(f"\n⚡ Performance Analysis:")
        print(f"Complexity: {analysis['complexity']}")

        if analysis['optimization_suggestions']:
            print(f"\n💡 Optimization Suggestions:")
            for suggestion in analysis['optimization_suggestions']:
                print(f"- {suggestion}")

        # Optimization
        optimized, suggestions = self.optimize_query(query)
        if optimized != query:
            print(f"\n🔧 Optimized Query: {optimized}")
            for suggestion in suggestions:
                print(f"- {suggestion}")

    def interactive_mode(self) -> None:
        """Run interactive query building session."""
        while True:
            print("\n" + "=" * 50)
            print("🔍 Beets Query Builder - Interactive Mode")
            print("=" * 50)

            query = self.build_interactive_query()

            if not query:
                print("Empty query. Exiting...")
                break

            print(f"\nGenerated query: {query}")
            self.query_history.append(query)

            # Analyze the query
            self.generate_query_report(query)

            # Ask to continue
            continue_session = input("\nBuild another query? (Y/n): ").strip().lower()
            if continue_session == 'n':
                break

    def validate_only_mode(self, query: str) -> None:
        """Validate and analyze a single query."""
        print(f"🔍 Analyzing query: {query}")
        print("=" * 40)

        self.generate_query_report(query)

def main():
    parser = argparse.ArgumentParser(description='Beets query builder and validator')
    parser.add_argument('query', nargs='?', help='Query to validate or analyze')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run interactive query builder')
    parser.add_argument('--validate', '-v', action='store_true',
                       help='Validate query syntax')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Test query execution')
    parser.add_argument('--optimize', '-o', action='store_true',
                       help='Optimize query and show suggestions')
    parser.add_argument('--examples', '-e', action='store_true',
                       help='Show example queries')
    parser.add_argument('--fields', '-f', action='store_true',
                       help='List available query fields')

    args = parser.parse_args()

    builder = BeetsQueryBuilder()

    if args.examples:
        builder.show_examples()
        return

    if args.fields:
        print("📋 Available Query Fields:")
        print("=" * 30)
        for category, fields in builder.query_fields.items():
            print(f"\n{category}:")
            for field in fields:
                print(f"  - {field}")
        return

    if args.interactive:
        builder.interactive_mode()
        return

    if args.query:
        if args.validate:
            is_valid, error = builder.validate_query_syntax(args.query)
            if is_valid:
                print("✅ Query syntax is valid")
                sys.exit(0)
            else:
                print(f"❌ Invalid query: {error}")
                sys.exit(1)

        if args.optimize:
            optimized, suggestions = builder.optimize_query(args.query)
            print(f"Original: {args.query}")
            print(f"Optimized: {optimized}")
            if suggestions:
                print("\nOptimization suggestions:")
                for suggestion in suggestions:
                    print(f"- {suggestion}")
            return

        if args.test:
            success, error, results = builder.test_query(args.query)
            if success:
                print(f"✅ Query executed successfully")
                print(f"Results: {len(results)} items")
                for result in results[:10]:  # Show first 10
                    print(f"  - {result['artist']} - {result['album']} - {result['title']}")
                if len(results) > 10:
                    print(f"  ... and {len(results) - 10} more")
            else:
                print(f"❌ Query failed: {error}")
                sys.exit(1)
            return

        # Default: full analysis
        builder.validate_only_mode(args.query)
    else:
        print("Please provide a query or use --interactive mode")
        parser.print_help()

if __name__ == '__main__':
    main()