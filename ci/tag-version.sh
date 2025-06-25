#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly BLUE=$'\033[0;34m'
readonly NC=$'\033[0m'

readonly PROJECT_CONFIG_FILE="pyproject.toml"
readonly SCRIPTS_DIR="$(dirname "$(realpath "$0")")"

log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    case "$level" in
        INFO) printf "[%s] [${BLUE}%s${NC}] %s\n" "$timestamp" "$level" "$msg" ;;
        WARN) printf "[%s] [${YELLOW}%s${NC}] %s\n" "$timestamp" "$level" "$msg" ;;
        ERROR) printf "[%s] [${RED}%s${NC}] %s\n" "$timestamp" "$level" "$msg" >&2 ;;
        SUCCESS) printf "[%s] [${GREEN}%s${NC}] %s\n" "$timestamp" "$level" "$msg" ;;
        *) printf "[%s] [%s] %s\n" "$timestamp" "$level" "$msg" ;;
    esac
}

error_exit() {
    log ERROR "$1"
    exit 1
}

usage() {
    cat <<EOF
Usage: $0

Tags the current Git commit using the version from $PROJECT_CONFIG_FILE

Requirements:
  - 'pdm' must be installed
  - 'toml-cli' must be accessible via 'pdm run'
  - Must be inside a git repository

EOF
    exit 1
}

main() {
    [[ "${1:-}" =~ ^(-h|--help)$ ]] && usage

    command -v git >/dev/null 2>&1 || error_exit "git not found in PATH"
    command -v pdm >/dev/null 2>&1 || error_exit "pdm not found in PATH"

    [[ -f "$PROJECT_CONFIG_FILE" ]] || error_exit "Missing $PROJECT_CONFIG_FILE"
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || error_exit "Not inside a git repository"

    log INFO "Extracting project version from $PROJECT_CONFIG_FILE"
    version=$(pdm run toml get --toml-path "$PROJECT_CONFIG_FILE" project.version) || error_exit "Failed to extract version"
    tag="v$version"
    log INFO "Version extracted: ${YELLOW}$version${NC}"

    if git rev-parse --verify "$tag" >/dev/null 2>&1; then
        log WARN "Tag '$tag' already exists. Aborting."
        exit 1
    fi

    log INFO "Creating Git tag '$tag'"
    git tag "$tag" || error_exit "Failed to create tag"

    log SUCCESS "Tag '$tag' created"
}

main "$@"
