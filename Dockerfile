FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Copy only the necessary files for dependency installation
COPY uv.lock pyproject.toml /app/

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-install-workspace --package rascalapi

# Copy the entire project after dependencies are installed
COPY . /app/

# Sync project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --package rascalapi

CMD ["fastapi", "run", "--workers", "2", "app/main.py"]
