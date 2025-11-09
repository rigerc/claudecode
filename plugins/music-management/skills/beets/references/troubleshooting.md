# Beets Troubleshooting Guide

This comprehensive guide covers common beets issues, their solutions, and preventive measures to keep your music library running smoothly.

## Installation and Setup Issues

### Beets Installation Problems

#### Issue: Beets command not found

```bash
# Error
bash: beet: command not found

# Solutions:

# 1. Check if beets is installed
python -c "import beets; print('Beets is installed')"

# 2. Install beets
pip install beets

# 3. Check Python path
which python
which pip
echo $PATH

# 4. Install with user directory
pip install --user beets
export PATH=$PATH:~/.local/bin
```

#### Issue: Permission denied during installation

```bash
# Error
PermissionError: [Errno 13] Permission denied

# Solutions:

# 1. Use user installation
pip install --user beets

# 2. Use virtual environment
python -m venv beets-env
source beets-env/bin/activate
pip install beets

# 3. Use system package manager
# macOS
brew install beets

# Ubuntu/Debian
sudo apt-get install beets
```

#### Issue: Missing dependencies

```bash
# Error
ImportError: No module named 'mutagen'

# Solutions:

# 1. Install with all dependencies
pip install beets[mediafile,requests]

# 2. Install specific dependencies
pip install mutagen python-mpd2

# 3. Install audio format libraries
# Ubuntu/Debian
sudo apt-get install python3-mutagen libmagic1

# macOS
brew install libmagic
```

## Configuration Issues

### Configuration File Problems

#### Issue: Invalid YAML syntax

```bash
# Error
yaml.scanner.ScannerError: mapping values are not allowed here

# Common causes and solutions:

# 1. Indentation errors (YAML requires spaces, not tabs)
# WRONG:
paths:
  default: $albumartist/$album/$title
    comp: Compilations/$album/$title  # Extra indentation

# CORRECT:
paths:
  default: $albumartist/$album/$title
  comp: Compilations/$album/$title

# 2. Unquoted special characters
# WRONG:
directory: C:\Music\Library  # Backslashes need quotes

# CORRECT:
directory: "C:\\Music\\Library"
# or
directory: C:/Music/Library

# 3. Missing colons
# WRONG:
directory ~/Music

# CORRECT:
directory: ~/Music
```

#### Issue: Plugin not found

```bash
# Error
PluginNotFoundError: No plugin named 'fetchart'

# Solutions:

# 1. Install the plugin
pip install beets[fetchart]

# 2. Install all common plugins
pip install beets[plugins]

# 3. Check plugin spelling in config
# Check config.yaml
plugins: [fetchart, lyrics, lastgenre]  # Correct spelling

# 4. Verify plugin is available
beet plugins
```

#### Issue: Database connection failed

```bash
# Error
DatabaseError: unable to open database file

# Solutions:

# 1. Check directory permissions
ls -la ~/.config/beets/
mkdir -p ~/.config/beets

# 2. Check database file path
# In config.yaml
library: ~/.config/beets/library.db

# 3. Create directory if it doesn't exist
mkdir -p ~/.config/beets

# 4. Check file permissions
chmod 644 ~/.config/beets/library.db
```

## Import Issues

### Import Failures

#### Issue: No matches found during import

```bash
# Error
No match found for: /path/to/music/track.mp3

# Solutions:

# 1. Check MusicBrainz availability
ping musicbrainz.org

# 2. Use manual search during import
beet import /path/to/music
# When prompted, use 's' for search

# 3. Relax matching criteria
# In config.yaml
match:
    strong_rec_thresh: 0.10  # Lower threshold
    medium_rec_thresh: 0.30  # Lower threshold

# 4. Use ASIN from Amazon
beet import --asin /path/to/music

# 5. Skip autotagging and import as-is
beet import --noautotag /path/to/music
```

#### Issue: Duplicate detection during import

```bash
# Error
Item already imported: /path/to/track.mp3

# Solutions:

# 1. Skip duplicates
beet import --copy /path/to/music

# 2. Use incremental mode
# In config.yaml
import:
    incremental: true

# 3. Remove from library first
beet remove -y "path:/path/to/track.mp3"

# 4. Import with different metadata
beet import --set genre=Live /path/to/music
```

#### Issue: Permission denied during import

```bash
# Error
PermissionError: [Errno 13] Permission denied

# Solutions:

# 1. Check source directory permissions
ls -la /path/to/music/
chmod -R 755 /path/to/music/

# 2. Check destination directory permissions
ls -la ~/Music/
chmod -R 755 ~/Music/

# 3. Use different user or sudo (not recommended)
sudo beet import /path/to/music

# 4. Change music directory ownership
sudo chown -R $USER:$USER ~/Music/
```

## Metadata Issues

### Tagging Problems

#### Issue: Incorrect metadata after import

```bash
# Solutions:

# 1. Manual metadata correction
beet modify artist="Correct Artist" album="Correct Album" track:5

# 2. Reimport with different search terms
beet import --search "Correct Artist Correct Album" /path/to/music

# 3. Use MusicBrainz ID directly
beet modify mb_trackid="xxxxx-xxxx" track.mp3

# 4. Reset and reimport
beet remove -y "artist:Wrong Artist"
beet import /path/to/original/music
```

#### Issue: Special characters in metadata

```bash
# Problems with: AC/DC, Björk, etc.

# Solutions:

# 1. Use quotes in queries
beet list artist:"AC/DC"

# 2. Escape characters in config
paths:
  default: $artist/$album/$title  # Should handle most cases

# 3. Check encoding
# In config.yaml
import:
    from_scratch: true

# 4. Manual correction
beet modify artist="AC/DC" artist:"ACDC"
```

#### Issue: Album art not embedding

```bash
# Solutions:

# 1. Enable embedart plugin
plugins: [embedart]

# 2. Configure fetchart
fetchart:
    auto: true
    minwidth: 500
    maxwidth: 1200

# 3. Manual album art fetch
beet fetchart

# 4. Embed existing art
beet embedart

# 5. Check image format compatibility
# Supported: JPEG, PNG, GIF
```

## Performance Issues

### Slow Operations

#### Issue: Slow imports

```bash
# Solutions:

# 1. Enable threading
# In config.yaml
threaded: true
librarythreads: 4

# 2. Reduce detail during import
import:
    detail: false
    quiet: true

# 3. Use incremental imports
import:
    incremental: true

# 4. Optimize database
beet modify --yes --nodb dummy:true
```

#### Issue: Slow library operations

```bash
# Solutions:

# 1. Vacuum database
sqlite3 ~/.config/beets/library.db "VACUUM;"

# 2. Rebuild statistics
beet stats

# 3. Check database size
du -h ~/.config/beets/library.db

# 4. Optimize configuration
librarythreads: 8  # Increase for SSD
```

#### Issue: Memory usage problems

```bash
# Solutions:

# 1. Limit concurrent operations
librarythreads: 2

# 2. Process in smaller batches
beet import /path/to/music/small-chunk

# 3. Close other applications
# Free up system memory

# 4. Check for memory leaks
# Monitor with htop or Activity Monitor
```

## File System Issues

### Path and File Problems

#### Issue: Paths too long

```bash
# Error: File name too long

# Solutions:

# 1. Use shorter path formats
paths:
  default: %upper{%left{$artist,1}}/$album/$track $title

# 2. Truncate long titles
paths:
  default: $artist/$album/%left{$title,50}/$track $title

# 3. Remove problematic characters
paths:
  default: %substitute{$artist,/,_}/%substitute{$album,/,_}/$track $title
```

#### Issue: Missing files in library

```bash
# Solutions:

# 1. Find missing files
beet list -f '$path' | xargs ls -la 2>&1 | grep "No such file"

# 2. Remove missing items from library
beet update --reset

# 3. Check for moved files
find ~/Music -name "*.mp3" -exec beet import -L {} \;

# 4. Re-link moved files
beet modify path="new/path/to/file.mp3" "title:Track Title"
```

#### Issue: Case sensitivity problems

```bash
# On case-sensitive filesystems (Linux)

# Solutions:

# 1. Use consistent case in path formats
paths:
  default: $artist/$album/$track $title  # Use original case

# 2. Normalize case in queries
beet list -i artist:beatles  # Case-insensitive search

# 3. Check actual file case
ls -la ~/Music/beatles/  # Might be "Beatles"
```

## Plugin Issues

### Plugin-Specific Problems

#### Issue: Fetchart not working

```bash
# Solutions:

# 1. Check internet connection
ping google.com

# 2. Configure API keys
fetchart:
    google_key: YOUR_GOOGLE_API_KEY
    fanarttv_key: YOUR_FANARTTV_API_KEY

# 3. Try different sources
fetchart:
    sources: [filesystem, amazon, albumart]

# 4. Manual fetch
beet fetchart --force artist:"The Beatles" album:"Abbey Road"
```

#### Issue: Lyrics plugin not finding lyrics

```bash
# Solutions:

# 1. Check plugin configuration
lyrics:
    sources: [google, lyricwiki, musixmatch]

# 2. Try manual fetch
beet lyrics artist:"The Beatles" title:"Yesterday"

# 3. Check if lyrics exist in sources
# Try searching manually first

# 4. Use different sources
lyrics:
    sources: [genius, azlyrics, musixmatch]
```

#### Issue: ReplayGain errors

```bash
# Error: bs1770gain not found

# Solutions:

# 1. Install required tools
# Ubuntu/Debian
sudo apt-get install bs1770gain

# macOS
brew install bs1770gain

# 2. Use different backend
replaygain:
    backend: ffmpeg  # Or 'loudgain', 'bs1770gain'

# 3. Skip ReplayGain temporarily
# Remove 'replaygain' from plugins list
```

## Database Issues

### Corruption and Recovery

#### Issue: Database corruption

```bash
# Symptoms: Crashes, strange query results

# Solutions:

# 1. Backup current database
cp ~/.config/beets/library.db ~/.config/beets/library.db.backup

# 2. Check database integrity
sqlite3 ~/.config/beets/library.db "PRAGMA integrity_check;"

# 3. Rebuild from files
beet import --resume --quiet ~/Music/

# 4. Start fresh (last resort)
mv ~/.config/beets/library.db ~/.config/beets/library.db.corrupt
beet import ~/Music/
```

#### Issue: Database locked

```bash
# Error: database is locked

# Solutions:

# 1. Check for running processes
ps aux | grep beet

# 2. Kill hanging processes
pkill -f beet

# 3. Remove lock files
rm -f ~/.config/beets/library.db.lock

# 4. Wait and retry
# Sometimes locks clear automatically
```

## Network Issues

### MusicBrainz and Online Services

#### Issue: MusicBrainz connection timeout

```bash
# Solutions:

# 1. Check internet connection
ping musicbrainz.org

# 2. Use mirror or configure timeout
match:
    musicbrainz:
        host: musicbrainz.org
        port: 443
        timeout: 30

# 3. Reduce concurrent requests
import:
    threads: 1

# 4. Work offline temporarily
beet import --noautotag /path/to/music
```

#### Issue: Album art sources not working

```bash
# Solutions:

# 1. Check source availability
curl -I https://albumart.com

# 2. Configure alternative sources
fetchart:
    sources: [filesystem, amazon, google]

# 3. Use local art only
fetchart:
    sources: [filesystem]

# 4. Manual art management
# Copy cover.jpg to album folders manually
```

## Prevention and Maintenance

### Regular Maintenance Tasks

```bash
# 1. Weekly backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp ~/.config/beets/library.db ~/.config/beets/backups/library_$DATE.db

# 2. Monthly consistency check
beet update --reset
beet list missing:genre
beet list missing:year

# 3. Quarterly cleanup
beet duplicates
beet badfiles

# 4. Annual optimization
sqlite3 ~/.config/beets/library.db "VACUUM;"
beet stats
```

### Monitoring and Health Checks

```bash
# 1. Library size monitoring
du -sh ~/Music/
beet stats

# 2. Database health check
sqlite3 ~/.config/beets/library.db "PRAGMA integrity_check;"

# 3. Missing files check
beet list -f '$path' | while read path; do
    if [ ! -f "$path" ]; then
        echo "Missing: $path"
    fi
done

# 4. Duplicate monitoring
beet duplicates | wc -l
```

### Configuration Backup

```bash
# Backup complete beets configuration
#!/bin/bash
BACKUP_DIR="$HOME/beets_backup_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

cp -r ~/.config/beets "$BACKUP_DIR/"
cp -r ~/Music "$BACKUP_DIR/"  # If space allows

echo "Backup created: $BACKUP_DIR"
```

## Getting Help

### Community Resources

1. **Official Documentation**: https://beets.readthedocs.io/
2. **GitHub Issues**: https://github.com/beetbox/beets/issues
3. **MusicBrainz Community**: https://community.metabrainz.org/
4. **Reddit**: r/beetsmusic

### Debug Information Collection

```bash
# Collect system information for bug reports
echo "=== Beets Version ==="
beet version

echo "=== Python Version ==="
python --version

echo "=== Configuration ==="
beet config -p

echo "=== Plugins ==="
beet plugins

echo "=== Database Info ==="
sqlite3 ~/.config/beets/library.db "SELECT count(*) FROM items;"

echo "=== System Info ==="
uname -a
```

### When to Report Issues

Report issues when:
1. You've tried all relevant solutions above
2. The issue is reproducible
3. You have specific error messages
4. You can provide debug information

Include in your report:
- Beets version
- Operating system
- Configuration (sanitized)
- Exact error messages
- Steps to reproduce

This troubleshooting guide covers the most common beets issues. Regular maintenance and proper configuration can prevent many of these problems.