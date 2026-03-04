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
  autoremove-torrents
```

### Docker Compose

```yaml
services:
  autoremove-torrents:
    image: autoremove-torrents
    container_name: autoremove-torrents
    environment:
      - PUID=1000
      - PGID=1000
      - INTERVAL=3600
    volumes:
      - /path/to/my/config:/config # Place config.yml inside here
    restart: unless-stopped
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PUID` | Optional user ID for the internal container process to match volume permissions. | `1000` |
| `PGID` | Optional group ID. | `1000` |
| `INTERVAL` | The interval in seconds to sleep in between executions. | `3600` |
| `CONFIG_YAML` | Can be set to a raw YAML string to create `config.yml` automatically on startup (helpful when native file mounts are restrictive). | *None* |

### Dynamic Environment Mapping

You can override or define configuration values by prepending variables with `ART_`. You can use double underscores `__` to map nested YAML properties.
Keys will be lowercased automatically during configuration generation.

*Example:* `ART_QBITTORRENT__HOST=192.168.1.1` becomes:

```yaml
qbittorrent:
  host: 192.168.1.1
```

*Example:* `ART_QBITTORRENT__USERNAME=admin` and `ART_QBITTORRENT__PASSWORD=secret` becomes:

```yaml
qbittorrent:
  username: admin
  password: secret
```

This flexibility allows you to inject keys seamlessly or keep secrets completely within the docker environment. 
