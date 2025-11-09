# Beets Query Syntax Reference

This comprehensive guide covers beets query syntax for searching and filtering your music library.

## Query Basics

Beets queries allow you to search and filter your music library using a powerful query language. Queries can be used with commands like `beet list`, `beet modify`, and `beet remove`.

### Basic Query Structure

```
field:value query_text
```

**Examples:**
```bash
beet list artist:Beatles           # Find all Beatles tracks
beet list "Yesterday"              # Find tracks with "Yesterday" in any field
beet list year:1965                # Find tracks from 1965
```

## Field Queries

### Standard Fields

#### Artist and Album Queries

```bash
# Artist searches
artist:Beatles                     # Exact match
artist:Beatles OR artist:Stones    # Multiple artists
artist!:"The Beatles"              # Not The Beatles

# Album searches
album:"Abbey Road"                 # Exact album title
album:Road                         # Contains "Road"
albumartist:Various Artists        # Album artist

# Combined searches
artist:Beatles album:"Abbey Road"  # Specific album by specific artist
```

#### Title and Track Queries

```bash
# Title searches
title:Yesterday                    # Exact title match
title:"Day Tripper"                # Exact match with spaces
title:love                         # Contains "love"

# Track number queries
track:1                            # Track number 1
track:1..5                         # Tracks 1 through 5
track>10                           # Track numbers greater than 10
track>=10                          # Track numbers 10 and above
```

#### Year and Date Queries

```bash
# Year searches
year:1969                          # Exact year
year:1960..1969                    # Range of years
year>=1980                         # 1980 and later
year<1970                          # Before 1970

# Combined with other fields
artist:Beatles year:1965..1969     # Beatles tracks from 1965-1969
```

#### Genre Queries

```bash
# Genre searches
genre:Rock                         # Rock genre
genre:"Classic Rock"               # Exact genre match
genre:Rock OR genre:Pop            # Multiple genres
genre!:"Hip Hop"                   # Not Hip Hop
```

#### Technical Field Queries

```bash
# Format queries
format:MP3                         # MP3 files only
format:FLAC                        # FLAC files only
format:MP3 OR format:FLAC          # Multiple formats

# Bitrate queries
bitrate:320000                     # Exactly 320kbps
bitrate:320000..                    # 320kbps and above
bitrate:192000..320000             # 192-320kbps range
bitrate<128000                     # Low bitrate files

# Length queries
length:180                         # Exactly 3 minutes
length:120..240                    # 2-4 minutes
length>300                         # Longer than 5 minutes
```

### Special Query Types

#### Missing Field Queries

```bash
# Find items with missing metadata
missing:genre                      # No genre set
missing:year                       # No year set
missing:album                      # No album set
missing:artwork                    # No album art
missing:lyrics                     # No lyrics

# Multiple missing fields
missing:genre OR missing:year      # Missing genre OR year
```

#### Singleton and Compilation Queries

```bash
# Singletons (tracks not part of albums)
singleton:true                     # Only singletons
singleton:false                    # Only album tracks

# Compilations
comp:true                          # Compilation albums
comp:false                         # Non-compilation albums
```

#### Duplicate Queries

```bash
# Find duplicate items
dup:true                           # All duplicates
artist:Beatles dup:true            # Duplicate Beatles tracks
album:"Abbey Road" dup:true        # Duplicate Abbey Road tracks
```

#### Path Queries

```bash
# Path-based searches
path:Beatles                       # Files in Beatle directories
path:/music/beatles                # Specific path pattern
path:*.flac                        # FLAC files
```

## Query Operators

### Comparison Operators

```bash
# Numeric comparisons
year:>=1980                        # 1980 or later
bitrate:>320000                    # Greater than 320kbps
track:<5                           # Less than track 5
length:>=180                       # 3 minutes or longer

# Text comparisons (case-insensitive)
artist:=Beatles                    # Case-sensitive exact match
artist:!=Beatles                   # Not equal to Beatles
```

### Range Operators

```bash
# Inclusive ranges
year:1960..1969                    # 1960s (inclusive)
bitrate:192000..320000             # 192-320kbps range
track:1..12                        # Tracks 1 through 12

# Open-ended ranges
year:1980..                        # 1980 and later
year:..1970                        # 1970 and earlier
```

### Logical Operators

```bash
# AND (implicit, space-separated)
artist:Beatles year:1969           # Beatles tracks from 1969

# OR
artist:Beatles OR artist:Stones    # Beatles or Stones

# NOT
genre:Rock artist!:"The Beatles"   # Rock but not Beatles

# Complex logic
(artist:Beatles OR artist:Stones) year:1965..1970
```

### Wildcard and Pattern Matching

```bash
# Wildcard searches
artist:Beat*                       # Starts with "Beat"
title:*Love                         # Ends with "Love"
title:*Day*                         # Contains "Day"

# Regular expressions (in some contexts)
artist:/^The Beatles$/             # Exact match using regex
title:/Yesterday|Hey Jude/         # Multiple titles
```

## Complex Query Examples

### Musical Era Queries

```bash
# 1960s Rock
genre:Rock year:1960..1969

# Classic Rock era
year:1970..1985 genre:(Rock OR "Classic Rock")

# Jazz classics
genre:Jazz year:1950..1965
```

### Quality-Based Queries

```bash
# High-quality audio
format:FLAC OR bitrate:>=320000

# Lossless audio
format:FLAC OR format:ALAC

# Low-quality files (for cleanup)
bitrate:<128000 OR format:MP3 bitrate:<192000
```

### Organization Queries

```bash
# Files needing metadata
missing:genre OR missing:year OR missing:album

# Duplicate detection
dup:true

# Various Artists compilations
albumartist:"Various Artists" OR comp:true

# Singletons (loose tracks)
singleton:true
```

### Custom Field Queries

```bash
# Rating-based queries
rating:5                            # 5-star tracks
rating:4..5                         # 4-5 star tracks
rating:                             # Unrated tracks

# Mood-based queries
mood:party                          # Party music
mood:chill OR mood:relax           # Chill/relaxing music

# Play count queries
play_count:>10                      # Frequently played
play_count:0                        # Never played
```

## Advanced Query Techniques

### Query Optimization

```bash
# More specific queries are faster
artist:Beatles album:"Abbey Road"   # Specific = fast
artist:Beatles                      # Less specific = slower

# Use indexes when possible
year:1969                           # Indexed field = fast
title:"Something"                   # Text search = slower
```

### Nested Queries

```bash
# Parentheses for grouping
(artist:Beatles OR artist:Stones) AND year:1965..1970

# Complex logic
(genre:Rock OR genre:Pop) AND year:1980..1989 AND bitrate:>=192000
```

### Query Chaining

```bash
# Multiple criteria with different operators
artist:Beatles year:1965..1969 format:FLAC

# Combine with negative queries
genre:Rock artist!:"The Beatles" year:1970..1979
```

## Query Shortcuts and Aliases

### Common Query Patterns

```bash
# Recently added (if you have an 'added' field)
added:>2023-12-01                   # Added after December 1, 2023
added:>30d                          # Added in last 30 days

# Favorite tracks
rating:5 OR play_count:>20          # 5-star or frequently played

# Problem files
missing:genre OR missing:year OR bitrate:<128000
```

### Query Templates

Save common queries as shell aliases:

```bash
# In .bashrc or .zshrc
alias beet-60s='beet list year:1960..1969'
alias beet-high-quality='beet list format:FLAC OR bitrate:>=320000'
alias beet-duplicates='beet list dup:true'
alias beet-needs-metadata='beet list missing:genre OR missing:year'
```

## Query Performance Tips

### Efficient Query Construction

1. **Be specific**: Use multiple fields to narrow results
2. **Use ranges**: Range queries are faster than text searches
3. **Avoid wildcards**: Leading wildcards are slow
4. **Use indexed fields**: Year, format, bitrate are indexed
5. **Limit results**: Use `head` or limit commands for large libraries

### Performance Examples

```bash
# Fast (indexed fields)
beet list year:1969 format:FLAC

# Slower (text search)
beet list title:"Something"

# Fast (specific combination)
beet list artist:Beatles album:"Abbey Road"

# Slower (broad search)
beet list Beatles
```

## Query Results Formatting

### Custom Output Formats

```bash
# Basic format
beet list -f '$artist - $title' artist:Beatles

# Detailed format
beet list -f '$artist - $album ($year) - $title [$bitrate]' year:1969

# Tabular format
beet list -f '$artist\t$album\t$title\t$year' genre:Rock

# Path format
beet list -f '$path' format:FLAC
```

### Sorting Results

```bash
# Sort by year (newest first)
beet list -f '$year $artist - $title' year+

# Sort by bitrate (highest first)
beet list -f '$bitrate $artist - $title' bitrate+

# Multi-field sorting
beet list -f '$artist $year $album' artist year+

# Reverse sorting
beet list -f '$year $artist - $title' year-
```

## Special Query Cases

### Unicode and Special Characters

```bash
# Unicode searches work naturally
artist:Björk                        # Works with Unicode characters
artist:"Daft Punk"                  # Handles spaces in names

# Escape special characters if needed
artist:"AC/DC"                      # Use quotes for special characters
```

### Case Sensitivity

```bash
# Most queries are case-insensitive
artist:beatles                      # Same as artist:Beatles
artist:BEATLES                      # Same as artist:Beatles

# Use := for case-sensitive exact matches
artist:="The Beatles"               # Exact case match
```

## Troubleshooting Queries

### Common Query Issues

1. **No results found**: Check spelling and field names
2. **Too many results**: Add more specific criteria
3. **Slow queries**: Be more specific or use indexed fields
4. **Syntax errors**: Check operator placement and quotes

### Query Debugging

```bash
# Test query components separately
beet list artist:Beatles            # Test artist part
beet list year:1969                 # Test year part

# Use simple queries first
beet list Beatles                    # Simple text search
beet list artist:Beatles            # More specific

# Check field names
beet list -f '$artist' | head -5    # Verify artist field exists
```

## Integration with Scripts

### Using Queries in Scripts

```bash
#!/bin/bash
# Find and process high-quality files
beet list format:FLAC OR bitrate:>=320000 | while read line; do
    echo "Processing: $line"
    # Your processing logic here
done
```

### Python Integration

```python
import subprocess

def run_beets_query(query):
    cmd = ['beet', 'list', '-f', '$artist|$album|$title', query]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        items = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                artist, album, title = line.split('|', 2)
                items.append({'artist': artist, 'album': album, 'title': title})
        return items
    return []

# Usage
beatles_tracks = run_beets_query('artist:Beatles')
```

This query syntax reference provides comprehensive coverage of beets query capabilities. Use these patterns to efficiently search and manage your music library.