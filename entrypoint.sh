#!/bin/bash
set -e

PUID=${PUID:-1000}
PGID=${PGID:-1000}

echo "Ensuring user abc with UID=${PUID} and GID=${PGID} exists"

# Add group if it doesn't exist
if ! getent group abc > /dev/null; then
    addgroup -g "${PGID}" abc
fi

# Add user if it doesn't exist
if ! getent passwd abc > /dev/null; then
    adduser -u "${PUID}" -D -G abc -h /config abc
fi

# We only try to chown the config directory explicitly if we are root
chown abc:abc /config || true

if [ -n "$CONFIG_YAML" ]; then
    echo "Creating /config/config.yml from CONFIG_YAML environment variable"
    echo "$CONFIG_YAML" > /config/config.yml
    chown abc:abc /config/config.yml || true
fi

echo "Starting autoremove-torrents loop..."
# The -u flag to python ensures output isn't buffered, allowing docker to capture logs
exec su-exec abc python -u /app/run.py
