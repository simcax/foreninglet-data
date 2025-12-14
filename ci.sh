#!/bin/bash
set -euo pipefail

echo "🚀 Starting CI Pipeline for foreninglet-data"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

# Sync dependencies
echo "📦 Syncing dependencies with uv..."
uv sync --locked

# Run linting with black
echo "🔍 Running code formatting check with black..."
uv run black --check --diff --exclude="(.venv|foreninglet_data/sdk/)" .

# Run tests with coverage
echo "🧪 Running tests with coverage..."
uv run pytest --cov=foreninglet_data --cov-report=term-missing tests/ -v --tb=short

echo "✅ CI Pipeline completed successfully!"