# Development Docker container configuration
# hadolint ignore=DL3007
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SHELL=/bin/bash

# hadolint ignore=DL3008,DL3009
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip

# hadolint ignore=DL3013
RUN pip3 install pipenv

# Create non-root run user and a project base directory
RUN mkdir /app /home/app && \
    useradd -d /home/app -b /app app && \
    chown app:app /app /home/app

# Copy an entrypoint script
COPY ./entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]

# Set working directory and run user
WORKDIR /app
USER app
