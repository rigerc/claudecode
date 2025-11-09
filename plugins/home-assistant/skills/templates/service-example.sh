#!/command/with-contenv bashio
# shellcheck shell=bash

# Read configuration values
log_level=$(bashio::config 'log_level')
enable_feature=$(bashio::config 'enable_feature')
custom_port=$(bashio::config 'custom_port')

# Use configuration with validation
if bashio::config.has_value 'custom_port'; then
    port=$(bashio::config 'custom_port')
    bashio::log.info "Using configured port: ${port}"
else
    port=8080
    bashio::log.warning "No port configured, using default: ${port}"
fi

# Logging at different levels
bashio::log.trace "Detailed trace message"
bashio::log.debug "Debug information"
bashio::log.info "Starting service with log level: ${log_level}"
bashio::log.notice "Service started successfully"
bashio::log.warning "This is a warning message"
bashio::log.error "An error occurred"
bashio::log.fatal "Critical failure"

# Main service logic
main() {
    bashio::log.info "Starting main service loop..."

    while true; do
        # Your main service logic here
        sleep "${interval:-30}"
    done
}

# Execute main function
main "$@"