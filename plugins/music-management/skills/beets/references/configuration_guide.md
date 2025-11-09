# Beets Configuration Guide

This comprehensive guide covers all aspects of beets configuration, from basic setup to advanced optimization.

## Configuration File Location

Beets configuration is stored in:
- **Linux/macOS**: `~/.config/beets/config.yaml`
- **Windows**: `%APPDATA%\beets\config.yaml`

## Basic Configuration Structure

```yaml
# Basic beets configuration
directory: ~/Music                    # Music library directory
library: ~/.config/beets/library.db   # Library database location

# Plugin configuration
plugins: fetchart lyrics lastgenre    # Enabled plugins

# Import settings
import:
    copy: true                        # Copy files to library
    write: true                       # Write metadata to files
    autotag: true                     # Automatic tagging
    quiet: false                      # Show import progress
    detail: false                     # Show detailed import info
    incremental: true                 # Skip already imported files
    log: ~/.config/beets/import.log   # Import log file

# Path format configuration
paths:
    default: $albumartist/$year - $album%aunique{}/$track - $title
    singleton: Singletons/$artist - $title
    comp: Compilations/$year - $album%aunique{}/$track - $title
```

## Directory and Library Settings

### Directory Configuration

```yaml
directory: /path/to/music/library     # Main music directory
library: /path/to/library.db         # Database file location

# Threaded operations
threaded: true                        # Enable threaded operations
librarythreads: 4                     # Number of threads for library operations

# Temporary directory
temp_directory: /tmp/beets            # Temporary file location
```

### Library Database Options

```yaml
# Database options
library:
    path: ~/.config/beets/library.db  # Database file path
    timeout: 30                       # Connection timeout (seconds)

# Performance settings
per_disc_numbering: false             # Track numbering per disc
original_date: true                   # Use original release date
id3v23: true                          # Use ID3v2.3 tags
```

## Import Configuration

### Basic Import Settings

```yaml
import:
    copy: true                        # Copy files to library
    move: false                       # Move files instead of copying
    write: true                       # Write metadata to files
    autotag: true                     # Automatic tagging
    detail: false                     # Show detailed import info
    quiet: false                      # Suppress output
    resume: false                     # Resume interrupted imports
    incremental: true                 # Skip already imported
    timid: false                      # Ask before making changes
    log: ~/.config/beets/import.log   # Log file path
    quiet_fallback: skip              # What to do in quiet mode on conflicts
    none_rec_action: ask              # Action for non-recognition
    duplicate_action: ask             # Action for duplicates
    delete: false                     # Delete original files
```

### Advanced Import Options

```yaml
import:
    # Clutter handling
    clutter: ['Thumbs.db', '.DS_Store', '*.tmp']

    # Filename parsing
    default_action: apply              # Default action for matches
    languages: en                     # Language for metadata

    # MusicBrainz settings
    musicbrainz:
        host: musicbrainz.org
        port: 443
        https: true

    # Autotagging thresholds
    strong_rec_thresh: 0.04           # Strong recommendation threshold
    medium_rec_thresh: 0.25           # Medium recommendation threshold
    rec_gap_thresh: 0.25              # Recommendation gap threshold
```

## Plugin Configuration

### Essential Plugins

```yaml
plugins:
    - fetchart                        # Album art fetching
    - lyrics                          # Lyrics fetching
    - lastgenre                       # Genre fetching
    - embedart                        # Embed album art
    - replaygain                      # ReplayGain calculation
    - scrub                           # Sensitive metadata removal
    - mbsync                          # MusicBrainz sync
```

### Plugin-Specific Configuration

#### Album Art (fetchart)

```yaml
fetchart:
    auto: true                        # Automatically fetch art
    minwidth: 500                     # Minimum image width
    maxwidth: 1200                    # Maximum image width
    quality: 2                        # Image quality (0-2)
    sources:                          # Art sources in order
        - filesystem
        - amazon
        - albumart
        - google
        - fanarttv
        - lastfm
    google_key: YOUR_API_KEY          # Google Images API key
    fanarttv_key: YOUR_API_KEY        # Fanart.tv API key
    enforce_ratio: false              # Enforce aspect ratio
    cover_names:                      # Recognized cover filenames
        - cover
        - front
        - art
        - album
        - folder
```

#### Lyrics

```yaml
lyrics:
    auto: true                        # Automatically fetch lyrics
    sources:                          # Lyrics sources
        - google
        - lyricwiki
        - musixmatch
        - genius
        - txtlyrics
    google_API_key: YOUR_API_KEY      # Google Custom Search API key
    genius_api_key: YOUR_API_KEY      # Genius API key
    fallback: false                   # Use built-in lyrics as fallback
    force: false                      # Force refetch existing lyrics
```

#### Genre (lastgenre)

```yaml
lastgenre:
    auto: true                        # Automatically fetch genres
    source: album                     # Source: album or track
    force: true                       # Overwrite existing genres
    min_weight: 10                    # Minimum genre weight
    count: 1                          # Number of genres to keep
    canonical: true                   # Use canonical genre tree
    whitelist: true                   # Use genre whitelist
    separator: ', '                   # Genre separator
    custom:
        - map:
            from: electronic
            to: 'electronic, techno'
```

#### ReplayGain

```yaml
replaygain:
    auto: true                        # Automatically calculate
    backend: bs1770gain               # Calculation backend
    targetlevel: 89                   # Target level in dB
    r128: false                       # Use EBU R128 standard
    albumgain: true                   # Calculate album gain
    trackgain: true                   # Calculate track gain
    overwrite: false                  # Overwrite existing values
```

#### Bad Files

```yaml
badfiles:
    check_on_import: true             # Check during import
    commands:                         # Validation commands
        mp3: ['mp3val', '-f']
        ogg: ['oggz-validate']
        flac: ['flac', '-t']
    warn_on_rename: true              # Warn when renaming bad files
```

## Path Format Configuration

### Basic Path Formats

```yaml
paths:
    default: $albumartist/$year - $album%aunique{}/$track - $title
    singleton: Singletons/$artist - $title
    comp: Compilations/$year - $album%aunique{}/$track - $title
```

### Advanced Path Formats with Template Functions

```yaml
paths:
    # Using template functions
    default: %upper{%left{$albumartist,1}}/$albumartist/$album%aunique{}/$track - $title

    # Conditional paths based on format
    default: $albumartist/$album [$format]/$track - $title
    comp: Compilations/$albumartist/$album [$format]/$track - $title

    # Organize by rating
    rating:5: Favorites/$albumartist/$album/$track - $title
    rating:4: Good/$albumartist/$album/$track - $title

    # Organize by custom fields
    mood:party: Party Music/$artist - $title
    mood:chill: Chill Music/$artist - $title
```

### Template Functions

Beets provides several template functions for path formatting:

- `%upper{text}`: Convert to uppercase
- `%lower{text}`: Convert to lowercase
- `%left{text,n}`: Left n characters
- `%right{text,n}`: Right n characters
- `%if{condition,true,false}`: Conditional logic
- `%first{list}`: First item from list
- `%aunique{}`: Unique album identifier
- `%time{format}`: Format timestamps

## Performance Configuration

### Threading and Performance

```yaml
# Threaded operations
threaded: true                        # Enable threading globally
librarythreads: 4                     # Library operation threads
importthreads: 4                      # Import operation threads

# Database optimization
timeout: 30                           # Database timeout
max_recursion: 1000                   # Maximum recursion depth

# Memory settings
import_copy: true                     # Copy during import
import_write: true                    # Write during import
```

### Caching and Optimization

```yaml
# Image caching
art_filename: cover                   # Default art filename
store_originals: false                # Store original art

# Path format caching
path_formats_separator: /             # Path separator

# Import optimization
import_autofetch: true                # Auto-fetch metadata
import_write: true                   # Write metadata immediately
```

## Web Interface Configuration

```yaml
web:
    host: 127.0.0.1                   # Web interface host
    port: 8337                        # Web interface port
    reverse_proxy: false              # Behind reverse proxy
    cors: '*'                         # CORS settings
    cors_origins: '*'                 # Allowed origins
```

## Match Configuration

### MusicBrainz Matching

```yaml
match:
    strong_rec_thresh: 0.04           # Strong match threshold
    medium_rec_thresh: 0.25           # Medium match threshold
    rec_gap_thresh: 0.25              # Gap threshold

    # Track matching
    track_length_grace: 10            # Track length grace period (seconds)
    track_length_max: 30              # Maximum track length difference

    # Preferred countries
    country_priorities:
        - US
        - GB
        - DE
        - JP

    # Media format preferences
    media_priorities:
        - CD
        - Digital Media
        - Vinyl
```

### Artist Credits

```yaml
artist_credit:
    normalize: true                   # Normalize artist names
    fallback: true                    # Use fallback artists

    # Name handling
    strip_diacritics: false           # Keep diacritics
    ascii: false                      # Use ASCII only
```

## Format-Specific Configuration

### MP3 Configuration

```yaml
# MP3 settings
id3v23: true                          # Use ID3v2.3
id3v1: false                         # Don't write ID3v1

# MP3 encoding
mp3_enc:
    vbr: true                         # Variable bitrate
    quality: 2                        # Quality setting (0-9)
```

### FLAC Configuration

```yaml
# FLAC settings
flac_enc:
    compression: 8                    # Compression level (0-8)
    verify: true                      # Verify after encoding
```

## Custom Fields Configuration

### Adding Custom Fields

```yaml
# Define custom fields
item_fields:
    mood:                             # Custom mood field
    rating:                           # Rating field
    play_count:                       # Play count field

album_fields:
    average_rating:                   # Album rating
    total_plays:                      # Total plays

# Field calculations
album_fields:
    average_bitrate: |
        total = 0
        count = 0
        for item in items:
            if item.bitrate:
                total += int(item.bitrate)
                count += 1
        return total / count if count > 0 else 0
```

## Environment-Specific Configurations

### Development Configuration

```yaml
# Development settings
directory: ~/Music/Development
library: ~/dev/beets/library.db
threaded: false                      # Disable threading for debugging
import:
    detail: true                      # Show detailed output
    timid: true                       # Ask before changes
```

### Production Configuration

```yaml
# Production settings
directory: /music/library
library: /var/lib/beets/library.db
threaded: true
librarythreads: 8
import:
    incremental: true
    autotag: true
    write: true
    quiet: false
    log: /var/log/beets/import.log
```

### Server Configuration

```yaml
# Server/headless settings
directory: /srv/music
library: /srv/lib/beets/library.db
threaded: true
librarythreads: 16
import:
    incremental: true
    autotag: true
    copy: true
    write: true
    quiet: true
    log: /var/log/beets/import.log
```

## Configuration Validation

### Testing Configuration

Test your configuration with:

```bash
# Check syntax
beet config -p

# Test plugins
beet plugins

# Test library access
beet list -f '$artist' | head -5
```

### Common Configuration Issues

1. **YAML Syntax**: Ensure proper indentation and quoting
2. **Plugin Loading**: Verify plugins are installed and enabled
3. **Path Permissions**: Check directory permissions
4. **Database Location**: Ensure database directory exists
5. **Thread Count**: Don't exceed CPU core count significantly

## Configuration Migration

### Upgrading Configuration

When upgrading beets versions:

1. **Backup current config**: `cp config.yaml config.yaml.backup`
2. **Check release notes**: Look for breaking changes
3. **Test new config**: Use `beet config -p` to validate
4. **Gradual migration**: Apply changes incrementally
5. **Backup library**: Create library backup before major changes

### Migrating from Other Tools

Common migration scenarios:

```yaml
# iTunes migration
paths:
    default: $albumartist/$album/$track $title

# Directory-based migration
import:
    copy: true                        # Copy to maintain structure
    write: true                       # Update metadata
    autotag: true                     # Match with MusicBrainz
```

This configuration guide provides comprehensive coverage of beets configuration options. Adjust settings based on your specific needs and workflow requirements.