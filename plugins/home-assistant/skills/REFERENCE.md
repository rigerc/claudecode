# Home Assistant Add-on Development Reference

## Common Commands

### Building and Testing
```bash
# Build for all architectures with official builder
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

# Build for current architecture only
docker build \
  --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base:latest" \
  -t local/my-test-addon \
  .

# Run the built image for testing
docker run \
  --rm \
  -v /tmp/my_test_data:/data \
  -p 8080:8080 \
  local/my-test-addon
```

### Configuration Validation
```bash
# Validate add-on configuration
ha addons validate /path/to/your/addon

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
yamllint config.yaml
```

### Debugging
```bash
# View container logs
docker logs container_name

# Enter running container for debugging
docker exec -it container_name /bin/bash

# Inspect container configuration
docker inspect container_name

# Check resource usage
docker stats container_name
```

## Security Rating System

| Configuration | Score Impact | Recommendation |
|---------------|--------------|----------------|
| Ingress enabled | +2 | Enable for web interfaces |
| Custom AppArmor | +1 | Add for enhanced security |
| CodeNotary signature | +1 | Sign all production images |
| Host PID access | -2 | Avoid unless absolutely necessary |
| Host network access | -1 | Use port mapping instead |
| Full system access | -2 | Use minimum required permissions |

## Architecture Support

| Architecture | Docker Tag | Typical Use |
|--------------|------------|-------------|
| amd64 | `ghcr.io/home-assistant/amd64-base` | Standard x86_64 systems |
| aarch64 | `ghcr.io/home-assistant/aarch64-base` | ARM 64-bit (RPi 4+, modern ARM) |
| armhf | `ghcr.io/home-assistant/armhf-base` | ARM 32-bit hard float (RPi 2/3) |
| armv7 | `ghcr.io/home-assistant/armv7-base` | ARM v7 (older 32-bit ARM) |
| i386 | `ghcr.io/home-assistant/i386-base` | Legacy 32-bit x86 |

## Common Configuration Patterns

### Basic Web Service
```yaml
name: "Web Service"
version: "1.0.0"
slug: "web-service"
ports:
  8080/tcp: 8080
options:
  port: 8080
schema:
  port: "int(1,65535)"
```

### Database Service
```yaml
name: "Database Service"
version: "1.0.0"
slug: "database"
map:
  - "share"
options:
  database_path: "/share/data.db"
schema:
  database_path: "str"
```

### Home Assistant Integration
```yaml
name: "HA Integration"
version: "1.0.0"
slug: "ha-integration"
homeassistant_api: true
hassio_api: true
auth_api: true
hassio_role: "manager"
```

### API-Only Service
```yaml
name: "API Service"
version: "1.0.0"
slug: "api-service"
ingress: true
ingress_port: 8080
ingress_entry: "/"
panel_icon: "mdi:puzzle"
panel_title: "My API Service"
```

## Bashio API Reference

### Configuration Access
```bash
# Read configuration value
value=$(bashio::config 'option_name')

# Check if option exists
if bashio::config.has_value 'option_name'; then
    # Option is set
fi

# Read nested values
nested=$(bashio::config 'parent.child')
```

### Logging
```bash
bashio::log.trace "Detailed trace message"
bashio::log.debug "Debug information"
bashio::log.info "General information"
bashio::log.notice "Notable event"
bashio::log.warning "Warning message"
bashio::log.error "Error occurred"
bashio::log.fatal "Critical failure"
```

### Home Assistant API
```bash
# Make service calls
bashio::homeassistant.service_call "light.turn_on" \
  '{"entity_id": "light.living_room"}'

# Get states
states=$(bashio::homeassistant.states)

# Get specific entity state
state=$(bashio::homeassistant.state "sensor.temperature")
```

### System Information
```bash
# Get Home Assistant version
version=$(bashio::supervisor.version)

# Get CPU architecture
arch=$(bashio::info.cpu_arch)

# Check if feature is available
if bashio::info.has_service "mqtt"; then
    # MQTT is available
fi
```

## Troubleshooting Common Issues

### Build Failures
1. **Package not found**: Check base image compatibility
2. **Permission denied**: Verify Docker is running and user has access
3. **Out of space**: Clean up Docker images and containers
4. **Network issues**: Check internet connectivity and Docker daemon

### Runtime Issues
1. **Container exits immediately**: Check entrypoint and service scripts
2. **Permission denied**: Review volume mappings and file permissions
3. **Network not working**: Verify port configuration and firewall rules
4. **API access denied**: Check Home Assistant API permissions in config.yaml

### Configuration Issues
1. **Invalid YAML**: Use YAML linter to validate syntax
2. **Schema validation fails**: Check options match schema definitions
3. **Missing required fields**: Verify all required config.yaml fields are present
4. **Architecture not supported**: Check build.yaml and available architectures

## Development Workflow

1. **Setup**: Install Docker, create development directory
2. **Structure**: Follow official directory structure with rootfs/, config.yaml, etc.
3. **Configure**: Set up config.yaml, build.yaml, and Dockerfile
4. **Implement**: Add service logic in rootfs/s6-rc.d/
5. **Test**: Build locally, run container, test functionality
6. **Validate**: Use ha addons validate and manual testing
7. **Publish**: Set up repository, CI/CD, and release process

## Resources

- [Official Add-on Documentation](https://developers.home-assistant/docs/add-ons/)
- [Community Add-on Repository](https://github.com/hassio-addons/repository)
- [Add-on Example](https://github.com/hassio-addons/addon-example)
- [Home Assistant Community Forums](https://community.home-assistant.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Bashio Documentation](https://github.com/hassio-addons/bashio)