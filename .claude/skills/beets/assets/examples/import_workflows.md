# Beets Import Workflows Examples

This document provides practical examples of common import workflows for different scenarios.

## Beginner Import Workflow

### Scenario: First-time user with existing music collection

```bash
# 1. Initial setup
python3 scripts/setup_beets.py --template basic --interactive

# 2. Test import with small batch
mkdir ~/Music/Import
cp /path/to/small/album/* ~/Music/Import/
python3 scripts/import_helper.py --guided-import ~/Music/Import

# 3. Review results
beet list -f '$artist - $album - $title' | head -10

# 4. Continue with full collection
python3 scripts/import_helper.py --guided-import /path/to/entire/collection
```

### Configuration for Beginners

```yaml
# ~/.config/beets/config.yaml
directory: ~/Music
library: ~/.config/beets/library.db

plugins:
  - fetchart
  - lyrics
  - lastgenre

import:
  copy: true
  write: true
  autotag: true
  quiet: false
  detail: false
  incremental: true

paths:
  default: $albumartist/$album/$track $title
  singleton: $artist/$title
  comp: Compilations/$album/$track $title
```

## Power User Import Workflow

### Scenario: Large, organized collection with specific requirements

```bash
# 1. Advanced setup
python3 scripts/setup_beets.py --template audiophile

# 2. Pre-import validation
python3 scripts/import_helper.py --diagnose
python3 scripts/query_builder.py --validate "format:FLAC OR bitrate:>=320000"

# 3. Batch import by quality
# High quality first
beet import --quiet --copy --write ~/Music/To_Import/FLAC/
beet import --quiet --copy --write ~/Music/To_Import/HighQuality/

# 4. Metadata validation
python3 scripts/metadata_validator.py --check-all

# 5. Duplicate detection
python3 scripts/library_maintenance.py --duplicates
```

### Advanced Configuration

```yaml
directory: ~/Music
library: ~/.config/beets/library.db

plugins:
  - fetchart
  - lyrics
  - lastgenre
  - embedart
  - badfiles
  - replaygain

import:
  copy: true
  write: true
  autotag: true
  quiet: false
  detail: true
  incremental: true
  log: ~/.config/beets/import.log

paths:
  default: $albumartist/$year - $album [$format]/$track - $title
  singleton: Singletons/$artist/$title [$format]
  comp: Compilations/$year - $album [$format]/$track - $title
```

## DJ Import Workflow

### Scenario: DJ importing new music for performances

```bash
# 1. DJ-specific setup
python3 scripts/setup_beets.py --template dj

# 2. Import new releases
beet import --copy --write ~/Downloads/NewMusic/

# 3. BPM and key analysis
beet update  # Trigger BPM/key detection

# 4. Organize by tempo
beet list bpm:>120 --format '$artist - $title - $bpm BPM' > high_tempo_tracks.txt

# 5. Key detection for harmonic mixing
beet list key:C --format '$artist - $title - $key' > c_major_tracks.txt
```

### DJ Configuration

```yaml
directory: ~/DJ Music
library: ~/.config/beets/dj_library.db

plugins:
  - fetchart
  - bpm
  - key
  - lastgenre

import:
  copy: true
  write: true
  autotag: true

paths:
  default: $genre/$albumartist/$album/$track - $artist - $title
  singleton: $genre/$artist - $title

bpm:
  auto: true

key:
  auto: true
```

## Metadata Cleanup Workflow

### Scenario: Cleaning up messy metadata from various sources

```bash
# 1. Import with loose matching
beet import --noautotag --copy ~/Music/MessyCollection/

# 2. Validate and fix issues
python3 scripts/metadata_validator.py --check-all
python3 scripts/metadata_validator.py --fix-issues

# 3. Batch metadata fixes
beet modify genre="Unknown" "genre:!"
beet modify year=2023 "year:!"

# 4. Re-tag with MusicBrainz
beet import --copy --write ~/Music/MessyCollection/

# 5. Quality report
python3 scripts/metadata_validator.py --quality-report
```

## Incremental Import Workflow

### Scenario: Regularly adding new music to existing library

```bash
# 1. Watch directory setup
mkdir ~/Music/Incoming
python3 scripts/import_helper.py --watch ~/Music/Incoming --auto-import

# 2. Manual weekly import
beet import --copy --write ~/Downloads/NewMusic/

# 3. Update metadata
beet update
beet fetchart
beet lyrics

# 4. Library maintenance
python3 scripts/library_maintenance.py --full-check
```

### Automated Script

```bash
#!/bin/bash
# weekly_import.sh

echo "Starting weekly music import..."

# Import from downloads
if [ -d ~/Downloads/NewMusic ]; then
    beet import --copy --write ~/Downloads/NewMusic/
    rm -rf ~/Downloads/NewMusic/*
fi

# Update metadata
beet update
beet fetchart

# Library maintenance
~/.config/beets/scripts/library_maintenance.py --optimize

echo "Weekly import complete"
```

## Format Conversion Workflow

### Scenario: Converting to uniform format for devices

```bash
# 1. Import original files
beet import --copy ~/Music/Sources/

# 2. Convert to target format
beet convert -d ~/Music/Portable/ -k format:mp3 bitrate:320000

# 3. Verify conversion
beet list -f '$format $bitrate $path' format:MP3 | head -10

# 4. Update portable device
rsync -av ~/Music/Portable/ /media/PLAYER/Music/
```

## Classical Music Workflow

### Scenario: Organizing classical music with composer and work information

```bash
# 1. Classical-specific import
beet import --copy ~/Classical/NewAdditions/

# 2. Add composer information
beet modify composer="Bach" "album:Bach*"

# 3. Organize by composer
beet modify path="Classical/$composer/$work/$movement" genre:Classical

# 4. Custom path format
# In config.yaml:
# paths:
#   genre:Classical: Classical/$composer/$year $album/$disc $track $title
```

## Podcast Import Workflow

### Scenario: Managing podcast collections with beets

```bash
# 1. Import podcasts as singles
beet import --singleton --copy ~/Podcasts/Downloads/

# 2. Tag with podcast information
beet modify genre=Podcast album="Podcast Name" artist="Episode Title"

# 3. Organize by date
beet modify path="Podcasts/$album/$year-$month-$day $title" genre:Podcast

# 4. Clean up old episodes
beet list genre:Podcast added:<90d  # Episodes older than 90 days
```

## Troubleshooting Import Issues

### Common Problems and Solutions

#### Problem: No matches found

```bash
# 1. Check internet connection
ping musicbrainz.org

# 2. Use manual search
beet import -s /path/to/problematic/files/

# 3. Relax matching criteria
# Add to config.yaml:
# match:
#   strong_rec_thresh: 0.10
#   medium_rec_thresh: 0.30
```

#### Problem: Import too slow

```bash
# 1. Enable threading
# In config.yaml:
# threaded: true
# librarythreads: 4

# 2. Import in smaller batches
beet import /path/to/small/subset/
beet import /path/to/another/subset/

# 3. Use quiet mode
beet import --quiet /path/to/music/
```

#### Problem: Duplicate imports

```bash
# 1. Enable incremental mode
# In config.yaml:
# import:
#   incremental: true

# 2. Remove duplicates first
beet duplicates
beet remove -y dup:true

# 3. Use copy instead of move
beet import --copy /path/to/music/
```

## Best Practices

### Before Importing

1. **Backup your library**: `cp ~/.config/beets/library.db ~/.config/beets/library.db.backup`
2. **Test configuration**: `beet config -p`
3. **Check plugins**: `beet plugins`
4. **Validate source files**: Ensure files are accessible and readable

### During Import

1. **Start small**: Test with a few albums first
2. **Use appropriate options**: Match options to your use case
3. **Monitor progress**: Watch for error messages
4. **Review results**: Check imported metadata

### After Import

1. **Validate results**: `python3 scripts/metadata_validator.py --check-all`
2. **Fetch missing data**: `beet fetchart && beet lyrics`
3. **Check for duplicates**: `python3 scripts/library_maintenance.py --duplicates`
4. **Backup again**: Save the updated library database

## Automation Examples

### Cron Job for Weekly Maintenance

```bash
# Add to crontab: crontab -e
# Weekly on Sunday at 2 AM
0 2 * * 0 /home/user/.config/beets/scripts/weekly_maintenance.sh

# weekly_maintenance.sh
#!/bin/bash
cd ~/.config/beets
python3 scripts/library_maintenance.py --full-check
python3 scripts/metadata_validator.py --quality-report
beet update
beet fetchart
```

### Systemd Service for Auto-Import

```ini
# ~/.config/systemd/user/beets-auto-import.service
[Unit]
Description=Beets Auto-Import Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/user/.config/beets/scripts/import_helper.py --watch /home/user/Music/Incoming --auto-import
Restart=always
RestartSec=30

[Install]
WantedBy=default.target
```

These workflow examples provide practical guidance for different use cases. Adapt them to your specific needs and preferences.