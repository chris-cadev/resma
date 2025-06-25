#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly NC=$'\033[0m'

readonly PROJECT_CONFIG_FILE="pyproject.toml"
readonly SCRIPTS_DIR="$(dirname "$(realpath "$0")")"
TMP_MSG_FILE=""

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    case "$level" in
        INFO) printf "[%s] [\033[0;34m%s\033[0m] %s\n" "$timestamp" "$level" "$msg" ;;
        WARN) printf "[%s] [\033[1;33m%s\033[0m] %s\n" "$timestamp" "$level" "$msg" ;;
        ERROR) printf "[%s] [\033[0;31m%s\033[0m] %s\n" "$timestamp" "$level" "$msg" >&2 ;;
        *) printf "[%s] [%s] %s\n" "$timestamp" "$level" "$msg" ;;
    esac
}

cleanup() {
    if [[ -n "$TMP_MSG_FILE" && -f "$TMP_MSG_FILE" ]]; then
        rm -f "$TMP_MSG_FILE"
    fi
}
trap cleanup EXIT

error_exit() {
    log ERROR "$1"
    exit 1
}

usage() {
    cat << EOF
Usage: $0 version_type [version_tag]

Arguments:
  version_type  Required. Type of version bump: patch, minor, major, or custom-string
  version_tag   Optional. Version tag suffix, default is "local"

This script:
- Computes the next version based on version_type
- Updates the version in $PROJECT_CONFIG_FILE
- Amends the last git commit with the updated version file
- Tags the new version in git

Example:
  $0 minor
  $0 patch rc1
EOF
    exit 1
}

main() {
    if [[ "${1:-}" =~ ^(-h|--help)$ ]]; then
        usage
    fi

    if [[ $# -lt 1 || $# -gt 2 ]]; then
        usage
    fi

    local version_type="$1"
    local version_tag="${2:-local}"

    command -v git >/dev/null 2>&1 || error_exit "git not found in PATH"
    command -v pdm >/dev/null 2>&1 || error_exit "pdm not found in PATH"

    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        error_exit "Current directory is not inside a git repository"
    fi

    if [[ ! -x "$SCRIPTS_DIR/next-version.sh" ]]; then
        error_exit "Missing or not executable: $SCRIPTS_DIR/next-version.sh"
    fi

    log INFO "Computing next version..."
    local next_version
    next_version=$("$SCRIPTS_DIR/next-version.sh" "$version_type" "$version_tag" "$PROJECT_CONFIG_FILE") || error_exit "Failed to determine next version"

    if [[ -z "$next_version" ]]; then
        error_exit "Next version is empty"
    fi

    log INFO "Next version: ${YELLOW}$next_version${NC}"

    log INFO "Updating version in $PROJECT_CONFIG_FILE..."
    if output=$(pdm run toml set --toml-path "$PROJECT_CONFIG_FILE" project.version "$next_version" 2>&1); then
        log INFO "${GREEN}Version updated successfully${NC}"
    else
        error_exit "Failed to update version in $PROJECT_CONFIG_FILE: $output"
    fi
}

main "$@"
