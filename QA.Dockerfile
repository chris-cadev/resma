# --- ttyd Stage ---
FROM python:3.13-slim AS ttyd
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential cmake git libjson-c-dev libwebsockets-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/tsl0922/ttyd.git ttyd
RUN mkdir -p ttyd/build && cd ttyd/build && cmake .. && make

# --- Python PDM + PEX Stage ---
FROM python:3.13-slim AS python-pdm
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pdm pex

COPY pyproject.toml pdm.lock README.md ./

RUN pdm install --prod --frozen-lockfile
RUN pdm run playwright install --with-deps chromium

COPY . .

RUN pex . -e resma.cli:main -o /app/resma --python-shebang="/usr/bin/env python3" --compress

RUN /app/resma --version
RUN /app/resma --help

# --- Final Image Stage ---
FROM python:3.13-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libjson-c5 libwebsockets-dev tini libssl-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ttyd /build/ttyd/build/ttyd /usr/bin/ttyd
COPY --from=python-pdm /app/resma /usr/local/bin/resma

EXPOSE 7681

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["ttyd", "-W", "bash"]
