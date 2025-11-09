---
name: beets
description: Use PROACTIVELY for comprehensive music library management system guidance covering setup, advanced querying, plugin development, and automation workflows for the beets music organization tool. MUST BE USED when working with music collections, metadata management, library organization, or extending beets functionality through plugins and automation.
---

# Beets Music Library Management

## Overview

This skill provides comprehensive guidance for working with beets, the powerful music library management system and MusicBrainz tagger. It covers everything from initial library setup to advanced automation workflows, enabling efficient music collection management with precise metadata handling and organizational control.

## Quick Start & Setup

### Installation and Initial Configuration

Install beets using the system package manager:

```bash
# macOS
brew install beets

# Ubuntu/Debian
sudo apt-get install beets

# Python pip
pip install beets
```

### Configuration Setup

Generate initial configuration:

```bash
beet config -e
```

Use the `scripts/setup_beets.py` script to generate optimized configurations:

```bash
python3 scripts/setup_beets.py --template audiophile --interactive
```

### First Import Workflow

For guided first import:

```bash
python3 scripts/import_helper.py --guided-import /path/to/music
```

## Core Workflows

### Music Import Strategies

#### Automated Import with Metadata Fetching

Enable essential plugins for automatic metadata enrichment:

```yaml
plugins: fetchart lyrics lastgenre embedart
```

Run unattended import with logging:

```yaml
import:
    incremental: yes
    quiet: yes
    log: /path/to/import.log
    autotag: yes
    copy: yes
    write: yes
```

#### Attachment Handling

Import with additional file types as attachments:

```bash
beet import --attachments=jpg,cue,log /path/to/music
```

### Path Format Configuration

#### Basic Organization Structure

Standard artist/album organization:

```yaml
paths:
    default: $albumartist/$year - $album%aunique{}/$track - $title
    singleton: Singletons/$artist - $title
    comp: Compilations/$year - $album%aunique{}/$track - $title
```

#### Advanced Organization with Custom Fields

Organize based on custom attributes like mood or rating:

```yaml
paths:
    default: $albumartist/$year - $album%aunique{}/$track - $title
    mood:party: Party Music/$artist - $title
    rating:5: Five Star/$artist - $title
```

Use template functions for dynamic organization:

```yaml
paths:
    default: %upper{%left{$albumartist,1}}/$albumartist/$album%aunique{}/$track - $title
```

## Advanced Operations

### Complex Querying and Searching

#### Query Syntax Examples

Find music by specific attributes:

```bash
# Find tracks by bitrate
beet list bitrate:320000

# List albums with custom formatting
beet ls -f '$bitrate $artist - $title' bitrate+

# Query by custom attributes
beet ls mood:sunny
beet ls -f '$title: $mood'

# Complex queries with multiple criteria
beet list artist:Beatles year:1965..1969 genre:Rock
```

#### Interactive Query Building

Use the query builder for complex searches:

```bash
python3 scripts/query_builder.py --interactive
```

Validate and optimize queries:

```bash
python3 scripts/query_builder.py --validate "artist:Beatles year:1965..1969"
```

### Metadata Management

#### Flexible Attributes

Add custom metadata fields:

```bash
beet modify context:mope
beet modify mood=party artist:'beastie boys'
beet modify bad=1 christmas
```

Define album fields with Python calculations:

```yaml
album_fields:
    bitrate: |
        total = 0
        for item in items:
            total += item.bitrate
        return total / len(items)
```

#### Batch Metadata Operations

Validate metadata consistency:

```bash
python3 scripts/metadata_validator.py --check-all
```

Perform batch modifications:

```bash
python3 scripts/metadata_validator.py --batch-modify "genre:Electronic genre:Techno"
```

### Library Maintenance

#### Duplicate Detection and Resolution

Find and manage duplicates:

```bash
python3 scripts/library_maintenance.py --duplicates --auto-resolve
```

#### Library Consistency Checks

Run comprehensive library validation:

```bash
python3 scripts/library_maintenance.py --full-check
```

## Plugin Development

### Plugin Structure and Templates

Generate new plugin templates:

```bash
python3 scripts/plugin_generator.py --name myplugin --type metadata
```

Add event listeners:

```bash
python3 scripts/plugin_generator.py --add-event --event album_imported
```

### Custom Template Functions

Create custom path format functions:

```python
class MyPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.template_funcs["initial"] = _tmpl_initial

def _tmpl_initial(text: str) -> str:
    if text:
        return text[0].upper()
    else:
        return ""
```

### Plugin Configuration Patterns

Configure plugin-specific settings:

```yaml
fetchart:
    auto: yes
    minwidth: 500
    maxwidth: 1200
    sources: filesystem amazon albumart google fanarttv

lyrics:
    auto: yes
    sources: google lyricwikia musixmatch

lastgenre:
    auto: yes
    source: album
    force: yes
```

## Automation and Integration

### Scripting Common Workflows

#### Automated Import Processing

```bash
# Process incoming music directory
python3 scripts/import_helper.py --watch /incoming/music --auto-import

# Convert and optimize for portable devices
beet convert -d portable -k format:mp3 bitrate:192000 artist:"Led Zeppelin"
```

#### Scheduled Maintenance

```bash
# Weekly library maintenance
python3 scripts/library_maintenance.py --scheduled --cleanup

# Monthly metadata refresh
beet update -f
beet fetchart
beet lyrics
```

### External Tool Integration

#### Audio Quality Analysis

Integrate with audio analysis tools:

```bash
# Check audio quality using badfiles plugin
beet badfiles

# Generate quality reports
python3 scripts/metadata_validator.py --quality-report
```

#### Cloud Service Integration

Sync with cloud storage services using beets web interface:

```yaml
web:
    host: 127.0.0.1
    port: 8337
    reverse_proxy: yes
    cors: '*'
```

## Configuration Templates

Use configuration templates from `assets/config_templates/`:

- **basic_config.yaml**: Simple setup for beginners
- **advanced_config.yaml**: Power user configuration
- **dj_config.yaml**: DJ workflow optimization
- **audiophile_config.yaml**: High-quality audio management

## Resources

### scripts/

**Core automation and management scripts:**

- `setup_beets.py`: Configuration generator and setup wizard
- `import_helper.py`: Guided import workflow and batch processing
- `query_builder.py`: Interactive query building and validation
- `metadata_validator.py`: Metadata consistency and quality checks
- `plugin_generator.py`: Plugin template and scaffolding tools
- `library_maintenance.py`: Library health checks and maintenance

### references/

**Comprehensive documentation and guides:**

- `configuration_guide.md`: Complete configuration options and patterns
- `path_formats.md`: Advanced path format syntax and examples
- `query_syntax.md`: Query language reference and optimization
- `plugin_development.md`: Plugin architecture and API documentation
- `common_workflows.md`: Step-by-step workflow guides
- `troubleshooting.md`: Common issues and solutions
- `api_reference.md`: Python API documentation

### assets/

**Templates and examples:**

- `config_templates/`: Pre-configured setups for different use cases
- `plugin_templates/`: Boilerplate plugin code and patterns
- `examples/`: Real-world usage examples and case studies

## Troubleshooting

### Common Issues and Solutions

1. **Import Problems**: Use `scripts/import_helper.py --diagnose` to identify configuration issues
2. **Metadata Inconsistency**: Run `scripts/metadata_validator.py --fix-issues`
3. **Plugin Conflicts**: Check `references/troubleshooting.md` for common plugin conflicts
4. **Performance Issues**: Use `scripts/library_maintenance.py --optimize`

### Performance Optimization

- Optimize database with `beet update --reset`
- Use `scripts/library_maintenance.py --vacuum` for database maintenance
- Configure `librarythreads` and `threaded` options for better performance

## Best Practices

1. **Regular Backups**: Back up `library.db` and configuration files
2. **Testing**: Use `scripts/setup_beets.py --test-config` before applying changes
3. **Incremental Imports**: Always use incremental mode for safety
4. **Metadata Validation**: Regular validation prevents corruption
5. **Plugin Management**: Enable only necessary plugins for performance

Use this skill whenever working with music libraries, metadata management, or extending beets functionality through custom automation and plugins.