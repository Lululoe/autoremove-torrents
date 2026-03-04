FROM python:3.11-alpine

RUN apk add --no-cache bash su-exec tzdata

RUN pip install --no-cache-dir autoremove-torrents pyyaml

# Create directory structure
RUN mkdir -p /app /config && chmod 777 /config

COPY entrypoint.sh /app/entrypoint.sh
COPY run.py /app/run.py

RUN chmod +x /app/entrypoint.sh /app/run.py

WORKDIR /app

ENV PUID=1000
ENV PGID=1000
ENV INTERVAL=3600

VOLUME /config

ENTRYPOINT ["/app/entrypoint.sh"]
