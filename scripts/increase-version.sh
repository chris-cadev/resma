#!/bin/bash -e

TOML_FILE=./pyproject.toml
VERSION_TYPE="$1"

VERSION_PARTS=($(pdm run toml get --toml-path "$TOML_FILE" project.version | xargs -d '.'))
MAJOR_VERSION=${VERSION_PARTS[0]}
MINOR_VERSION=${VERSION_PARTS[1]}
PATCH_VERSION=${VERSION_PARTS[2]}

CURRENT_VERSION="${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}"

case "$VERSION_TYPE" in
    patch)
        PATCH_VERSION=$((PATCH_VERSION + 1))
    ;;
    minor)
        MINOR_VERSION=$((MINOR_VERSION + 1))
    ;;
    major)
        MAJOR_VERSION=$((MAJOR_VERSION + 1))
    ;;
esac

NEXT_VERSION="${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}"
if [ "$NEXT_VERSION" == "$CURRENT_VERSION" ]; then
    NEXT_VERSION="$CURRENT_VERSION-$VERSION_TYPE.$(date '+%Y%m%d%H')"
fi

echo "$CURRENT_VERSION -> $NEXT_VERSION"
if ! [[ -t 0 ]]; then
    echo "No TTY available. Cannot read user input."
else
    echo 'is it the expected version change? (Y/n) '
    read accepted
    accepted=$(printf '%s' "$accepted" | tr '[:upper:]' '[:lower:]')
    accepted=${accepted:-y}
    if [ "$accepted" != "y" ]; then
        exit 1
    fi
fi
pdm run toml set --toml-path "$TOML_FILE" project.version "$NEXT_VERSION"
