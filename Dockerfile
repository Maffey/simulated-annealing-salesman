FROM ghcr.io/astral-sh/uv:python3.11-alpine

ADD . /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install dependencies
RUN uv sync --locked

CMD ["uv", "run", "sas"]