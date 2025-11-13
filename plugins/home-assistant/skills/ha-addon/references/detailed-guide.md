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

## Troubleshooting

### Build and Container Issues

**Problem**: Docker build failures with package installation errors
- **Cause**: Incompatible base image, unavailable packages, or network connectivity issues
- **Solution**: Verify base image compatibility and check package availability in base OS
- **Debug**: Use local Docker builds to test before official builder
- **Fix**: Update package sources or use alternative base images

**Problem**: Container starts but immediately exits
- **Cause**: Missing service scripts, incorrect entry points, or permission issues
- **Solution**: Check s6-rc.d service configuration and ensure proper executable permissions
- **Debug**: Use `docker logs container_name` to see startup messages
- **Fix**: Verify service script paths and executable permissions in rootfs/

**Problem**: Add-on not appearing in Home Assistant Supervisor
- **Cause**: Invalid config.yaml format, missing required fields, or repository configuration issues
- **Solution**: Validate YAML syntax and check all required fields are present
- **Validate**: Run `ha addons validate /path/to/addon` for official validation
- **Fix**: Compare with working add-on examples and fix configuration errors

### Configuration and YAML Issues

**Problem**: YAML syntax errors in config files
- **Cause**: Incorrect indentation, missing quotes, or invalid characters
- **Solution**: Use YAML validators and proper indentation (2 spaces recommended)
- **Tools**: Use online YAML validators or `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`
- **Prevention**: Use IDE with YAML linting and syntax highlighting

**Problem**: Build configuration not working for multiple architectures
- **Cause**: Incorrect base image mappings or missing architecture-specific configurations
- **Solution**: Verify base image availability for all target architectures
- **Check**: Ensure all architectures (amd64, aarch64, armhf, armv7, i386) are properly configured
- **Test**: Use `--all` flag with official builder to test all architectures

### Permission and Security Issues

**Problem**: Add-on fails to access required resources
- **Cause**: Insufficient permissions in config.yaml or AppArmor profile blocking access
- **Solution**: Review and update permission settings, disable strict AppArmor for testing
- **Debug**: Check container logs for permission denied errors
- **Security**: Balance security requirements with functionality needs

**Problem**: Negative security rating affecting add-on acceptance
- **Cause**: Using host networking, PID sharing, or missing security features
- **Solution**: Enable ingress for web interfaces (+2), add custom AppArmor profiles (+1)
- **Optimization**: Sign images with CodeNotary (+1) and avoid insecure configurations
- **Guidelines**: Follow Home Assistant security best practices for maximum rating

### API Integration Issues

**Problem**: Home Assistant API calls failing
- **Cause**: Missing API permissions, incorrect authentication, or network issues
- **Solution**: Verify API permissions in config.yaml and check authentication setup
- **Debug**: Use bashio commands to test API connectivity from within container
- **Testing**: Manually test API endpoints before integrating into add-on code

**Problem**: Ingress not working for web interface
- **Cause**: Incorrect ingress configuration or port mapping issues
- **Solution**: Verify ingress settings in config.yaml and check internal port configuration
- **Debug**: Test web interface accessibility directly within container
- **Fix**: Ensure web service is listening on correct interface and port

### Performance and Resource Issues

**Problem**: Add-on consuming excessive memory or CPU
- **Cause**: Inefficient code, memory leaks, or resource-intensive operations
- **Solution**: Optimize application code and implement resource monitoring
- **Monitor**: Use Home Assistant Supervisor to monitor resource usage
- **Optimization**: Implement resource limits and efficient data structures

**Problem**: Slow startup times or delayed initialization
- **Cause**: Heavy initialization processes, network timeouts, or dependency loading delays
- **Solution**: Optimize startup sequence and implement timeout handling
- **Debug**: Add logging to identify bottlenecks in startup process
- **Improvement**: Use lazy loading and asynchronous initialization where possible

## Examples

### Example 1: Simple Web Service Add-on

**config.yaml:**
```yaml
name: Simple Web Service
version: 1.0.0
slug: simple-web
description: A basic web service add-on
url: https://github.com/user/simple-web-addon
arch:
  - amd64
  - aarch64
ingress: true
ingress_port: 8080
panel_icon: mdi:web
options:
  host: 0.0.0.0
  port: 8080
schema:
  host: str
  port: port
```

**Dockerfile:**
```dockerfile
FROM ghcr.io/home-assistant/amd64-base:latest

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
```

**Service script (rootfs/etc/s6-overlay/s6-rc.d/web-service/run):**
```bash
#!/bin/command -with-contenv sh
exec python3 /app/app.py
```

### Example 2: API Integration Add-on

**config.yaml with API access:**
```yaml
name: Home Assistant API Client
version: 2.0.0
slug: ha-api-client
description: Client for Home Assistant API integration
homeassistant_api: true
hassio_api: true
auth_api: true
arch:
  - amd64
  - aarch64
options:
  update_interval: 60
schema:
  update_interval: int(5, 300)
```

**Application code using bashio:**
```python
import asyncio
import aiohttp
import json

class HomeAssistantClient:
    def __init__(self):
        self.base_url = "http://supervisor/core"
        self.token = os.environ.get('SUPERVISOR_TOKEN')

    async def get_states(self):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.token}"}
            async with session.get(f"{self.base_url}/states", headers=headers) as resp:
                return await resp.json()

    async def call_service(self, domain, service, data):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/services/{domain}/{service}"
            async with session.post(url, json=data, headers=headers) as resp:
                return await resp.json()
```

### Example 3: Multi-Service Add-on with Docker Compose

**Dockerfile for complex service:**
```dockerfile
FROM ghcr.io/home-assistant/amd64-base:latest

# Install dependencies
RUN apk add --no-cache \
    nginx \
    php8-fpm \
    php8-cli \
    supervisor

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY php-fpm.conf /etc/php8/php-fpm.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy application
COPY . /app

# Expose ports
EXPOSE 80 443

CMD ["/usr/bin/supervisord"]
```

**Supervisor configuration (supervisord.conf):**
```ini
[supervisord]
nodaemon=true

[program:nginx]
command=nginx -g "daemon off;"
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:php-fpm]
command=php-fpm8
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:app]
command=php /app/index.php
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
```

### Example 4: Add-on with Custom AppArmor Profile

**config.yaml with security settings:**
```yaml
name: Secure Add-on
version: 1.0.0
slug: secure-addon
description: Add-on with enhanced security
apparmor: true
host_network: false
host_pid: false
full_access: false
arch:
  - amd64
  - aarch64
ingress: true
options:
  log_level: info
schema:
  log_level: list(debug|info|warning|error)
```

**AppArmor profile (rootfs/etc/apparmor.d/local/usr.bin.secure-addon):**
```apparmor
# Site-specific additions and overrides for usr.bin.secure-addon

# Allow network access
network inet stream,
network inet6 stream,

# Allow read access to configuration
owner /config/** r,
owner /data/** r,

# Deny access to sensitive files
deny /etc/passwd r,
deny /etc/shadow r,
deny /etc/ssh/** r,
```

## Performance Optimization

### Container Optimization

**Image Size Reduction**
- Use minimal base images (alpine, slim variants)
- Remove unnecessary packages and dependencies
- Multi-stage builds to eliminate build-time dependencies
- Optimize layer caching and minimize layer count

**Startup Performance**
- Implement lazy loading for heavy operations
- Use asynchronous initialization where possible
- Optimize service startup sequence with proper dependencies
- Implement health checks and graceful shutdown

**Resource Management**
- Set appropriate memory and CPU limits in config.yaml
- Monitor resource usage through Home Assistant Supervisor
- Implement resource pooling for database connections
- Use efficient data structures and algorithms

### Build Performance

**Multi-Architecture Build Optimization**
```yaml
# build.yaml
build_from:
  amd64: ghcr.io/home-assistant/amd64-base:3.18
  aarch64: ghcr.io/home-assistant/aarch64-base:3.18
  armhf: ghcr.io/home-assistant/armhf-base:3.18
  armv7: ghcr.io/home-assistant/armv7-base:3.18
  i386: ghcr.io/home-assistant/i386-base:3.18
codenotary:
  signer: your-signer-id
```

**CI/CD Performance**
- Use GitHub Actions with caching for dependencies
- Parallel builds for multiple architectures
- Implement build artifact caching
- Optimize test suite execution time

### Runtime Optimization

**Memory Efficiency**
```python
# Example: Memory-efficient processing
import gc
import sys

def process_data(data_stream):
    """Process data in chunks to minimize memory usage"""
    batch_size = 1000
    processed = []

    for chunk in chunked(data_stream, batch_size):
        processed.extend(process_chunk(chunk))
        gc.collect()  # Force garbage collection

    return processed

def process_chunk(chunk):
    """Process individual chunk"""
    # Process chunk efficiently
    return [transform(item) for item in chunk]
```

**Network Optimization**
- Implement connection pooling for HTTP requests
- Use compression for data transfer
- Cache frequently accessed data
- Implement timeout handling and retry logic

### Security Performance Balance

**Security Rating Optimization**
- Enable ingress (+2 rating) for web interfaces
- Add custom AppArmor profiles (+1 rating)
- Sign containers with CodeNotary (+1 rating)
- Avoid host networking (-1 rating) and PID sharing (-2 rating)

**Permission Management**
```yaml
# Minimal required permissions example
homeassistant_api: true  # Only if needed
hassio_api: false        # Use only if essential
auth_api: false         # Enable only for user auth
ingress: true            # Preferred over host_network
host_network: false     # Avoid when possible
host_pid: false         # Never enable unless essential
full_access: false      # Never enable in production
```

### Monitoring and Debugging

**Performance Monitoring**
```python
import time
import psutil
import logging

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)

    def log_resource_usage(self):
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()

        self.logger.info(f"Memory: {memory_mb:.2f}MB, CPU: {cpu_percent}%")

    def log_startup_time(self):
        startup_time = time.time() - self.start_time
        self.logger.info(f"Add-on startup completed in {startup_time:.2f}s")
```

**Debug Configuration**
```yaml
# Development config with debug logging
options:
  log_level: debug
  debug_mode: true
  enable_profiling: true
schema:
  log_level: list(debug|info|warning|error)
  debug_mode: bool
  enable_profiling: bool
```

## Troubleshooting Checklist

- [ ] Validate all YAML syntax (config.yaml, build.yaml)
- [ ] Check Dockerfile labels and build arguments
- [ ] Verify base image compatibility and package availability
- [ ] Test with local Docker builds
- [ ] Review security settings and permissions
- [ ] Check service management in s6-rc.d/
- [ ] Validate API integration and authentication
- [ ] Test multi-architecture builds if applicable
- [ ] Monitor resource usage during operation
- [ ] Test ingress and web interface connectivity
- [ ] Verify AppArmor profile syntax and effectiveness
- [ ] Check for memory leaks or performance bottlenecks