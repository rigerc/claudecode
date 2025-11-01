#!/bin/bash
# example-basic-script
# Example of a basic bash script following Google Shell Style Guide
# This is an example asset that can be copied as a starting point

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Functions
main() {
  echo "Hello from ${SCRIPT_NAME}"
  echo "Script directory: ${SCRIPT_DIR}"

  # Example variable usage
  local message="${1:-Hello World!}"
  echo "Message: ${message}"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi