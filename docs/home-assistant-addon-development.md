# Developing Home Assistant Add-ons

A comprehensive guide to creating, building, and publishing Home Assistant add-ons.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Add-on Structure](#addon-structure)
- [Configuration Files](#configuration-files)
- [Building Add-ons](#building-add-ons)
- [Testing Add-ons](#testing-addons)
- [Publishing Add-ons](#publishing-addons)
- [Security Best Practices](#security-best-practices)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)
- [Examples and Templates](#examples-and-templates)

## Overview

Home Assistant add-ons are containerized applications that extend the functionality of your Home Assistant installation. They run in isolated Docker containers managed by the Home Assistant Supervisor and can provide services like network tools, media servers, system monitoring, and custom integrations.

### Key Features

- **Containerized Security**: Each add-on runs in its own isolated Docker container
- **Easy Management**: Install, configure, and manage through the Home Assistant UI
- **Automatic Updates**: Built-in update mechanism with version control
- **Resource Control**: Fine-grained control over system resources and permissions
- **API Integration**: Direct access to Home Assistant APIs and services

## Prerequisites

Before you start developing Home Assistant add-ons, ensure you have:

1. **Docker**: Installed and running on your development machine
2. **Home Assistant Instance**: For testing (can be a local development instance)
3. **Git**: For version control and repository management
4. **Basic Knowledge**:
   - Docker containerization concepts
   - YAML configuration
   - Shell scripting (Bash)
   - Basic programming concepts

### Development Environment Setup

```bash
# Install Docker (Ubuntu/Debian example)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Clone the official example repository
git clone https://github.com/hassio-addons/addon-example.git my-addon
cd my-addon
```

## Addon Structure

A Home Assistant add-on follows a specific directory structure:

```
my-addon/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions for CI/CD
├── rootfs/
│   ├── etc/
│   │   └── cont-init.d/        # Initialization scripts
│   ├── usr/
│   │   └── bin/                # Application binaries
│   └── s6-rc.d/                # Service definitions
│       ├── init-example/       # Initialization service
│       └── example1/           # Main application service
├── CHANGELOG.md                # Version history
├── DOCS.md                     # Add-on documentation
├── LICENSE                     # License file
├── README.md                   # Project README
├── apparmor.txt               # AppArmor security profile (optional)
├── build.yaml                 # Build configuration
├── config.yaml                # Main add-on configuration
└── Dockerfile                 # Container build instructions
```

### Key Files Explained

- **`config.yaml`**: Main configuration file defining add-on metadata, options, and permissions
- **`Dockerfile`**: Container build instructions
- **`build.yaml`**: Build-time configuration for different architectures
- **`rootfs/`**: Filesystem overlay that gets copied into the container
- **`s6-rc.d/`**: Service management configuration using s6-overlay

## Configuration Files

### config.yaml

The main configuration file defines your add-on's metadata, user options, and system permissions:

```yaml
---
name: "My Awesome Add-on"
version: "1.0.0"
slug: "my-awesome-addon"
description: "A comprehensive description of what this add-on does"
url: "https://github.com/yourusername/your-repo"
codenotary: "your-email@example.com"
init: false
arch:
  - aarch64
  - amd64
  - armhf
  - armv7
  - i386
ports:
  8080/tcp: null
ports_description:
  8080/tcp: "Web interface port"
map:
  - "share"
  - "ssl"
options:
  log_level: "info"
  enable_feature: true
  custom_port: 8080
schema:
  log_level: "list(trace|debug|info|notice|warning|error|fatal)"
  enable_feature: "bool"
  custom_port: "int(1,65535)"
startup: "application"
boot: "auto"
```

### build.yaml

Defines build-time configuration for different architectures:

```yaml
---
build_from:
  aarch64: "ghcr.io/home-assistant/aarch64-base:latest"
  amd64: "ghcr.io/home-assistant/amd64-base:latest"
  armhf: "ghcr.io/home-assistant/armhf-base:latest"
  armv7: "ghcr.io/home-assistant/armv7-base:latest"
  i386: "ghcr.io/home-assistant/i386-base:latest"
codenotary:
  base_image: "your-email@example.com"
  signer: "your-email@example.com"
args:
  SOME_BUILD_ARG: "value"
```

### Dockerfile

Standard Dockerfile with required labels:

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment variables
ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    && pip3 install --no-cache-dir \
        requests \
        beautifulsoup4

# Copy application files
COPY rootfs /

# Install Python requirements if any
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Build arguments for metadata
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Required labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.version="${BUILD_VERSION}" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}"
```

## Building Add-ons

### Local Development Build

Build your add-on locally using the official builder:

```bash
# Build for all architectures
docker run \
  --rm \
  -it \
  --name builder \
  --privileged \
  -v /path/to/your/addon:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  ghcr.io/home-assistant/amd64-builder \
  -t /data \
  --all \
  --test \
  -i my-test-addon-{arch} \
  -d local
```

### Standalone Docker Build

Build without the official builder for quick testing:

```bash
# Build for current architecture only
docker build \
  --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base:latest" \
  --build-arg BUILD_ARCH="amd64" \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg BUILD_NAME="My Add-on" \
  --build-arg BUILD_DESCRIPTION="Test add-on" \
  --build-arg BUILD_VERSION="1.0.0" \
  -t local/my-test-addon \
  .
```

### GitHub Actions CI/CD

Set up automated builds with GitHub Actions:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * 0"

jobs:
  build:
    name: Build add-on
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [aarch64, amd64, armhf, armv7, i386]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build add-on
        uses: home-assistant/builder@master
        with:
          args: |
            --${{ matrix.arch }} \
            --test \
            --target /data \
            --docker-hub "yourusername"
```

## Testing Add-ons

### Local Testing

Test your add-on locally before publishing:

```bash
# Run the built image
docker run \
  --rm \
  -v /tmp/my_test_data:/data \
  -p 8080:8080 \
  local/my-test-addon

# Run with environment variables
docker run \
  --rm \
  -e TZ="America/New_York" \
  -v /tmp/my_test_data:/data \
  local/my-test-addon
```

### Testing with Home Assistant

1. **Add your repository** to Home Assistant:
   - Go to Settings → Add-ons → Add-on Store
   - Click the three-dot menu → Repositories
   - Add your GitHub repository URL

2. **Install your add-on**:
   - Find your add-on in the store
   - Click Install

3. **Configure and test**:
   - Set configuration options
   - Start the add-on
   - Check logs for errors

### Configuration Validation

Test your configuration schema:

```bash
# Validate config.yaml with Home Assistant's schema
ha addons validate /path/to/your/addon
```

## Publishing Add-ons

### Repository Structure

For publishing, you need a properly structured repository:

```
addons-repository/
├── .github/
│   └── workflows/
│       └── ci.yml
├── addons/
│   ├── my-first-addon/
│   │   ├── config.yaml
│   │   ├── Dockerfile
│   │   ├── build.yaml
│   │   └── rootfs/
│   └── my-second-addon/
│       ├── config.yaml
│       └── ...
├── repository.yaml
└── README.md
```

### repository.yaml

Root configuration file for your add-on repository:

```yaml
---
name: "My Awesome Add-on Repository"
url: "https://github.com/yourusername/addons"
maintainer: "Your Name <your-email@example.com>"
```

### Publishing Process

1. **Tag your release**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically**:
   - Build for all architectures
   - Push images to Docker Hub
   - Update repository files

3. **Add repository to Home Assistant**:
   - Users add your repository URL
   - Your add-ons appear in the store

## Security Best Practices

### Security Ratings

Home Assistant assigns security ratings based on configuration:

| Feature | Score Impact |
|---------|-------------|
| Ingress enabled | +2 |
| Custom AppArmor profile | +1 |
| CodeNotary signature | +1 |
| Host PID access | -2 |
| Host network access | -1 |
| Full system access | -2 |

### Recommended Security Settings

```yaml
# Avoid host network unless absolutely necessary
host_network: false

# Enable AppArmor for additional security
apparmor: true

# Use read-only mappings when possible
map:
  - type: share
    read_only: true
  - type: ssl
    read_only: true

# Limit permissions to minimum required
hassio_role: "default"  # Use "admin" only if necessary
privileged: []

# Use specific ports instead of host networking
ports:
  8080/tcp: null
```

### AppArmor Profile

Create a custom AppArmor profile for enhanced security:

```bash
# apparmor.txt
#include <tunables/global>

profile your-addon flags (attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Allow network access if needed
  network inet tcp,
  network inet udp,

  # Allow read access to specific files
  /data/** rw,
  /tmp/** rw,

  # Deny access to sensitive system files
  deny /etc/shadow r,
  deny /etc/passwd r,
  deny /proc/** r,
}
```

### CodeNotary Signing

Sign your add-on for additional security:

```yaml
# In config.yaml
codenotary: "your-email@example.com"

# In build.yaml
codenotary:
  base_image: "your-email@example.com"
  signer: "your-email@example.com"
```

## API Integration

### Home Assistant API Access

Enable access to Home Assistant APIs:

```yaml
# In config.yaml
homeassistant_api: true  # Access to Home Assistant API
hassio_api: true        # Access to Supervisor API
auth_api: true          # Access to authentication API
hassio_role: "manager"  # Permission level
```

### Using Bashio

Bashio provides helper functions for interacting with Home Assistant:

```bash
#!/command/with-contenv bashio

# Read configuration values
log_level=$(bashio::config 'log_level')
enable_feature=$(bashio::config 'enable_feature')

# Check if value exists
if bashio::config.has_value 'custom_port'; then
    port=$(bashio::config 'custom_port')
else
    port=8080
fi

# Logging
bashio::log.info "Starting add-on with log level: ${log_level}"
bashio::log.warning "This is a warning"
bashio::log.error "An error occurred"

# Make API calls to Home Assistant
token=$(bashio::config 'homeassistant_token')
response=$(curl -s -H "Authorization: Bearer ${token}" \
    http://supervisor/core/api/states)

# Service calls
bashio::homeassistant.service_call "light.turn_on" \
    '{"entity_id": "light.living_room"}'

# Get system information
ha_version=$(bashio::supervisor.version)
cpu_arch=$(bashio::info.cpu_arch)
```

### Ingress Integration

Enable web interface access through Home Assistant:

```yaml
# In config.yaml
ingress: true
ingress_port: 8080
ingress_entry: "/"
panel_icon: "mdi:puzzle"
panel_title: "My Add-on"
panel_admin: false
```

Access user information in your application:

```bash
# Read ingress headers for user identification
user_id=$(bashio::header 'X-Remote-User-Id')
user_name=$(bashio::header 'X-Remote-User-Name')
display_name=$(bashio::header 'X-Remote-User-Display-Name')
```

## Troubleshooting

### Common Issues

#### 1. Build Failures

**Problem**: Docker build fails during package installation

**Solution**:
- Check base image compatibility
- Verify package names are correct for your base OS
- Use specific package versions if needed

```bash
# Debug by building interactively
docker run -it --entrypoint /bin/bash ghcr.io/home-assistant/amd64-base:latest
```

#### 2. Permission Issues

**Problem**: Add-on can't access required files or directories

**Solution**:
- Check volume mappings in config.yaml
- Verify read/write permissions
- Use `host_pid: true` only if absolutely necessary

#### 3. Network Access Problems

**Problem**: Add-on can't connect to external services

**Solution**:
- Check DNS resolution in container
- Verify firewall settings
- Consider using `host_network: true` as last resort

#### 4. Memory/CPU Issues

**Problem**: Add-on crashes or becomes unresponsive

**Solution**:
- Monitor resource usage in Home Assistant
- Optimize application code
- Consider resource limits in config.yaml

### Debugging Techniques

#### 1. Container Inspection

```bash
# Check container logs
docker logs container_name

# Enter running container
docker exec -it container_name /bin/bash

# Inspect container configuration
docker inspect container_name
```

#### 2. Add-on Logging

Use bashio logging for better debugging:

```bash
# Enable debug logging
if bashio::config.exists 'log_level' && \
   [[ "$(bashio::config 'log_level')" == "debug" ]]; then
    set -x
    bashio::log.debug "Debug mode enabled"
fi
```

#### 3. Configuration Validation

```bash
# Validate your config.yaml
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Test with Home Assistant
ha addons validate /path/to/addon
```

#### 4. Network Debugging

```bash
# Test network connectivity from container
docker run --rm --network host alpine ping -c 4 google.com

# Check DNS resolution
docker run --rm --network host alpine nslookup google.com
```

## Examples and Templates

### Simple Web Service Add-on

```yaml
# config.yaml
name: "Simple Web Server"
version: "1.0.0"
slug: "simple-web"
description: "A simple HTTP server add-on"
arch:
  - amd64
  - aarch64
ports:
  8080/tcp: 8080
options:
  port: 8080
  message: "Hello World!"
schema:
  port: "int(1,65535)"
  message: "str"
```

```dockerfile
# Dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nginx

COPY rootfs /
```

```bash
# rootfs/etc/s6-overlay/s6-rc.d/nginx/run
#!/command/with-contenv bashio

# Generate nginx configuration
port=$(bashio::config 'port')
message=$(bashio::config 'message')

cat > /etc/nginx/http.d/default.conf << EOF
server {
    listen ${port};
    location / {
        return 200 "${message}";
        add_header Content-Type text/plain;
    }
}
EOF

exec nginx -g "daemon off;"
```

### Home Assistant Integration Add-on

```yaml
# config.yaml
name: "HA Integration Example"
version: "1.0.0"
slug: "ha-integration"
description: "Example add-on with Home Assistant integration"
homeassistant_api: true
hassio_api: true
arch:
  - amd64
  - aarch64
options:
  update_interval: 30
schema:
  update_interval: "int(5,300)"
```

```bash
# rootfs/usr/bin/app.sh
#!/command/with-contenv bashio

interval=$(bashio::config 'update_interval')

while true; do
    # Get system info
    cpu_temp=$(bashio::info.cpu_temperature)

    # Send sensor data to Home Assistant
    if [ -n "$cpu_temp" ]; then
        bashio::homeassistant.service_call "sensor.create" \
            "{
                \"state\": \"${cpu_temp}\",
                \"attributes\": {
                    \"unit_of_measurement\": \"°C\",
                    \"friendly_name\": \"CPU Temperature\"
                }
            }"
    fi

    sleep "${interval}"
done
```

### Database Add-on

```yaml
# config.yaml
name: "SQLite Database"
version: "1.0.0"
slug: "sqlite-db"
description: "SQLite database add-on with web interface"
arch:
  - amd64
  - aarch64
map:
  - "share"
ports:
  8080/tcp: 8080
ingress: true
ingress_port: 8080
options:
  database_path: "/share/my-database.db"
schema:
  database_path: "str"
```

```dockerfile
# Dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    sqlite \
    python3 \
    py3-pip \
    && pip3 install --no-cache-dir \
        flask \
        sqlite-web

COPY rootfs /
```

## Resources and References

- [Official Home Assistant Add-on Documentation](https://developers.home-assistant/docs/add-ons/)
- [Community Add-on Repository](https://github.com/hassio-addons/repository)
- [Add-on Example](https://github.com/hassio-addons/addon-example)
- [Home Assistant Community Forums](https://community.home-assistant.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Bashio Documentation](https://github.com/hassio-addons/bashio)

## Contributing

This guide is maintained by the community. Please contribute improvements and corrections by:

1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

For specific questions about add-on development, visit the [Home Assistant Developer Discord](https://www.home-assistant.io/join-developers/) or the [community forums](https://community.home-assistant.io/).