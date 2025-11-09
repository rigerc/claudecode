---
name: Home Assistant Add-on Development
description: Create, build, and publish Home Assistant add-ons. Use when developing Home Assistant add-ons, troubleshooting container issues, configuring Docker-based services, or working with YAML configuration files for Home Assistant extensions.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, TodoWrite
---

# Home Assistant Add-on Development

Specializes in creating, configuring, building, and publishing Home Assistant add-ons with expertise in Docker containerization, YAML configuration, security best practices, and Home Assistant API integration.

## When to Use

- **Creating new add-ons**: From initial structure to configuration files
- **Building and testing**: Docker builds, local testing, and CI/CD setup
- **Configuration management**: YAML files, build configurations, and Dockerfiles
- **Security and permissions**: AppArmor profiles, API access, and security ratings
- **API integration**: Home Assistant APIs, ingress, and authentication
- **Troubleshooting**: Build failures, permission issues, and debugging container problems
- **Publishing**: Repository setup, versioning, and distribution

## Core Expertise

### Add-on Structure and Files
- **config.yaml**: Main configuration with metadata, options, schema, and permissions
- **build.yaml**: Multi-architecture build configuration and CodeNotary signing
- **Dockerfile**: Container build instructions with required labels and base images
- **rootfs/**: Filesystem overlay structure with s6-rc.d service management
- **repository.yaml**: Add-on repository configuration for publishing

### Development Workflow
1. **Setup development environment** with Docker and Home Assistant instance
2. **Create add-on structure** following the official directory layout
3. **Configure build settings** for target architectures (amd64, aarch64, armhf, armv7, i386)
4. **Implement functionality** with proper service management and error handling
5. **Test locally** using Docker containers and Home Assistant integration
6. **Publish** through GitHub Actions and add-on repositories

### Security Best Practices
- **Security ratings**: Understand +2 to -2 point system for different configurations
- **AppArmor profiles**: Create custom security profiles for enhanced isolation
- **Permission management**: Use minimum required privileges and API access
- **CodeNotary signing**: Sign images for additional security (+1 rating)
- **Network security**: Avoid host networking unless absolutely necessary

### Configuration Patterns
- **Options schema**: Define user-configurable settings with validation
- **Port mapping**: Configure network access with proper security considerations
- **Volume mapping**: Share data with Home Assistant while maintaining security
- **API integration**: Enable Home Assistant, Supervisor, and authentication APIs
- **Ingress setup**: Provide web interface access through Home Assistant UI

## Common Tasks

### Initialize New Add-on
1. Create directory structure with rootfs/, config.yaml, build.yaml, Dockerfile
2. Set up basic configuration with name, version, architecture support
3. Implement s6-overlay service management in rootfs/s6-rc.d/
4. Add build configuration for multi-architecture support

### Debug Build Issues
- Check base image compatibility and package availability
- Validate YAML syntax in config files
- Verify Dockerfile labels and build arguments
- Test with local Docker builds before using official builder

### Optimize Security Rating
- Enable ingress (+2) for web interfaces
- Add custom AppArmor profile (+1) for enhanced security
- Sign with CodeNotary (+1) for image verification
- Avoid host PID (-2) and unnecessary host networking (-1)

### Set Up CI/CD
- Configure GitHub Actions with home-assistant/builder
- Set up multi-architecture builds for all supported platforms
- Configure automated testing and Docker Hub publishing
- Add release tagging and repository updating

### API Integration Patterns
- **Bashio usage**: Read configuration, make service calls, handle logging
- **Authentication**: Use Home Assistant auth backend instead of storing credentials
- **Service discovery**: Register and discover add-on services
- **Data access**: Safely read from Home Assistant configuration and data

## Development Tools

### Local Testing
```bash
# Build with official builder (all architectures)
docker run --rm --privileged -v /path/to/addon:/data \
  ghcr.io/home-assistant/amd64-builder -t /data --all --test

# Build for current architecture only
docker build --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base:latest" \
  -t local/my-test-addon .
```

### Configuration Validation
```bash
# Validate config.yaml schema
ha addons validate /path/to/addon

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### Debugging Commands
```bash
# Enter running container
docker exec -it container_name /bin/bash

# View container logs
docker logs container_name

# Check configuration
docker inspect container_name
```

## File Templates

Use standard templates for common files:

- **config.yaml**: Complete configuration with security settings
- **Dockerfile**: Multi-stage build with required labels
- **build.yaml**: Architecture-specific base images and signing
- **service scripts**: s6-rc.d service management with proper error handling
- **AppArmor profiles**: Custom security profiles for enhanced protection

## Integration Points

### Home Assistant APIs
- **homeassistant_api**: Access to Home Assistant core API
- **hassio_api**: Supervisor API for system management
- **auth_api**: Authentication backend for user validation
- **ingress**: Web interface integration through Home Assistant UI

### External Services
- **CodeNotary**: Image signing and verification
- **Docker Hub**: Container image distribution
- **GitHub Actions**: Automated builds and publishing
- **Add-on repositories**: Community distribution channels

## Resources

- Reference documentation is available in the full guide
- Use official Home Assistant add-on examples
- Check community repositories for patterns and best practices
- Monitor Home Assistant forums for updates and issues

## Troubleshooting Checklist

- [ ] Validate all YAML syntax (config.yaml, build.yaml)
- [ ] Check Dockerfile labels and build arguments
- [ ] Verify base image compatibility and package availability
- [ ] Test with local Docker builds
- [ ] Review security settings and permissions
- [ ] Check service management in s6-rc.d/
- [ ] Validate API integration and authentication
- [ ] Test multi-architecture builds if applicable