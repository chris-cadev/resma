#!/bin/bash -e

TOML_FILE=./pyproject.toml
VERSION_TYPE="$1"
LOCAL_TAG="$2"

RAW_VERSION=$(pdm run -v toml get --toml-path "$TOML_FILE" project.version)

BASE_PART=${RAW_VERSION%%[!0-9.]*}
REMAINDER=${RAW_VERSION#"$BASE_PART"}
PRERELEASE_PART=""
LOCAL_PART=""

if [[ "$REMAINDER" =~ ^(\.[a-z]+[0-9]*)?(.*)$ ]]; then
    PRERELEASE_PART="${BASH_REMATCH[1]}"
    LOCAL_PART="${BASH_REMATCH[2]}"
fi

IFS='.' read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "$BASE_PART"
PATCH_VERSION=${PATCH_VERSION:-0}

CURRENT_VERSION="${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}${PRERELEASE_PART}${LOCAL_PART}"

case "$VERSION_TYPE" in
    patch)
        PATCH_VERSION=$((PATCH_VERSION + 1))
        PRERELEASE_PART=""
        LOCAL_PART=""
    ;;
    minor)
        MINOR_VERSION=$((MINOR_VERSION + 1))
        PATCH_VERSION=0
        PRERELEASE_PART=""
        LOCAL_PART=""
    ;;
    major)
        MAJOR_VERSION=$((MAJOR_VERSION + 1))
        MINOR_VERSION=0
        PATCH_VERSION=0
        PRERELEASE_PART=""
        LOCAL_PART=""
    ;;
    alpha)
        if [[ "$PRERELEASE_PART" =~ \.a([0-9]+) ]]; then
            NUM=${BASH_REMATCH[1]}
            PRERELEASE_PART=".a$((NUM + 1))"
        else
            PRERELEASE_PART=".a1"
        fi
        LOCAL_PART=""
    ;;
    beta)
        if [[ "$PRERELEASE_PART" =~ \.b([0-9]+) ]]; then
            NUM=${BASH_REMATCH[1]}
            PRERELEASE_PART=".b$((NUM + 1))"
        else
            PRERELEASE_PART=".b1"
        fi
        LOCAL_PART=""
    ;;
    rc | release-candidate)
        if [[ "$PRERELEASE_PART" =~ \.rc([0-9]+) ]]; then
            NUM=${BASH_REMATCH[1]}
            PRERELEASE_PART=".rc$((NUM + 1))"
        else
            PRERELEASE_PART=".rc1"
        fi
        LOCAL_PART=""
    ;;
    local)
        TIMESTAMP="$(date '+%Y%m%d%H%M%S')"
        TAG="${LOCAL_TAG:-local}"
        LOCAL_PART="+${TAG}.${TIMESTAMP}"
    ;;
    *)
        echo "Invalid version type: $VERSION_TYPE"
        echo "Allowed types: major, minor, patch, alpha, beta, rc, local"
        exit 1
    ;;
esac

NEXT_VERSION="${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}${PRERELEASE_PART}${LOCAL_PART}"

if [ "$NEXT_VERSION" == "$CURRENT_VERSION" ]; then
    LOCAL_PART="+${VERSION_TYPE}.$(date '+%Y%m%d%H%M')"
    NEXT_VERSION="${CURRENT_VERSION}${LOCAL_PART}"
fi

echo "$CURRENT_VERSION -> $NEXT_VERSION"

if ! [[ -t 0 ]]; then
    echo "No TTY available. Cannot read user input."
else
    echo 'Is it the expected version change? (Y/n) '
    read accepted
    accepted=$(printf '%s' "$accepted" | tr '[:upper:]' '[:lower:]')
    accepted=${accepted:-y}
    if [ "$accepted" != "y" ]; then
        exit 1
    fi
fi

pdm run toml set --toml-path "$TOML_FILE" project.version "$NEXT_VERSION"
