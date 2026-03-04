# Autoremove-torrents Docker Container

An automated, self-contained docker wrapper for [autoremove-torrents](https://github.com/jerrymakesjelly/autoremove-torrents).

It runs periodically on a customizable schedule and allows configuring `autoremove-torrents` either by mounting a native `config.yml` or through environment variables. If both are utilized, environment variables will override the YAML file mapping.

## Usage

### Docker CLI

```bash
docker run -d \
  --name autoremove-torrents \
  -e PUID=1000 \
  -e PGID=1000 \
  -e INTERVAL=3600 \
  -v /path/to/my/config.yml:/config/config.yml \
  ghcr.io/lululoe/autoremove-torrents:latest
```

### Docker Compose

```yaml
services:
  autoremove-torrents:
    image: ghcr.io/lululoe/autoremove-torrents:latest
    container_name: autoremove-torrents
    environment:
      - PUID=1000
      - PGID=1000
      - INTERVAL=3600
    volumes:
      - /path/to/my/config:/config # Place config.yml inside here
    restart: unless-stopped
```

## Tags and Architectures

This image is built for both `linux/amd64` and `linux/arm64` architectures.

The following tags are available on the GitHub Container Registry (`ghcr.io/lululoe/autoremove-torrents`):
- `latest`: The most recent stable release.
- `{major}.{minor}` (e.g. `1.5`): Follows the latest patch release for the given minor version.
- `{version}` (e.g. `1.5.0`): A specific, immutable release version.
- `edge`: The latest unstable pipeline build from the `main` branch.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PUID` | Optional user ID for the internal container process to match volume permissions. | `1000` |
| `PGID` | Optional group ID. | `1000` |
| `INTERVAL` | The interval in seconds to sleep in between executions. | `3600` |
| `CONFIG_YAML` | Can be set to a raw YAML string to create `config.yml` automatically on startup (helpful when native file mounts are restrictive). | *None* |

### Dynamic Environment Mapping

You can override or define configuration values by prepending variables with `CONFIG_`. You can use double underscores `__` to map nested YAML properties.
Keys will be lowercased automatically during configuration generation.

*Example:* `CONFIG_QBITTORRENT__HOST=192.168.1.1` becomes:

```yaml
qbittorrent:
  host: 192.168.1.1
```

*Example:* `CONFIG_QBITTORRENT__USERNAME=admin` and `CONFIG_QBITTORRENT__PASSWORD=secret` becomes:

```yaml
qbittorrent:
  username: admin
  password: secret
```

This flexibility allows you to inject keys seamlessly or keep secrets completely within the docker environment. 
