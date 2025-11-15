# Argcfile.sh Patterns

Common patterns for using Argc as a project automation tool (like Make or npm scripts).

## Basic Argcfile.sh

Place in project root as `Argcfile.sh`:

```bash
#!/usr/bin/env bash
# Argcfile.sh - Project automation

set -euo pipefail

# @meta dotenv
# @meta require-tools node,npm

# @cmd Install dependencies
install() {
    npm install
}

# @cmd Build project
# @option -m --mode[dev|prod]=dev
build() {
    install
    npm run build -- --mode "$argc_mode"
}

# @cmd Run tests
# @arg pattern*    Test patterns
test() {
    npm test -- "${argc_pattern[@]}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

**Usage:**
```bash
argc install
argc build --mode prod
argc test "**/*.test.js"
```

## Development Workflow

Complete development environment setup and tasks:

```bash
#!/usr/bin/env bash
# Argcfile.sh

set -euo pipefail

# @meta dotenv
# @meta require-tools node,npm,docker

# Environment
# @env NODE_ENV=development
# @env PORT=3000

# @cmd Setup development environment
# @flag --full    Complete setup with database
setup() {
    echo "Installing dependencies..."
    npm install

    if [[ "$argc_full" -eq 1 ]]; then
        echo "Setting up database..."
        docker-compose up -d postgres
        npm run db:migrate
        npm run db:seed
    fi

    echo "Setup complete!"
}

# @cmd Start development server
# @option -p --port=${PORT}
# @option --host=localhost
# @flag -d --debug
# @meta default-subcommand
dev() {
    local port="$argc_port"

    if [[ "$argc_debug" -eq 1 ]]; then
        export DEBUG=*
    fi

    echo "Starting server on $argc_host:$port"
    npm run dev -- --port "$port" --host "$argc_host"
}

# @cmd Build for production
# @flag --analyze    Bundle analysis
# @flag --no-clean   Skip clean step
build() {
    if [[ "$argc_no_clean" -ne 1 ]]; then
        rm -rf dist/
    fi

    npm run build:prod

    if [[ "$argc_analyze" -eq 1 ]]; then
        npm run analyze
    fi
}

# @cmd Run tests
test() { :; }

# @cmd Run unit tests
# @option --coverage[lcov|html]
# @arg pattern*
test::unit() {
    local cmd="npm test"

    if [[ -n "${argc_pattern[*]:-}" ]]; then
        cmd="$cmd -- ${argc_pattern[*]}"
    fi

    if [[ -n "$argc_coverage" ]]; then
        cmd="$cmd -- --coverage --coverageReporters=$argc_coverage"
    fi

    eval "$cmd"
}

# @cmd Run integration tests
# @flag --docker    Run with Docker services
test::integration() {
    if [[ "$argc_docker" -eq 1 ]]; then
        docker-compose up -d
        trap 'docker-compose down' EXIT
    fi

    npm run test:integration
}

# @cmd Linting and formatting
lint() { :; }

# @cmd Check code style
# @flag --fix    Auto-fix issues
lint::check() {
    if [[ "$argc_fix" -eq 1 ]]; then
        npm run lint -- --fix
        npm run format
    else
        npm run lint
    fi
}

# @cmd Type checking
lint::types() {
    npm run typecheck
}

eval "$(argc --argc-eval "$0" "$@")"
```

**Usage:**
```bash
argc                          # Runs dev (default subcommand)
argc setup --full             # Full setup
argc dev --port 4000 --debug  # Dev server with debug
argc build --analyze          # Production build with analysis
argc test unit --coverage html
argc test integration --docker
argc lint check --fix
```

## Deployment Patterns

Multi-environment deployment automation:

```bash
#!/usr/bin/env bash
# Argcfile.sh

set -euo pipefail

# @meta dotenv

# @env AWS_REGION=us-east-1
# @env DOCKER_REGISTRY!

# Dynamic functions
_list_versions() {
    git tag --sort=-version:refname | head -10
}

_current_branch() {
    git branch --show-current
}

# @cmd Build and tag Docker image
# @option -t --tag=latest    Image tag
# @flag --no-cache           Build without cache
docker::build() {
    local image="${DOCKER_REGISTRY}/myapp:${argc_tag}"

    local build_args="--tag $image"
    [[ "$argc_no_cache" -eq 1 ]] && build_args="$build_args --no-cache"

    docker build $build_args .
    echo "Built: $image"
}

# @cmd Push Docker image
# @option -t --tag=latest    Image tag
docker::push() {
    local image="${DOCKER_REGISTRY}/myapp:${argc_tag}"
    docker push "$image"
}

# @cmd Deploy application
deploy() { :; }

# @cmd Deploy to staging
# @option -b --branch=`_current_branch`
# @flag --skip-tests
deploy::staging() {
    if [[ "$argc_skip_tests" -ne 1 ]]; then
        echo "Running tests..."
        argc test unit
    fi

    echo "Building for staging..."
    argc docker build --tag "staging-${argc_branch}"
    argc docker push --tag "staging-${argc_branch}"

    echo "Deploying to staging..."
    # Deployment commands here
}

# @cmd Deploy to production
# @arg version[`_list_versions`]!
# @flag --dry-run
deploy::production() {
    local version="$argc_version"

    # Validate version exists
    if ! git rev-parse --verify "$version" >/dev/null 2>&1; then
        echo "Error: Version $version not found" >&2
        exit 1
    fi

    if [[ "$argc_dry_run" -eq 1 ]]; then
        echo "DRY RUN: Would deploy $version to production"
        return
    fi

    echo "Building version $version..."
    git checkout "$version"
    argc docker build --tag "$version"
    argc docker push --tag "$version"

    echo "Deploying $version to production..."
    # Production deployment
}

# @cmd Rollback deployment
# @arg env[staging|production]!
# @arg version[`_list_versions`]!
deploy::rollback() {
    echo "Rolling back $argc_env to $argc_version..."
    # Rollback logic
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Database Management

Database tasks and migrations:

```bash
#!/usr/bin/env bash
# Argcfile.sh

set -euo pipefail

# @meta dotenv
# @env DB_URL!

# @cmd Database operations
db() { :; }

# @cmd Run migrations
# @arg direction[up|down]=up
# @option -v --version    Target version
db::migrate() {
    echo "Running migrations: $argc_direction"

    if [[ -n "$argc_version" ]]; then
        npm run migrate -- --to "$argc_version"
    else
        npm run migrate -- --"$argc_direction"
    fi
}

# @cmd Create new migration
# @arg name!    Migration name
db::migration::create() {
    local timestamp=$(date +%Y%m%d%H%M%S)
    local filename="migrations/${timestamp}_${argc_name}.sql"

    cat > "$filename" <<EOF
-- Migration: ${argc_name}
-- Created: $(date)

-- UP
CREATE TABLE ...;

-- DOWN
DROP TABLE ...;
EOF

    echo "Created: $filename"
}

# @cmd Seed database
# @flag --reset    Reset before seeding
db::seed() {
    if [[ "$argc_reset" -eq 1 ]]; then
        npm run db:reset
    fi

    npm run db:seed
}

# @cmd Create backup
# @option -o --output    Output file (default: timestamped)
db::backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output="${argc_output:-backup_${timestamp}.sql}"

    pg_dump "$DB_URL" > "$output"
    echo "Backup created: $output"
}

# @cmd Restore from backup
# @arg file!    Backup file
# @flag --force    Skip confirmation
db::restore() {
    if [[ "$argc_force" -ne 1 ]]; then
        read -p "Restore from ${argc_file}? This will overwrite data. [y/N] " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
    fi

    psql "$DB_URL" < "$argc_file"
    echo "Database restored from ${argc_file}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Monorepo Pattern

Managing multiple packages in a monorepo:

```bash
#!/usr/bin/env bash
# Argcfile.sh

set -euo pipefail

# List all packages
_list_packages() {
    find packages -maxdepth 1 -mindepth 1 -type d -exec basename {} \;
}

# @cmd Install dependencies for all packages
install::all() {
    npm install
    for pkg in packages/*; do
        (cd "$pkg" && npm install)
    done
}

# @cmd Install for specific package
# @arg package[`_list_packages`]!
install::pkg() {
    (cd "packages/${argc_package}" && npm install)
}

# @cmd Build operations
build() { :; }

# @cmd Build all packages
# @flag --clean    Clean before build
build::all() {
    [[ "$argc_clean" -eq 1 ]] && clean::all

    for pkg in packages/*; do
        echo "Building $(basename "$pkg")..."
        (cd "$pkg" && npm run build)
    done
}

# @cmd Build specific package
# @arg package[`_list_packages`]!
# @flag --watch
build::pkg() {
    local pkg_dir="packages/${argc_package}"

    if [[ "$argc_watch" -eq 1 ]]; then
        (cd "$pkg_dir" && npm run build -- --watch)
    else
        (cd "$pkg_dir" && npm run build)
    fi
}

# @cmd Clean build artifacts
clean() { :; }

# @cmd Clean all packages
clean::all() {
    for pkg in packages/*; do
        rm -rf "$pkg/dist" "$pkg/node_modules/.cache"
    done
}

# @cmd Clean specific package
# @arg package[`_list_packages`]!
clean::pkg() {
    local pkg_dir="packages/${argc_package}"
    rm -rf "$pkg_dir/dist" "$pkg_dir/node_modules/.cache"
}

# @cmd Run command in package
# @arg package[`_list_packages`]!
# @arg command+    Command to run
run() {
    (cd "packages/${argc_package}" && "${argc_command[@]}")
}

eval "$(argc --argc-eval "$0" "$@")"
```

**Usage:**
```bash
argc install all
argc build pkg api --watch
argc run api npm test
```

## Hooks and Validation

Using hooks for cross-cutting concerns:

```bash
#!/usr/bin/env bash
# Argcfile.sh

set -euo pipefail

# @meta dotenv
# @meta require-tools node,npm

# Validation hook
_argc_before() {
    # Check for required files
    if [[ ! -f package.json ]]; then
        echo "Error: package.json not found" >&2
        exit 1
    fi

    # Environment validation
    if [[ "$argc__fn" == "deploy"* ]] && [[ -z "${CI:-}" ]]; then
        echo "Warning: Not running in CI environment" >&2
    fi
}

# Cleanup hook
_argc_after() {
    local exit_code=$?

    # Clean temporary files
    rm -f /tmp/argc-*.tmp

    # Log execution time
    if [[ -n "${ARGC_START_TIME:-}" ]]; then
        local duration=$((SECONDS - ARGC_START_TIME))
        echo "Completed in ${duration}s"
    fi

    return $exit_code
}

# Track start time
ARGC_START_TIME=$SECONDS

# @cmd Build project
build() {
    npm run build
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Best Practices

1. **Use `set -euo pipefail`** for safe script execution
2. **Always use `@meta dotenv`** for environment variable management
3. **Declare required tools** with `@meta require-tools`
4. **Use dynamic functions** for choices that change (branches, versions)
5. **Group related commands** with namespaces (`deploy::staging`)
6. **Add default subcommand** for most common operation
7. **Include cleanup** in `_argc_after` hook
8. **Validate prerequisites** in `_argc_before` hook
9. **Use meaningful defaults** for options
10. **Document with descriptions** - they appear in `--help`
