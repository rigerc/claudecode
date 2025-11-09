# Beets Path Formats Reference

This comprehensive guide covers beets path format syntax, template functions, and organizational patterns for structuring your music library.

## Path Format Basics

Path formats determine how beets organizes your music files on disk. They use a template language with field names and functions.

### Basic Syntax

```yaml
paths:
    default: $albumartist/$year - $album%aunique{}/$track - $title
```

**Components:**
- `$field`: Access metadata fields
- `%function{arg}`: Apply template functions
- `text`: Literal text
- `/`: Directory separator

### Available Fields

#### Standard Fields
- `$artist`: Track artist
- `$albumartist`: Album artist (may differ from track artist)
- `$album`: Album name
- `$title`: Track title
- `$year`: Release year
- `$month`: Release month
- `$day`: Release day
- `$track`: Track number
- `$tracktotal`: Total tracks
- `$disc`: Disc number
- `$disctotal`: Total discs
- `$genre`: Genre
- `$lyrics`: Lyrics content
- `$comments`: Comments
- `$bpm`: Beats per minute
- `$comp`: Compilation flag
- `$mb_trackid`: MusicBrainz track ID
- `$mb_albumid`: MusicBrainz album ID
- `$mb_artistid`: MusicBrainz artist ID

#### Technical Fields
- `$format`: Audio format (MP3, FLAC, etc.)
- `$bitrate`: Bitrate in bps
- `$length`: Track length in seconds
- `$size`: File size in bytes
- `$mtime`: Modification time
- `$added`: Date added to library

#### Path Fields
- `$path`: Original file path
- `$dirname`: Original directory name
- `$extension`: File extension

#### Flexible Fields
Any custom fields you've defined can be used with `$field_name`.

## Template Functions

### Text Manipulation

```yaml
# Uppercase conversion
%upper{$artist}                       # "THE BEATLES"

# Lowercase conversion
%lower{$album}                        # "abbey road"

# Leftmost characters
%left{$albumartist,1}                 # "B" for "Beatles"

# Rightmost characters
%right{$title,3}                      # "day" for "Yesterday"

# Article handling
%the{$artist}                         # "Beatles, The" for "The Beatles"
```

### Conditional Functions

```yaml
# Conditional logic
%if{$comp,Compilations,Artists}       # Use "Compilations" if compilation

# Nested conditions
%if{$year,$year,Unknown Year}         # Show year or "Unknown Year"

# Field presence check
%ifdef{$genre,$genre,Unknown}         # Show genre or "Unknown"
```

### Date/Time Functions

```yaml
# Date formatting
%time{$added,%Y-%m-%d}                # "2023-12-25"

# Time formatting
%time{$length,%M:%S}                  # "03:45"

# Year extraction
%time{$added,%Y}                      # "2023"
```

### Unique Identifiers

```yaml
# Album uniqueness
%aunique{}                            # Unique album identifier

# Singleton uniqueness
%sunique{}                            # Unique singleton identifier

# With custom format
%aunique{/albumartist album year}     # Custom uniqueness criteria
```

### Advanced Functions

```yaml
# String substitution
%substitute{$artist,/,_}               # Replace "/" with "_"

# First item from list
%first{$genre}                        # First genre from multi-genre

# Range bucketing
%bucket{$year,1960,1970,1980,1990,2000} # Year range buckets
```

## Path Format Examples

### Basic Organization

#### Simple Artist/Album Structure

```yaml
paths:
    default: $albumartist/$album/$track $title
    singleton: $artist/$title
    comp: Compilations/$album/$track $title
```

#### Year-Based Organization

```yaml
paths:
    default: $albumartist/$year - $album/$track $title
    singleton: $artist/$year $title
    comp: Compilations/$year - $album/$track $title
```

#### Numeric Track Organization

```yaml
paths:
    default: $albumartist/$album/$tracktotal - $track - $title
    singleton: Singletons/$artist - $title
```

### Advanced Organization

#### Format-Based Organization

```yaml
paths:
    default: $albumartist/$album [$format]/$track $title
    singleton: $artist/$title [$format]
    comp: Compilations/$album [$format]/$track $title
```

#### Quality-Based Organization

```yaml
paths:
    # High-quality audio
    bitrate:320000: $albumartist/$album [FLAC]/$track $title
    bitrate:192000: $albumartist/$album [HQ]/$track $title

    # Standard quality
    default: $albumartist/$album/$track $title

    # Low quality
    bitrate:128000: $albumartist/$album [LQ]/$track $title
```

#### Custom Field Organization

```yaml
paths:
    # Rating-based organization
    rating:5: 5★/$albumartist/$album/$track $title
    rating:4: 4★/$albumartist/$album/$track $title
    rating:3: 3★/$albumartist/$album/$track $title
    default: Unrated/$albumartist/$album/$track $title
```

#### Mood-Based Organization

```yaml
paths:
    mood:party: Party Music/$artist - $title
    mood:chill: Chill Music/$artist - $title
    mood:workout: Workout/$artist - $title
    mood:sleep: Sleep/$artist - $title
    default: Other/$artist - $title
```

### Complex Multi-Level Organization

#### Genre First, Then Artist

```yaml
paths:
    default: $genre/$albumartist/$year - $album%aunique{}/$track $title
    comp: Compilations/$genre/$year - $album%aunique{}/$track $title
    singleton: $genre/$artist/$title
```

#### Decade-Based Organization

```yaml
paths:
    default: %bucket{$year,1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020}/$albumartist/$album/$track $title
    comp: %bucket{$year,1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020}/Compilations/$album/$track $title
```

#### Alphabetical Organization

```yaml
paths:
    default: %upper{%left{$albumartist,1}}/$albumartist/$album/$track $title
    comp: Compilations/%upper{%left{$album,1}}/$album/$track $title
    singleton: Singletons/%upper{%left{$artist,1}}/$artist/$title
```

## Special Path Types

### Album Path Formats

Album path formats use the `paths:` configuration section and apply to full albums.

```yaml
paths:
    # Standard album format
    default: $albumartist/$album/$track $title

    # Various artists compilations
    comp: Compilations/$album/$track $title

    # Soundtracks
    album:soundtrack: Soundtracks/$album/$track $title

    # Live albums
    album:live: Live/$albumartist/$album/$track $title
```

### Singleton Path Formats

Singletons (individual tracks not part of albums) can have separate paths.

```yaml
paths:
    singleton: Singletons/$artist/$title

    # Or organize by artist
    singleton: $artist/Non-Album/$title

    # Or by year
    singleton: Singletons/$year/$artist - $title
```

### Conditional Path Formats

Use field conditions for different path formats:

```yaml
paths:
    # Lossless audio
    format:FLAC: $albumartist/$album [FLAC]/$track $title
    format:ALAC: $albumartist/$album [ALAC]/$track $title

    # High-quality lossy
    bitrate:320000: $albumartist/$album [320]/$track $title
    bitrate:256000: $albumartist/$album [256]/$track $title

    # Standard quality
    default: $albumartist/$album/$track $title

    # Compilations
    comp: Compilations/$album/$track $title
```

## Advanced Template Techniques

### Multi-Field Organization

```yaml
paths:
    # Combine artist and year
    default: $albumartist [$year]/$album/$track $title

    # Include genre for better organization
    default: $genre/$albumartist/$year - $album/$track $title

    # Include both bitrate and format
    default: $albumartist/$album [$format $bitrate]/$track $title
```

### Dynamic Path Components

```yaml
paths:
    # Use artist initial for organization
    default: %upper{%left{$albumartist,1}}/$albumartist/$album/$track $title

    # Clean up problematic characters
    default: %substitute{$albumartist,/,_}/%substitute{$album,/,_}/$track $title

    # Handle Various Artists specially
    comp: Compilations/$album/$track $title
    albumartist:Various Artists: Compilations/$album/$track $title
```

### Template Function Chaining

```yaml
paths:
    # Multiple function applications
    default: %upper{%left{$albumartist,1}}/%lower{$album}/$track $title

    # Conditional with functions
    default: %if{$comp,Compilations,%upper{%left{$albumartist,1}}}/$album/$track $title

    # Date-based organization with formatting
    default: $albumartist/%time{$added,%Y}/$album/$track $title
```

## Migration Strategies

### From Simple Structures

If migrating from a simple artist/album structure:

```yaml
# Before: Artist/Album/Track Title
# After: Artist/Year - Album/Track Title

paths:
    default: $albumartist/$year - $album/$track $title
```

### Adding Format Information

To add format information to existing paths:

```yaml
# Before: Artist/Album/Track Title
# After: Artist/Album [Format]/Track Title

paths:
    default: $albumartist/$album [$format]/$track $title
```

### From iTunes Structure

iTunes typically uses: Music/Artist/Album/Track Title

```yaml
paths:
    default: $albumartist/$album/$track $title
    comp: Compilations/$album/$track $title
```

## Special Characters and Safety

### Handling Problematic Characters

```yaml
# Replace problematic characters
paths:
    default: %substitute{$albumartist,/,_}/%substitute{$album,/,_}/$track $title

# Remove or replace colons
paths:
    default: %substitute{$album,:, }/$album/$track $title
```

### Path Length Considerations

Be aware of filesystem path length limits:

```yaml
# Truncate long titles
paths:
    default: $albumartist/$album/%left{$title,50}/$track $title

# Use abbreviations for long artist names
paths:
    default: %left{$albumartist,20}/$album/$track $title
```

## Testing Path Formats

### Testing New Path Formats

1. **Test with dry run**:
   ```bash
   beet import -n --copy /path/to/music
   ```

2. **Check specific items**:
   ```bash
   beet move -p -f '$albumartist/$album/$track $title' artist:Beatles
   ```

3. **Validate paths**:
   ```bash
   beet list -f '$path' | head -10
   ```

### Path Format Debugging

Use template function to debug:

```yaml
# Test template functions
beet list -f '%upper{%left{$artist,1}}' | head -5

# Test conditional logic
beet list -f '%if{$comp,Compilation,Album}' | head -5
```

## Best Practices

### Path Format Design Principles

1. **Consistency**: Use consistent patterns across your library
2. **Readability**: Make paths human-readable
3. **Sortability**: Ensure paths sort logically
4. **Uniqueness**: Avoid naming conflicts
5. **Compatibility**: Consider filesystem limitations

### Recommended Practices

```yaml
# Good: Includes year for sorting
default: $albumartist/$year - $album/$track $title

# Good: Handles compilations separately
comp: Compilations/$year - $album/$track $title

# Good: Uses uniqueness for duplicate albums
default: $albumartist/$year - $album%aunique{}/$track $title

# Good: Organizes by format when needed
format:FLAC: $albumartist/$album [FLAC]/$track $title
```

### Avoid These Patterns

```yaml
# Avoid: Too deep nesting
default: $genre/$albumartist/$year/$album/$disc/$track $title

# Avoid: Non-sorting formats
default: $title - $artist  # Won't sort by artist

# Avoid: Special characters that cause issues
default: $artist/$album?/($year)/$track $title
```

This path formats reference provides comprehensive guidance for organizing your beets music library effectively. Choose patterns that match your workflow and filesystem requirements.