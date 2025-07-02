# --- ttyd Stage ---
FROM debian:bullseye-slim AS ttyd
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /build

RUN apt-get update && \
    apt-get install -y cmake g++ git libjson-c-dev libwebsockets-dev

RUN git clone --depth 1 https://github.com/tsl0922/ttyd.git ttyd
RUN mkdir -p ttyd/build && \
    cd ttyd/build && \
    cmake .. && \
    make

# --- Python PDM + Shiv Stage ---
FROM python:3.13-slim AS python-pdm
WORKDIR /app

# Install PDM, Git, and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

# Install PDM and Shiv
RUN pip install --no-cache-dir pdm
RUN pip install --no-cache-dir shiv

# Copy dependency files first for caching
COPY pyproject.toml pdm.lock README.md ./

# Install dependencies
RUN pdm install --prod --frozen-lockfile
RUN pdm run playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Build standalone executable using Shiv
RUN shiv \
    --compressed \
    -c resma \
    -e resma.cli:main \
    -o /app/resma \
    -p "/usr/bin/env python3" \
    .
RUN /app/resma --version
RUN /app/resma --help

# --- Final Image Stage ---
FROM debian:bullseye-slim
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies for ttyd and the shiv binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libjson-c5 \
    libwebsockets16 \
    python3 \
    python3-pycurl \
    tini && \
    rm -rf /var/lib/apt/lists/*

# Copy ttyd from build stage
COPY --from=ttyd /build/ttyd/build/ttyd /usr/bin/ttyd

# Copy standalone resma binary from python-pdm stage
COPY --from=python-pdm /app/resma /usr/local/bin/resma

# Expose ttyd port
EXPOSE 7681

# Set entrypoint and command
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["ttyd", "-W", "bash"]
